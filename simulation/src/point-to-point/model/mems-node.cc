#include "ns3/ipv4.h"
#include "ns3/packet.h"
#include "ns3/ipv4-header.h"
#include "ns3/flow-id-tag.h"
#include "ns3/boolean.h"
#include "ns3/uinteger.h"
#include "ns3/double.h"
#include "ns3/path-id-tag.h"
#include "mems-node.h"
#include "mems-link-matrix.h"
#include "qbb-net-device.h"
#include <cmath>

namespace ns3 {

TypeId MemsNode::GetTypeId (void)
{
  static TypeId tid = TypeId ("ns3::MemsNode")
    .SetParent<Node> ()
    .AddConstructor<MemsNode> ();
  return tid;
}

MemsNode::MemsNode(){
	m_node_type = 2; 
}

MemsNode::MemsNode(uint32_t id){
	m_node_type = 2;
    m_memsId = id;
    m_linkIndex = m_memsId;
    m_linkMatrix.push_back(MATRIX_1);
    m_linkMatrix.push_back(MATRIX_2);
    m_linkMatrix.push_back(MATRIX_3);
    m_linkMatrix.push_back(MATRIX_4);
    m_linkMatrix.push_back(MATRIX_5);
    m_linkMatrix.push_back(MATRIX_6);
    m_linkMatrix.push_back(MATRIX_7);
    m_linkMatrix.push_back(MATRIX_8);
    m_linkMatrix.push_back(MATRIX_9);
    m_linkMatrix.push_back(MATRIX_10);
    m_linkMatrix.push_back(MATRIX_11);
    m_linkMatrix.push_back(MATRIX_12);
    m_linkMatrix.push_back(MATRIX_13);
    m_linkMatrix.push_back(MATRIX_14);
    m_linkMatrix.push_back(MATRIX_15);  
    m_linkTable.resize(16);
    for(int i = 0; i < 16; i++) {
        for(int j = 0; j < 16; j++) {
            if(m_linkMatrix[m_linkIndex][i][j]) {
                m_linkTable[i] = j;
            }
        }
    }
    m_isDay = true;
}

int MemsNode::GetOutDev(int indev){
    indev--;
    int outdev = m_linkTable[indev];
    outdev++;
    return outdev;
}


void MemsNode::SendToDev(int indev, Ptr<Packet> p){
	int idx = GetOutDev(indev);
    m_devices[idx]->MemsSend(p);
}


void MemsNode::Reconfiguration(){
    m_linkIndex = (m_linkIndex + 4) % 15;
    for(int i = 0; i < 16; i++) {
        for(int j = 0; j < 16; j++) {
            if(m_linkMatrix[m_linkIndex][i][j]) {
                m_linkTable[i] = j;
            }            
        }
    }    
}

bool MemsNode::SwitchReceiveFromDevice(Ptr<NetDevice> device, Ptr<Packet> packet, CustomHeader &ch){
	SendToDev(device->GetIfIndex(), packet);
	return true;
}


} /* namespace ns3 */
