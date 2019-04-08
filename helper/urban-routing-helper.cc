/* -*- Mode:C++; c-file-style:"gnu"; indent-tabs-mode:nil; -*- */

#include "urban-routing-helper.h"
#include "ns3/urban-routing.h"


namespace ns3 {

    NS_LOG_COMPONENT_DEFINE ("UrbanRoutingHelper");

    UrbanRoutingHelper::~UrbanRoutingHelper ()
    {
        NS_LOG_FUNCTION (this);
    }

    UrbanRoutingHelper::UrbanRoutingHelper () : Ipv4RoutingHelper ()
    {
        NS_LOG_FUNCTION (this);
        m_agentFactory.SetTypeId ("ns3::UrbanRouting::RoutingProtocol");
    }

    UrbanRoutingHelper* UrbanRoutingHelper::Copy (void) const
    {
        NS_LOG_FUNCTION (this);
        return new UrbanRoutingHelper (*this);
    }

    Ptr<Ipv4RoutingProtocol> UrbanRoutingHelper::Create (Ptr<Node> node) const
    {
        NS_LOG_FUNCTION (this << node);
        Ptr<UrbanRouting::RoutingProtocol>
                agent = m_agentFactory.Create<UrbanRouting::RoutingProtocol> ();
        node->AggregateObject (agent);
        return agent;
    }

    void UrbanRoutingHelper::Set (std::string name, const AttributeValue &value)
    {
        NS_LOG_FUNCTION (this << name);
        m_agentFactory.Set (name, value);
    }



}

