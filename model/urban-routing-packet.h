/* -*- Mode:C++; c-file-style:"gnu"; indent-tabs-mode:nil; -*- */
#ifndef URBAN_ROUTING_PACKET_H
#define URBAN_ROUTING_PACKET_H


#include <iostream>
#include "ns3/header.h"
#include "ns3/ipv4-address.h"
#include "ns3/nstime.h"
#include "algorithm"

/**
 * \file
 * \ingroup UrbanRouting
 * ns3::UrbanRouting::TypeHeader, ns3::UrbanRouting::SummaryVectorHeader
 * and ns3::UrbanRouting::UrbanRoutingHeader declarations.
 */

namespace ns3 {
namespace UrbanRouting {



/**
 * \ingroup UrbanRouting
 * \brief  UrbanRouting routing packet type header.
 *
 * UrbanRouting routing packets come in three types:
 *
 * 1. Beacon Packet: it is used to advertise the presence of a node
 *    in the network.
 * 2. Reply Packet: once a beacon packet is received, it starts
 *    the anti-entropy session.
 *    1.  Packet with smaller network ID (i.e. IP) will send a reply packet,
 *        which contains summary vector of all the packet IDs in its buffer.
 * 3. Reply Back Packet: once a reply packet is received,
 *    the receiver determines the disjoint packets between its buffer
 *    and the received summary vector. Then, it sends the disjoint
 *    packets the other node. After that, it sends a reply back packet
 *    containing a summary vector of all the packet IDs in its buffer
 *    so the other host sends the disjoint packets as well.
 *
  \verbatim
   0
   0 1 2 3 4 5 6 7
   +-+-+-+-+-+-+-+-+
   |     Type      |
   +-+-+-+-+-+-+-+-+
  \endverbatim
*/
class TypeHeader : public Header
{
public:
  /// MessageType enum, several types for UrbanRouting control packets
  enum MessageType
  {
    BEACON,     //!< Advertise the presence of a node
    REPLY,      //!< Reply to a beacon, with the packet Id summary vector
    REPLY_BACK, //!< Response to a Reply packet, as list of disjoint packets.

  };

  /**
   * \brief Constructor.
   * \param t Header message type.
   */
  TypeHeader (MessageType t = BEACON);
  /**
   * \brief Destructor.
   */
  ~TypeHeader ();
  /**
   *  Get the registered TypeId for this class.
   *  \return The object TypeId.
   */
  static TypeId GetTypeId ();
  /**
   * \brief Set the instance type ID.
   * \param type message type to be set.
   */
  void SetMessageType (MessageType type);
  // Inherited
  TypeId GetInstanceTypeId () const;
  uint32_t GetSerializedSize () const;
  void Serialize (Buffer::Iterator start) const;
  uint32_t Deserialize (Buffer::Iterator start);
  void Print (std::ostream &os) const;

  /// \returns The message type.
  MessageType GetMessageType () const;
  /**
   *  Check that this is a message of the expected type.
   *
   * \param type The expected message type.
   * \return true if \p type matches the MessageType of this TypeHeader
   */
  bool IsMessageType (const MessageType type) const;
  /// \return true if the MessageType of this TypeHeader is valid.
  bool IsValid () const;
  /**
   * \brief Comparison operator
   * \param o header to compare
   * \return true if the headers are equal
   */
  bool operator== (TypeHeader const & o) const;
private:
  /// message type
  MessageType m_type;
  /**
  Valid flag: \c true if the message deserialized correctly.
  otherwise \c false.
  */
  bool m_valid;
};

/**
  * \brief Stream output operator
  * \param os output stream
  * \return updated stream
  */
std::ostream & operator<< (std::ostream & os, TypeHeader const & h);


/**
* \ingroup UrbanRouting
* \brief    UrbanRouting Summary Vector Header
*  This packet is used to carry the packet IDs of packets located
*  in the host's buffer to the other node.
  \verbatim
  0                   1                   2                   3
  0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
  +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
  |                   32 bit Summary Vector Length                |
  +                                                               +
  |                                                               |
  +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
  |                   32 bit Global ID for Packet # 1             |
  +                                                               +
  |                                                               |
  +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
  |                   32 bit Global ID for Packet # 2             |
  |                                                               |
  |                              .                                |
  |                              .                                |
  |                              .                                |
  |                                                               |
  +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
  |                   32 bit Global ID for Packet # n             |
  +                                                               +
  |                                                               |
  +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
  \endverbatim
*/


class SummaryVectorHeader : public Header
{
public:
  /**
  * \brief Constructor.
  */
  SummaryVectorHeader (size_t size2 = 0);
  /**
   * \brief Destructor.
   */
  virtual ~SummaryVectorHeader ();
  /**
   * \return The object TypeId.
   */
  static TypeId GetTypeId (void);
  // Inherited
  virtual TypeId GetInstanceTypeId (void) const;
  virtual uint32_t GetSerializedSize () const;
  virtual void Serialize (Buffer::Iterator start) const;
  virtual uint32_t Deserialize (Buffer::Iterator start);
  virtual void Print (std::ostream &os) const;


  /**
   * Add a global packet id.
   *
   * \param pkt_ID The global packet id to add.
   */
  void Add (const uint32_t pkt_ID);
  /**
   * Check for a global packet id.
   *
   * \param pkt_ID The global packet id to check for.
   * \return True if the packet is in this summary vector.
   */
  bool Contains (const uint32_t pkt_ID) const;
  /**
   * Get the number of entries.
   *
   * \return The number of global packet IDs in this header.
   */
  size_t Size (void) const;

private:
  /**
   * A vector to store packet IDs.
   */
  std::vector<uint32_t> m_packets;

  // RoutingProtocol::SendDisjointPackets
  // needs to iterate through the vector
  friend class RoutingProtocol;

};

/**
 * \ingroup UrbanRouting
 * \brief Output streamer for UrbanRoutingSummaryVectorHeader.
 *
 * \param os The stream.
 * \param packet The UrbanRoutingSummaryVectorHeader.
 * \returns The stream.
 */

std::ostream &operator<< (std::ostream& os,
                          const SummaryVectorHeader & packet);

/**
 * \ingroup UrbanRouting
 * \brief UrbanRouting Summary Vector Header
 *
 *  This packet header is added to a data packet in the source node once it is
 *  received from the transport layer. It is removed in the receiver node
 *  before it is delivered to the transport layer.
 *  The UrbanRouting Header consists of three fields:
 *
 *  1. Packet ID:  global packet ID
 *
 *     The format of a global packet ID is a concatenation of 16 bit sender IP
 *     and a 16 bit sender data packet counter.  We call the packet ID global
 *     packet ID to distinguish from the ns3 packet id.
 *
 *         16 bit    : 16 Bit
 *         SENDER IP : SENDER PACKET COUNTER
 *  2. Hop Count:
 *
 *     It is flood control parameter used to set the number of hops
 *     the packet can travel before it is discarded. It is similar to TTL
 *     field but with higher size limit.
 *  3. Timestamp:
 *
 *     It show when the packet is generated.  This field is used
 *     to discard old packets with a time threshold limit set by the user.
 *
 *  The complete header is formatted as follows:
  \verbatim
  0                   1                   2                   3
  0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
  +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
  |                         Packet ID                             |
  +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
  |                         Hop Count                             |
  +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
  |                     64 Bit Timestamp                          |
  |                                                               |
  +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
  \endverbatim
 */
class UrbanRoutingHeader : public Header
{
public:
  /**
   * \brief Destructor.
   */
  virtual ~UrbanRoutingHeader ();
  /**
   *  \brief Get the registered TypeId for this class.
   *  \return The object TypeId.
   */
  static TypeId GetTypeId (void);
  // Inherited
  virtual TypeId GetInstanceTypeId (void) const;
  virtual uint32_t GetSerializedSize () const;
  virtual void Serialize (Buffer::Iterator start) const;
  virtual uint32_t Deserialize (Buffer::Iterator start);
  virtual void Print (std::ostream &os) const;
  /**
   * \brief Set Packet ID for current packet
   */
  void SetPacketID (uint32_t pktID);
  /**
   * \brief Get Packet ID for current packet
   * \return packet ID
   */
  uint32_t GetPacketID  () const;

  /**
   * \brief Set Hop count for current packet
   */
  void SetHopCount (uint32_t floodCount);
  /**
   * \brief Get Hop count for current packet
   * \return hop count
   */
  uint32_t GetHopCount () const;

  /**
   * \brief Set Timestamp current packet
   */
  void SetTimeStamp (Time timeStamp);

  /**
   * \brief Get Timestamp for current packet
   * \return timestamp
   */
  Time GetTimeStamp () const;



private:
  uint32_t m_packetID;      ///< global packet ID
  uint32_t m_hopCount;      ///< Count to keep track of number of traveled hops
  Time m_timeStamp;         ///< Time at which packet was originated


};
/**
 * \ingroup UrbanRouting
 * \brief Output streamer for UrbanRoutingHeader.
 *
 * \param os The stream.
 * \param header The UrbanRoutingHeader.
 * \returns The stream.
 */

std::ostream &operator<< (std::ostream& os,
                          const UrbanRoutingHeader & header);

} //end namespace UrbanRouting
} //end namespace ns3
#endif
