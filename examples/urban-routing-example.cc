/* -*- Mode:C++; c-file-style:"gnu"; indent-tabs-mode:nil; -*- */

#include "ns3/core-module.h"
#include "ns3/network-module.h"
#include "ns3/applications-module.h"
#include "ns3/mobility-module.h"
#include "ns3/wifi-module.h"
#include "ns3/internet-module.h"
#include "ns3/urban-routing-helper.h"

using namespace ns3;


NS_LOG_COMPONENT_DEFINE ("UrbanRoutingExample");

int
main(int argc, char *argv[]) {
    // General parameters
    std::string mobility_model = "Grid";  // Grid or RandomWaypoint
    uint32_t nWifis = 10;
    double txpDistance = 120.0;
    double nodeSpeed = 50.0;
    bool app_logging = true;
    NodeContainer nodeContainer;
    NetDeviceContainer devices;


    // UrbanRouting parameters
    uint32_t UrbanRoutingHopCount = 50;
    uint32_t UrbanRoutingQueueLength = 50;
    Time UrbanRoutingQueueEntryExpireTime = Seconds (100);
    Time UrbanRoutingBeaconInterval = Seconds (1);

    // Application parameters
    std::string rate = "0.512kbps";
    uint32_t packetSize = 64;
    double appTotalTime = 100.0;
    double appDataStart = 10.0;
    double appDataEnd = 15;
    uint32_t source_num = 0;
    uint32_t sink_num = 1;

    /*
    Allow users to override the default parameters and set it to
    new ones from CommandLine.
    */
    CommandLine cmd;
    cmd.Usage ("Simple example shows basic UrbanRouting routing scenario.  "
               "This example creates an N-node wireless network, which is set by "
               "default to 10 nodes.  The mobility model can be either static Grid "
               "or Randomwaypoint, which by default is selected to be Grid.  For "
               "the static grid, nodes are placed in a grid of node with 100 m distance."
               "For the Randomwaypoint, the initial positions are randomly uniformly "
               "distributed within an area of 300x1500 m.The data traffic is generated "
               "using OnOff application and received by PacketSink. There is one source "
               "and one sink in this configuration. The example runs for 100 seconds, "
               "and data is sent from time 10 to 15 seconds, with the extra time in "
               "the example allocated to allow the UrbanRouting routing to eventually "
               "deliver the packets.\n");
    cmd.AddValue ("nWifis", "Number of wifi nodes", nWifis);
    cmd.AddValue ("txpDistance", "Specify node's transmit range", txpDistance);
    cmd.AddValue ("Source", "specify Source traffic node", source_num);
    cmd.AddValue ("Sink", "specify SINK traffic node", sink_num);
    cmd.AddValue ("rate", "CBR traffic rate(in kbps)", rate);
    cmd.AddValue ("packetSize", "The packet size", packetSize);
    cmd.AddValue ("nodeSpeed", "Node speed in RandomWayPoint model", nodeSpeed);
    cmd.AddValue ("Hop Count", "number of hops before a packet is dropped",
                  UrbanRoutingHopCount);
    cmd.AddValue ("QueueLength", "Specify queue Length", UrbanRoutingQueueLength);
    cmd.AddValue ("QueueEntryExpireTime", "Specify queue Entry Expire Time",
                  UrbanRoutingQueueEntryExpireTime);
    cmd.AddValue ("BeaconInterval", "Specify beaconInterval",
                  UrbanRoutingBeaconInterval);
    cmd.Parse (argc, argv);




    if (source_num >= nWifis)
    {
        std::cerr << "Source number can not exceed number of nodes" << std::endl;
        exit (-1);
    }

    if (sink_num >= nWifis || source_num >= nWifis)
    {
        std::cerr << "Sink number can not exceed number of nodes" << std::endl;
        exit (-1);
    }



    std::cout << "Number of wifi nodes: " << nWifis << std::endl;
    std::cout << "Source number: " << source_num << std::endl;
    std::cout << "Sink number: " << sink_num << std::endl;
    std::cout << "Node speed: " << nodeSpeed << " m/s" << std::endl;
    std::cout << "Packet size: " << packetSize << " b" << std::endl;
    std::cout << "Transmission distance: " << txpDistance << " m" << std::endl;
    std::cout << "Hop count: " << UrbanRoutingHopCount << std::endl;
    std::cout << "Queue length: " << UrbanRoutingQueueLength << " packets"
              << std::endl;
    std::cout << "Queue entry expire time: " <<
              UrbanRoutingQueueEntryExpireTime.GetSeconds () << " s" << std::endl;
    std::cout << "Beacon interval: " << UrbanRoutingBeaconInterval.GetSeconds ()
              << " s" << std::endl;


    /*
     *       Enabling OnOffApplication and PacketSink logging
     */
    if (app_logging)
    {
        LogComponentEnable ("OnOffApplication", LOG_LEVEL_INFO);
        LogComponentEnable ("PacketSink", LOG_LEVEL_INFO);
        LogComponentEnable ("UrbanRoutingRoutingProtocol", LOG_LEVEL_INFO);
        LogComponentEnableAll (LOG_PREFIX_TIME);
        LogComponentEnableAll (LOG_PREFIX_NODE);
        LogComponentEnableAll (LOG_PREFIX_FUNC);
    }



    LogComponentEnable ("UrbanRoutingExample", LOG_LEVEL_ALL);
    nodeContainer.Create (nWifis);


    /*
     *       Mobility model Setup
     */
    MobilityHelper mobility;
    if (mobility_model == "Grid")
    {
        int internode_distance = 100;
        Ptr<GridPositionAllocator> positionAlloc;
        positionAlloc = CreateObject<GridPositionAllocator> ();
        positionAlloc->SetDeltaX (internode_distance);
        mobility.SetPositionAllocator (positionAlloc);

    }
    else if (mobility_model == "RandomWaypoint")
    {

        /*
         *  Nodes initial positions and mobility bounds are based on
         *  original paper.
         *  See Docs for more details.
         */
        ObjectFactory pos;
        mobility.SetPositionAllocator ("ns3::RandomRectanglePositionAllocator",
                                       "X", StringValue ("ns3::UniformRandomVariable[Min=0.0|Max=300.0]"),
                                       "Y", StringValue ("ns3::UniformRandomVariable[Min=0.0|Max=1500.0]"));

        mobility.SetMobilityModel ("ns3::SteadyStateRandomWaypointMobilityModel",
                                   "MinSpeed", DoubleValue (0.01),
                                   "MaxSpeed", DoubleValue (nodeSpeed),
                                   "MinX", DoubleValue (0.0),
                                   "MaxX", DoubleValue (300.0),
                                   "MinPause", DoubleValue (10),
                                   "MaxPause", DoubleValue (20),
                                   "MinY", DoubleValue (0.0),
                                   "MaxY", DoubleValue (1500.0)
        );
    }
    mobility.Install (nodeContainer);


    /*
     *       Physical and link Layers Setup
     */

    WifiMacHelper wifiMac;
    wifiMac.SetType ("ns3::AdhocWifiMac");
    YansWifiPhyHelper wifiPhy = YansWifiPhyHelper::Default ();
    YansWifiChannelHelper wifiChannel = YansWifiChannelHelper::Default ();

    wifiChannel.AddPropagationLoss ("ns3::RangePropagationLossModel",
                                    "MaxRange", DoubleValue (txpDistance));
    wifiPhy.SetChannel (wifiChannel.Create ());
    WifiHelper wifi;
    wifi.SetRemoteStationManager ("ns3::ConstantRateWifiManager",
                                  "DataMode", StringValue ("OfdmRate6Mbps"),
                                  "RtsCtsThreshold", UintegerValue (0));
    devices = wifi.Install (wifiPhy, wifiMac, nodeContainer);

    /*
     *       UrbanRouting Routing Setup
     */
    UrbanRoutingHelper UrbanRouting;
    UrbanRouting.Set ("HopCount", UintegerValue (UrbanRoutingHopCount));
    UrbanRouting.Set ("QueueLength", UintegerValue (UrbanRoutingQueueLength));
    UrbanRouting.Set ("QueueEntryExpireTime",
                  TimeValue (UrbanRoutingQueueEntryExpireTime));
    UrbanRouting.Set ("BeaconInterval", TimeValue (UrbanRoutingBeaconInterval));

    /*
     *       Internet Stack Setup
     */
    Ipv4ListRoutingHelper list;
    InternetStackHelper internet;
    internet.SetRoutingHelper (UrbanRouting);
    internet.Install (nodeContainer);
    Ipv4AddressHelper ipv4;
    ipv4.SetBase ("10.1.1.0", "255.255.255.0");
    Ipv4InterfaceContainer interfaces = ipv4.Assign (devices);


    /*
     *         Application Setup
     */


    // Sink or server setup
    PacketSinkHelper sink ("ns3::UdpSocketFactory",
                           InetSocketAddress (Ipv4Address::GetAny (), 80));
    ApplicationContainer apps_sink = sink.Install (nodeContainer.Get (sink_num));
    apps_sink.Start (Seconds (0.0));
    apps_sink.Stop (Seconds (appTotalTime));


    // Client setup
    OnOffHelper onoff1 ("ns3::UdpSocketFactory",
                        Address (InetSocketAddress (interfaces.GetAddress (sink_num), 80)));
    onoff1.SetConstantRate (DataRate (rate));
    onoff1.SetAttribute ("PacketSize", UintegerValue (packetSize));
    ApplicationContainer apps1 = onoff1.Install (nodeContainer.Get (source_num));
    apps1.Start (Seconds (appDataStart));
    apps1.Stop (Seconds (appDataEnd));


    Simulator::Stop (Seconds (appTotalTime));
    Simulator::Run ();
    Simulator::Destroy ();
    return 0;

}


