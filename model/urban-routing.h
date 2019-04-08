/* -*- Mode:C++; c-file-style:"gnu"; indent-tabs-mode:nil; -*- */
#ifndef URBAN_ROUTING_PROTOCOL_H
#define URBAN_ROUTING_PROTOCOL_H

#include "urban-routing-packet-queue.h"
#include "urban-routing-packet.h"
#include "ns3/random-variable-stream.h"
#include "urban-routing-tag.h"
#include <vector>
#include "ns3/boolean.h"
#include "ns3/config.h"
#include "ns3/node.h"
#include "ns3/ipv4-routing-protocol.h"
#include "ns3/inet-socket-address.h"
#include "ns3/ipv4-interface.h"
#include "ns3/ipv4-l3-protocol.h"
#include "ns3/output-stream-wrapper.h"
#include "ns3/timer.h"
#include <iostream>
#include <algorithm>
#include <functional>
#include "ns3/ipv4-route.h"
#include "ns3/socket.h"
#include "ns3/log.h"


namespace ns3 {

    namespace UrbanRouting {
        class RoutingProtocol : public Ipv4RoutingProtocol
        {
        public:
            static TypeId GetTypeId (void);

            static const uint32_t URBAN_ROUTING_PORT = 269;
            RoutingProtocol ();
            virtual  ~RoutingProtocol ();
            virtual void  DoDispose ();
            Ptr<Ipv4Route> RouteOutput (Ptr<Packet> p, const Ipv4Header &header,
                                        Ptr<NetDevice> oif, Socket::SocketErrno &sockerr);
            bool RouteInput (Ptr<const Packet> p, const Ipv4Header &header,
                             Ptr<const NetDevice> idev, UnicastForwardCallback ucb,
                             MulticastForwardCallback mcb,
                             LocalDeliverCallback lcb, ErrorCallback ecb);
            virtual void PrintRoutingTable (Ptr<OutputStreamWrapper> stream, Time::Unit unit = Time::S) const;
            virtual void NotifyInterfaceUp (uint32_t interface);
            virtual void NotifyInterfaceDown (uint32_t interface);
            virtual void NotifyAddAddress (uint32_t interface, Ipv4InterfaceAddress address);
            virtual void NotifyRemoveAddress (uint32_t interface, Ipv4InterfaceAddress address);
            virtual void SetIpv4 (Ptr<Ipv4> ipv4);

        private:
            /// Main IP address for the current node
            Ipv4Address m_mainAddress;
            /// Number of times a packet is resent
            uint32_t m_hopCount;
            /// Maximum number of packets a queue can hold
            uint32_t m_maxQueueLen;
            /// Time in seconds after which the packet will expire in the queue
            Time m_queueEntryExpireTime;
            /// Time in seconds for sending periodic beacon packets
            Time m_beaconInterval;
            /// Time in seconds for host recent period, in which hosts can not
            // re-exchange summary vectors
            Time m_hostRecentPeriod;
            /// Upper bound of the uniform distribution random time added
            // to avoid collisions. Measured in milliseconds
            uint32_t m_beaconMaxJitterMs;
            /// Local counter for data packets
            uint16_t m_dataPacketCounter;
            /// A pointer to the Ipv4 for the current node
            Ptr<Ipv4> m_ipv4;
            /// A map between opened sockets and IP addresses
            std::map<Ptr<Socket>, Ipv4InterfaceAddress> m_socketAddresses;
            /// queue associated with a node
            PacketQueue m_queue;
            /// timer for sending beacons
            Timer m_beaconTimer;
            /// uniform random variable to be added to beacon intervals
            // to avoid collisions
            Ptr<UniformRandomVariable> m_beaconJitter;
            ///  Type to connect a host address to recent contact time value
            typedef std::map<Ipv4Address, Time> HostContactMap;
            /// Pair representing host address and time value
            typedef HostContactMap::value_type   HostContactMapPair;
            /// Hash table to store recent contact time for nodes
            HostContactMap m_hostContactTime;



            void Start ();
            void RecvUrbanRouting (Ptr<Socket> socket);
            void SendDisjointPackets (SummaryVectorHeader packet_SMV, Ipv4Address dest);
            void SendBeacons ();
            uint32_t FindOutputDeviceForAddress ( Ipv4Address  dst);
            uint32_t FindLoopbackDevice ();
            void SendPacket (Ptr<Packet> p,InetSocketAddress addr);
            bool IsMyOwnAddress (Ipv4Address src);
            void BroadcastPacket (Ptr<Packet> p);
            void SendSummaryVector (Ipv4Address dest,bool firstNode);
            Ptr<Socket> FindSocketWithInterfaceAddress (
                    Ipv4InterfaceAddress iface) const;
            void SendPacketFromQueue (Ipv4Address dst,QueueEntry queueEntry);
            bool IsHostContactedRecently (Ipv4Address hostID);


        };

    }

}

#endif /* URBAN_ROUTING_H */

