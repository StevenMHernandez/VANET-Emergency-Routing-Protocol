/* -*- Mode:C++; c-file-style:"gnu"; indent-tabs-mode:nil; -*- */
#include "urban-routing-packet.h"
#include "urban-routing-tag.h"
#include "ns3/address-utils.h"
#include "ns3/log.h"
#include "ns3/packet.h"

namespace ns3 {
namespace UrbanRouting {

NS_OBJECT_ENSURE_REGISTERED (ControlTag);

/// Get TypeId
TypeId ControlTag::GetTypeId ()
{
  static TypeId tid = TypeId ("ns3::UrbanRouting::ControlTag")
    .SetParent<Tag> ()
    .AddConstructor<ControlTag> ()
  ;
  return tid;
}


/// Get instanceTypeId
TypeId  ControlTag::GetInstanceTypeId () const
{
  return GetTypeId ();
}

/// Get UrbanRouting tag
ControlTag::TagType ControlTag::GetTagType () const
{
  return m_tag;
}

bool
ControlTag::IsTagType (const TagType type) const
{
  return m_tag == type;
}

/// Set UrbanRouting tag
void
ControlTag::SetTagType (const TagType tag)
{
  m_tag = tag;
}

/// Get size
uint32_t ControlTag::GetSerializedSize () const
{
  return sizeof(uint8_t);
}


/// Serialize
void  ControlTag::Serialize (TagBuffer i) const
{
  i.WriteU8 ((uint8_t) m_tag);
}



///Deserialize
void  ControlTag::Deserialize (TagBuffer i)
{
  uint8_t type = i.ReadU8 ();
  switch (type)
    {
    case CONTROL:
    case NOT_SET:
      {
        m_tag = (TagType) type;
        break;
      }
    default:
      break;
    }

}
/// Print
void  ControlTag::Print (std::ostream &os) const
{
  os << "ControlTag:" << m_tag;
}

} //end namespace UrbanRouting
} //end namespace ns3
