/* -*- Mode:C++; c-file-style:"gnu"; indent-tabs-mode:nil; -*- */
#ifndef URBAN_ROUTING_HELPER_H
#define URBAN_ROUTING_HELPER_H

#include "ns3/object-factory.h"
#include "ns3/node.h"
#include "ns3/node-container.h"
#include "ns3/ipv4-routing-helper.h"
//#include "ns3/urban-routing.h"

namespace ns3 {

class UrbanRoutingHelper : public Ipv4RoutingHelper {
public:
    UrbanRoutingHelper ();
    ~UrbanRoutingHelper ();
    UrbanRoutingHelper* Copy (void) const;
    virtual Ptr<Ipv4RoutingProtocol> Create (Ptr<Node> node) const;
    void Set (std::string name, const AttributeValue &value);
private:
    ObjectFactory m_agentFactory;
};

}

#endif /* URBAN_ROUTING_HELPER_H */

