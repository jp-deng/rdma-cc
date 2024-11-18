#ifndef MEMS_NODE_H
#define MEMS_NODE_H

#include <unordered_map>
#include <ns3/node.h>

namespace ns3 {

class Packet;

class MemsNode : public Node{
public:
    uint32_t m_memsId;
    uint32_t m_linkIndex;
    bool m_isDay;
	std::vector<std::vector<std::vector<uint32_t>> > m_linkMatrix;
    std::vector<uint32_t> m_linkTable;

	int GetOutDev(int indev);
	void SendToDev(int indev, Ptr<Packet> p);

	static TypeId GetTypeId (void);
	MemsNode();
    MemsNode(uint32_t id);
	void Reconfiguration();
	bool SwitchReceiveFromDevice(Ptr<NetDevice> device, Ptr<Packet> packet, CustomHeader &ch);
};

} /* namespace ns3 */

#endif /* SWITCH_NODE_H */
