/* -*- Mode:C++; c-file-style:"gnu"; indent-tabs-mode:nil; -*- */
#ifndef URBANROUTING_TAG_H
#define URBANROUTING_TAG_H


#include <iostream>
#include "ns3/log.h"
#include "ns3/tag.h"


namespace ns3 {
namespace UrbanRouting {


/**
 * Tag used by UrbanRouting implementation
 *  \ingroup UrbanRouting
 *  Tag used to differentiate between locally generated packets
 *  and incoming packets in RoutingProtocol::RouteInput() function.
 */
class ControlTag : public Tag
{

public:
  /// TagType enum, two types for UrbanRouting tags
  enum TagType
  {
    CONTROL,           //!< Tagged as control message
    NOT_SET,           //!< Tag is not set
  };

  /// Constructor
  ControlTag (TagType o = NOT_SET) : Tag (),
                                     m_tag (o)
  {
  }

  /**
   *  Get the registered TypeId for this class.
   *  \return The object TypeId.
   */
  static TypeId GetTypeId ();
  // Inherited
  TypeId  GetInstanceTypeId () const;

  /// \returns control tag type
  TagType GetTagType () const;

  /**
   * Check if this ControlTag is of the indicated TagType.
   *
   * \param type The expected TagType
   * \returns true if \p type matches the TagType of this ControlTag.
   */
  bool IsTagType (const TagType type) const;



  /**
   * \brief Seting UrbanRouting tag.
   * \param tag TagType to be set.
   */
  void SetTagType (const TagType tag);
  // Inherited
  uint32_t GetSerializedSize () const;
  void  Serialize (TagBuffer i) const;
  void  Deserialize (TagBuffer i);
  void  Print (std::ostream &os) const;

private:
  /// UrbanRouting tag
  TagType m_tag;
};





} //end namespace UrbanRouting
} //end namespace ns3
#endif
