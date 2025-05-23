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

#ifndef SEQ_TS_HEADER_H
#define SEQ_TS_HEADER_H

#include "ns3/header.h"
#include "ns3/nstime.h"
#include "ns3/int-header.h"

namespace ns3
{
  /**
   * \ingroup udpclientserver
   * \class SeqTsHeader
   * \brief Packet header for Udp client/server application
   * The header is made of a 32bits sequence number followed by
   * a 64bits time stamp.
   */
  class SeqTsHeader : public Header
  {
  public:
    SeqTsHeader();

    /**
     * \param seq the sequence number
     */
    void SetSeq(uint32_t seq);
    /**
     * \return the sequence number
     */
    uint32_t GetSeq(void) const;
    /**
     * \return the time stamp
     */
    Time GetTs(void) const;

    void SetPG(uint16_t pg);
    uint16_t GetPG() const;

    /**
     * \param sync the sync signal to the receiver
     */
    void SetSynchronise(uint8_t sync);
    uint8_t GetSynchronise(void) const;

    /**
     * \param reTx the retransmission signal from the receiver
     */
    void SetReTx(uint8_t reTx);
    uint8_t GetReTx(void) const;

    void SetPathId(uint8_t _pathId);
    void SetPathSeq(uint32_t _pathSeq);
    uint8_t GetPathId() const;
    uint32_t GetPathSeq() const;

    static TypeId GetTypeId(void);
    virtual TypeId GetInstanceTypeId(void) const;
    virtual void Print(std::ostream &os) const;
    virtual uint32_t GetSerializedSize(void) const;
    static uint32_t GetHeaderSize(void);

  private:
    virtual void Serialize(Buffer::Iterator start) const;
    virtual uint32_t Deserialize(Buffer::Iterator start);

    uint32_t m_seq;
    uint16_t m_pg;
    uint8_t m_synchronise;
    uint8_t m_ReTx;
    uint8_t pathId;
    uint32_t pathSeq;
  public:
    IntHeader ih;
  };

} // namespace ns3

#endif /* SEQ_TS_HEADER_H */