/* -*- Mode:C++; c-file-style:"gnu"; indent-tabs-mode:nil; -*- */
#ifndef URBAN_ROUTING_PACKET_QUEUE_H
#define URBAN_ROUTING_PACKET_QUEUE_H


#include <vector>
#include "ns3/ipv4-routing-protocol.h"
#include "ns3/simulator.h"
#include <string.h>
#include <sstream>


/**
 * \file
 * \ingroup UrbanRouting
 * ns3::UrbanRouting::QueueEntry and ns3::UrbanRouting::PacketQueue declarations.
 */

namespace ns3 {
namespace UrbanRouting {

/**
 * \ingroup UrbanRouting
 * \brief UrbanRouting Queue Entry
 */
class QueueEntry
{
public:
  /// Class local synonym for ns3::Ipv4RoutingProtocol::UnicastForwardCallback
  typedef Ipv4RoutingProtocol::UnicastForwardCallback UnicastForwardCallback;
  /// Class local synonym for ns3::Ipv4RoutingProtocol::ErrorCallback
  typedef Ipv4RoutingProtocol::ErrorCallback ErrorCallback;
  /**
   * \brief Constructor for QueueEntry
   * \param pa the queued packet.
   * \param h the corresponding Ipv4Header to the queued packet.
   * \param ecb the corresponding ErrorCallback to the queued packet.
   * \param exp the expiration time of the queued packet entry.
   * \param packetID the packet ID of the queued packet.
   */
  QueueEntry (void);
  QueueEntry (Ptr<const Packet> pa,
              Ipv4Header const & h,
              UnicastForwardCallback ucb,
              ErrorCallback ecb,
              Time exp = Simulator::Now (),
              uint32_t packetID = 0);
  /**
   * \brief Comparison operator
   * \param o QueueEntry to compare
   * \return true if the packet IDs of the two entries are equal
   */
  bool operator== (QueueEntry const & o) const;
  /// \returns the UnicastForwardCallback associated with the queued packet
  UnicastForwardCallback GetUnicastForwardCallback () const;
  /// Set the UnicastForwardCallback \param ucb associated with the queued packet
  void SetUnicastForwardCallback (UnicastForwardCallback ucb);
  /// \returns the ErrorCallback associated with the queued packet
  ErrorCallback GetErrorCallback () const;
  /// Set the ErrorCallback \param ucb associated with the queued packet
  void SetErrorCallback (ErrorCallback ecb);
  /// \returns the queued packet
  Ptr<const Packet> GetPacket () const;
  /// Set the packet pointer \param p
  void SetPacket (Ptr<const Packet> p);
  /// \returns the Ipv4Header associated with the queued packet
  Ipv4Header GetIpv4Header () const;
  /// Set the Ipv4Header associated with the queued packet
  void SetIpv4Header (Ipv4Header h);
  /// Set the ExpireTime \param exp associated with the queued packet
  void SetExpireTime (Time exp);
  /// \returns the ExpireTime associated with the queued packet
  Time GetExpireTime () const;
  /// \returns the PacketID associated with the queued packet
  uint32_t GetPacketID () const;
  /// Set the PacketID \param id associated with the queued packet
  void SetPacketID (uint32_t id);

private:
  /// queued packet
  Ptr<const Packet> m_packet;
  /// IP header
  Ipv4Header m_header;
  /// Unicast forward callback
  UnicastForwardCallback m_ucb;
  /// Error callback
  ErrorCallback m_ecb;
  /// Expire time for queue entry
  Time m_expire;
  /// Global packet ID
  uint32_t m_packetID;
};


// Forward declaration
class SummaryVectorHeader;

/**
 * \ingroup UrbanRouting
 * \brief UrbanRouting queue
 * This queue contains UrbanRouting packets.
 */
class PacketQueue
{
public:
  /**
   * \brief Constructor for PacketQueue
   * \param maxLen maximum length of the queue
   */
  PacketQueue (uint32_t maxLen = 0);
  /**
   * \brief Push entry in queue mapped with the its packet ID.
   *  If it already exists, update it.
   * \param entry contains a packet ID
   * \returns true if the entry  is successfully added.
   */
  bool Enqueue (QueueEntry & entry);
  /**
   * \brief remove entry in queue mapped with the its packet ID.
   * \param entry contains a packet ID
   * \returns true if the entry  is successfully removed.
   */
  bool Dequeue (QueueEntry & entry);
  /// \returns number of entries
  uint32_t GetSize ();
  /// \returns the maximum queue length
  uint32_t GetMaxQueueLen () const;
  /**
   * \brief set the maximum queue length.
   * \param len contains maximum queue length.
   */
  void SetMaxQueueLen (uint32_t len);
  /// \returns the queue timeout for each entry
  Time GetQueueTimeout () const;
  /**
   * \brief Set the queue timeout for each entry.
   * \param t timeout
   */
  void SetQueueTimeout (Time t);

  /**
   * \brief Find a packet in the UrbanRouting queue based on the packetID.
   *  If not found, return and empty QueueEntry
   * \param packetID packet ID for the target packet
   * \returns the found QueueEntry
   */
  QueueEntry  Find (uint32_t packetID);
  /// \returns the summary vector of a current node's buffer
  SummaryVectorHeader GetSummaryVector ();
  /**
   * \brief Returns a summary vector that contains
   *  the disjoint packets between the given list and current buffer
   * \param list a list of compared packet IDs
   * \returns the summary vector of the disjoint packets
   */
  SummaryVectorHeader FindDisjointPackets (SummaryVectorHeader list);
  /// Drop expired packet in the current node's buffer
  void DropExpiredPackets ();

private:
  ///  Type to connect a global Packet id to a QueueEntry
  typedef std::map<uint32_t, QueueEntry> PacketIdMap;
  /// Pair representing a global Packet Id and a QueueEntry
  typedef PacketIdMap::value_type        PacketIdMapPair;
  /// Map to store queue entries based on the packetID
  PacketIdMap m_map;
  /// Compare two QueueEntry's by expire time.
  static bool IsEarlier (const PacketIdMapPair & e1,
                         const PacketIdMapPair & e2);
  /**
   * \brief Remove all expired entries.
   * \param outdated if True, remove the outdated entries.
   */
  void Purge (bool outdated /* = false */);

  /**
   * \brief Drop a packet and log the reason.
   * \param en the packet to be dropped.
   * \param reason the reason for dropping the packet.
   */
  void Drop (PacketIdMap::iterator en, std::string reason);
  /// The maximum number of packets that we allow a routing protocol to buffer.
  uint32_t m_maxLen;


};
} //end namespace UrbanRouting
} //end namespace ns3
#endif
