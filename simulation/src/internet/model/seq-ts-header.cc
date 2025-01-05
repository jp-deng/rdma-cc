/* -*- Mode:C++; c-file-style:"gnu"; indent-tabs-mode:nil; -*- */
/*
 * Copyright (c) 2009 INRIA
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License version 2 as
 * published by the Free Software Foundation;
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
 *
 * Author: Mathieu Lacage <mathieu.lacage@sophia.inria.fr>
 */

#include "ns3/assert.h"
#include "ns3/log.h"
#include "ns3/header.h"
#include "ns3/simulator.h"
#include "seq-ts-header.h"

NS_LOG_COMPONENT_DEFINE("SeqTsHeader");

namespace ns3
{

  NS_OBJECT_ENSURE_REGISTERED(SeqTsHeader);

  SeqTsHeader::SeqTsHeader()
      : m_seq(0)
  {
    if (IntHeader::mode == 1)
      ih.ts = Simulator::Now().GetTimeStep();
  }

  void
  SeqTsHeader::SetSeq(uint32_t seq)
  {
    m_seq = seq;
  }
  uint32_t
  SeqTsHeader::GetSeq(void) const
  {
    return m_seq;
  }

  void
  SeqTsHeader::SetPG(uint16_t pg)
  {
    m_pg = pg;
  }
  uint16_t
  SeqTsHeader::GetPG(void) const
  {
    return m_pg;
  }

  Time
  SeqTsHeader::GetTs(void) const
  {
    NS_ASSERT_MSG(IntHeader::mode == 1, "SeqTsHeader cannot GetTs when IntHeader::mode != 1");
    return TimeStep(ih.ts);
  }

  void SeqTsHeader::SetSynchronise(uint8_t sync)
  {
    m_synchronise = sync;
  }

  uint8_t SeqTsHeader::GetSynchronise(void) const
  {
    return m_synchronise;
  }

  void SeqTsHeader::SetReTx(uint8_t reTx)
  {
    m_ReTx = reTx;
  }

  uint8_t SeqTsHeader::GetReTx(void) const
  {
    return m_ReTx;
  }

    void SeqTsHeader::SetPathId(uint8_t _pathId) {
        pathId = _pathId;
    }
    void SeqTsHeader::SetPathSeq(uint32_t _pathSeq) {
        pathSeq = _pathSeq;
    }
    uint8_t SeqTsHeader::GetPathId() const {
        return pathId;
    }
    uint32_t SeqTsHeader::GetPathSeq() const {
        return pathSeq;
    }

  TypeId
  SeqTsHeader::GetTypeId(void)
  {
    static TypeId tid = TypeId("ns3::SeqTsHeader")
                            .SetParent<Header>()
                            .AddConstructor<SeqTsHeader>();
    return tid;
  }
  TypeId
  SeqTsHeader::GetInstanceTypeId(void) const
  {
    return GetTypeId();
  }
  void
  SeqTsHeader::Print(std::ostream &os) const
  {
    // os << "(seq=" << m_seq << " time=" << TimeStep (m_ts).GetSeconds () << ")";
    // os << m_seq << " " << TimeStep (m_ts).GetSeconds () << " " << m_pg;
    os << m_seq << " " << m_pg;
  }
  uint32_t
  SeqTsHeader::GetSerializedSize(void) const
  {
    return GetHeaderSize();
  }
  uint32_t SeqTsHeader::GetHeaderSize(void)
  {
    return 6 + 2 + 5 + IntHeader::GetStaticSize();
  }

  void
  SeqTsHeader::Serialize(Buffer::Iterator start) const
  {
    Buffer::Iterator i = start;
    i.WriteHtonU32(m_seq);
    i.WriteHtonU16(m_pg);
    i.WriteU8(m_synchronise);
    i.WriteU8(m_ReTx);
        i.WriteU8(pathId);
        i.WriteU32(pathSeq);

    // write IntHeader
    ih.Serialize(i);
  }
  uint32_t
  SeqTsHeader::Deserialize(Buffer::Iterator start)
  {
    Buffer::Iterator i = start;
    m_seq = i.ReadNtohU32();
    m_pg = i.ReadNtohU16();
    m_synchronise = i.ReadU8();
    m_ReTx = i.ReadU8();
        pathId = i.ReadU8();
        pathSeq = i.ReadU32();
    // read IntHeader
    ih.Deserialize(i);

    return GetSerializedSize();
  }

} // namespace ns3