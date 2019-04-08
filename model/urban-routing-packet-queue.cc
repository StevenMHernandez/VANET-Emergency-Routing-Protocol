/* -*- Mode:C++; c-file-style:"gnu"; indent-tabs-mode:nil; -*- */
#include "urban-routing-packet-queue.h"
#include <algorithm>
#include <functional>
#include "ns3/ipv4-route.h"
#include "ns3/socket.h"
#include "ns3/log.h"
#include "urban-routing-packet.h"

using namespace std;



/**
 * \file
 * \ingroup UrbanRouting
 * ns3::UrbanRouting::QueueEntry and ns3::UrbanRouting::PacketQueue declarations.
 */


namespace ns3 {
NS_LOG_COMPONENT_DEFINE ("UrbanRoutingPacketQueue");

namespace UrbanRouting {


QueueEntry::QueueEntry (void)
  : m_packet (0),
    m_header (Ipv4Header ()),
    m_ucb (UnicastForwardCallback ()),
    m_ecb (ErrorCallback ()),
    m_expire (Simulator::Now ()),
    m_packetID (0)
{
}

QueueEntry::QueueEntry (Ptr<const Packet> pa,
                        Ipv4Header const & h,
                        UnicastForwardCallback ucb,
                        ErrorCallback ecb,
                        Time exp /* = Simulator::Now () */,
                        uint32_t packetID /* = 0 */)
  : m_packet (pa),
    m_header (h),
    m_ucb (ucb),
    m_ecb (ecb),
    m_expire (exp),
    m_packetID (packetID)
{
}




bool
QueueEntry::operator== (QueueEntry const & o) const
{
  return (m_packetID == o.m_packetID);
}

QueueEntry::UnicastForwardCallback
QueueEntry::GetUnicastForwardCallback () const
{
  return m_ucb;
}

void
QueueEntry::SetUnicastForwardCallback (QueueEntry::UnicastForwardCallback ucb)
{
  m_ucb = ucb;
}

QueueEntry::ErrorCallback
QueueEntry::GetErrorCallback () const
{
  return m_ecb;
}

void
QueueEntry::SetErrorCallback (QueueEntry::ErrorCallback ecb)
{
  m_ecb = ecb;
}

Ptr<const Packet>
QueueEntry::GetPacket () const
{
  return m_packet;
}

void
QueueEntry::SetPacket (Ptr<const Packet> p)
{
  NS_LOG_FUNCTION (this << p);
  m_packet = p;
}

Ipv4Header
QueueEntry::GetIpv4Header () const
{
  return m_header;
}

void
QueueEntry::SetIpv4Header (Ipv4Header h)
{
  NS_LOG_FUNCTION (this << h);
  m_header = h;
}

void
QueueEntry::SetExpireTime (Time exp)
{
  NS_LOG_FUNCTION (this << exp);
  m_expire = exp;
}

Time
QueueEntry::GetExpireTime () const
{
  return m_expire;
}

uint32_t
QueueEntry::GetPacketID () const
{
  return m_packetID;
}

void
QueueEntry::SetPacketID (uint32_t id)
{
  NS_LOG_FUNCTION (this << id);
  m_packetID = id;
}



PacketQueue::PacketQueue (uint32_t maxLen)
{
  NS_LOG_FUNCTION (this << maxLen);
  m_maxLen = maxLen;
}

uint32_t
PacketQueue::GetSize ()
{
  return m_map.size ();
}

bool
PacketQueue::Enqueue (QueueEntry & entry)
{
  NS_LOG_FUNCTION (this << entry.GetPacketID ());
  // Add or update the entry
  m_map[entry.GetPacketID ()] = entry;
  Purge (true);
  return true;
}

bool
PacketQueue::Dequeue (QueueEntry& entry)
{
  NS_LOG_FUNCTION (this << entry.GetPacketID ());
  if (m_map.size () > 0)
    {
      PacketIdMap::iterator entry_map = m_map.begin ();
      entry = entry_map->second;
      m_map.erase (entry_map);
      return true;
    }
  return false;
}

uint32_t
PacketQueue::GetMaxQueueLen () const
{
  NS_LOG_FUNCTION (this );
  return m_maxLen;
}

void
PacketQueue::SetMaxQueueLen (uint32_t len)
{
  NS_LOG_FUNCTION (this << len);
  m_maxLen = len;
}

QueueEntry
PacketQueue::Find (uint32_t packetID)
{
  NS_LOG_FUNCTION (this << packetID);
  PacketIdMap::iterator entry = m_map.find (packetID);
  if (entry != m_map.end ())
    {
      return entry->second;
    }
  return QueueEntry ();
}


// static
bool
PacketQueue::IsEarlier (const PacketIdMapPair & e1,
                        const PacketIdMapPair & e2)
{
  return (e1.second.GetExpireTime () < e2.second.GetExpireTime ());
}


void
PacketQueue::Purge (bool outdated /* = false */)
{
  NS_LOG_FUNCTION (this << outdated);
  if (outdated && m_map.size () > m_maxLen)
    {
      Drop (std::min_element (m_map.begin (), m_map.end (), IsEarlier),
            "Drop the oldest packet");
    }
  else
    {
      for (PacketIdMap::iterator i = m_map.begin ();
           i != m_map.end (); ++i)
        {
          if (i->second.GetExpireTime () < Now ())
            {
              Drop (i, "Drop outdated packet ");
            }
        }
    }
}

void
PacketQueue::Drop (PacketIdMap::iterator en, std::string reason)
{
  NS_LOG_FUNCTION (this << en->second.GetPacketID () << reason);
  m_map.erase (en->second.GetPacketID ());
}



VehiclePathVectorHeader
PacketQueue::GetVehiclePathVector ()
{
  NS_LOG_FUNCTION (this );
  Purge (true);
  VehiclePathVectorHeader sm (m_map.size ());
  for (PacketIdMap::iterator i = m_map.begin (); i != m_map.end (); ++i)
    {
      sm.Add (i->first);
    }
  return sm;
}


VehiclePathVectorHeader
PacketQueue::FindDisjointPackets (VehiclePathVectorHeader list)
{
  NS_LOG_FUNCTION (this << list);
  VehiclePathVectorHeader sm (std::min (m_map.size (), list.Size ()));
  for (PacketIdMap::iterator i = m_map.begin (); i != m_map.end (); ++i)
    {
      if (!list.Contains (i->first))
        {
          sm.Add (i->first);
        }
    }
  return sm;
}


void
PacketQueue::DropExpiredPackets ()
{
  NS_LOG_FUNCTION (this );
  Purge (true);
}

} //end namespace UrbanRouting
} //end namespace ns3
