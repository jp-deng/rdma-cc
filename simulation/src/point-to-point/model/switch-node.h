#ifndef SWITCH_NODE_H
#define SWITCH_NODE_H

#include <unordered_map>
#include <unordered_set>
#include <ns3/node.h>
#include "qbb-net-device.h"
#include "switch-mmu.h"
#include "pint.h"

namespace ns3 {

class Packet;

class SwitchNode : public Node{
public:    
	static const uint32_t pCnt = 257;	// Number of ports used
	static const uint32_t qCnt = 8;	// Number of queues/priorities used
	uint32_t m_ecmpSeed;
	std::unordered_map<uint32_t, std::vector<int> > m_rtTable; // map from ip address (u32) to possible ECMP port (index of dev)
	std::unordered_map<uint32_t, uint32_t> m_rtOpticalTable; // map from ip address (u32) to possible ECMP port (index of dev)
	std::unordered_map<uint32_t, uint32_t> m_rtMpOpticalTable; // map from ip address (u32) to possible ECMP port (index of dev)

	// monitor of PFC	
	uint64_t m_txBytes[pCnt]; // counter of tx bytes

	uint32_t m_lastPktSize[pCnt];
	uint64_t m_lastPktTs[pCnt]; // ns
	double m_u[pCnt];

protected:
	bool m_ecnEnabled;
	uint32_t m_ccMode;
	uint64_t m_maxRtt;

	uint32_t m_ackHighPrio; // set high priority for ACK/NACK

private:
	int GetOutDev(Ptr<const Packet>, CustomHeader &ch);
	int GetElecOutDev(CustomHeader &ch);
	void SendToDev(Ptr<Packet>p, CustomHeader &ch);
	static uint32_t EcmpHash(const uint8_t* key, size_t len, uint32_t seed);
	void CheckAndSendPfc(uint32_t inDev, uint32_t qIndex);
	void CheckAndSendResume(uint32_t inDev, uint32_t qIndex);
    void DoSwitchSend(Ptr<Packet> p, CustomHeader &ch, uint32_t idx, uint32_t qIndex);
    void SendToDevContinue(Ptr<Packet> p, CustomHeader &ch);    

public:
	Ptr<SwitchMmu> m_mmu;
    bool m_isToR;                                 // true if ToR switch
    std::unordered_set<uint32_t> m_isToR_hostIP;  // host's IP connected to this ToR
    uint32_t opticalPort = 0;

	static TypeId GetTypeId (void);
	SwitchNode();
	void SetEcmpSeed(uint32_t seed);
	void AddTableEntry(Ipv4Address &dstAddr, uint32_t intf_idx);
	void ClearTable();
	void AddOpticalTableEntry(Ipv4Address &dstAddr, uint32_t intf_idx);
	void ClearOpticalTableEntry(Ipv4Address &dstAddr);
	void AddMpOpticalTableEntry(Ipv4Address &dstAddr, uint32_t intf_idx);
	void ClearMpOpticalTableEntry();


	bool SwitchReceiveFromDevice(Ptr<NetDevice> device, Ptr<Packet> packet, CustomHeader &ch);
	void SwitchNotifyDequeue(uint32_t ifIndex, uint32_t qIndex, Ptr<Packet> p);

	// for approximate calc in PINT
	int logres_shift(int b, int l);
	int log2apprx(int x, int b, int m, int l); // given x of at most b bits, use most significant m bits of x, calc the result in l bits
};

} /* namespace ns3 */

#endif /* SWITCH_NODE_H */
