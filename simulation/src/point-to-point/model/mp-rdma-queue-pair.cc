#include "mp-rdma-queue-pair.h"
#include <ns3/simulator.h>
#include <ns3/ipv4-header.h>

namespace ns3
{
    /**
     * MpRdmaQueuePair class implementation
     */
    MpRdmaQueuePair::MpRdmaQueuePair(uint16_t pg, Ipv4Address _sip, Ipv4Address _dip, uint16_t _sport, uint16_t _dport, uint32_t _mtu)
        : m_mode(MP_RDMA_HW_MODE_NORMAL),
          m_cwnd(1.0),
          m_inflate(0),
          m_lastSyncTime(Simulator::Now()),
          snd_una(0),
          snd_retx(0),
          max_acked_seq(-1),
          snd_nxt(1),
          snd_done(0),
          m_lastProbpathTime(Simulator::Now()),
          m_size(0),
          m_baseRtt(0),
          m_pg(pg),
          m_ipid(0),
          sip(_sip),
          dip(_dip),
          sport(_sport),
          dport(_dport),
          m_nextAvail(Time(0)),
          m_mtu(_mtu),
          m_rate(0),
          startTime(Simulator::Now())

    {
        lostpkts = 0;
        // generate new virtual path
        VirtualPath vp;
        // source should be from 49152 to 65535
        vp.sPort = rand() % (65535 - 49152 + 1) + 49152;
        vp.numSend = 1;
        m_vpQueue.push(vp);
    }

    TypeId MpRdmaQueuePair::GetTypeId(void)
    {
        static TypeId tid = TypeId("ns3::MpRdmaQueuePair")
                                .SetParent<Object>();
        return tid;
    }

    uint32_t MpRdmaQueuePair::GetPacketsLeft()
    {
        return ((m_size - snd_done * m_mtu) + (m_mtu - 1)) / m_mtu;
    }

    uint64_t MpRdmaQueuePair::GetBytesLeft()
    {
        if(m_size > snd_done * m_mtu)
            return m_size - snd_done * m_mtu;
        else
            return 0;
    }

    void MpRdmaQueuePair::SetSize(uint64_t size)
    {
        m_size = size;
    }

    void MpRdmaQueuePair::SetBaseRtt(uint64_t baseRtt)
    {
        m_baseRtt = baseRtt;
    }

    void MpRdmaQueuePair::SetAppNotifyCallback(Callback<void> notifyAppFinish)
    {
        m_notifyAppFinish = notifyAppFinish;
    }

    uint32_t MpRdmaQueuePair::GetHash(void)
    {
        union
        {
            struct
            {
                uint32_t sip, dip;
                uint16_t sport, dport;
            };
            char c[12];
        } buf;
        buf.sip = sip.Get();
        buf.dip = dip.Get();
        buf.sport = sport;
        buf.dport = dport;
        return Hash32(buf.c, 12);
    }

    bool MpRdmaQueuePair::IsFinished()
    {
        return snd_done * m_mtu >= m_size;
        // return snd_una * m_mtu >= m_size;
    }

    bool MpRdmaQueuePair::IsWinBound()
    {
        // return snd_nxt - snd_una >= m_cwnd;
        // printf("CalAwnd: %f\n", CalAwnd());
        return CalAwnd() < 1.0 || m_vpQueue.empty();
    }

    double MpRdmaQueuePair::CalAwnd()
    {
        // printf("snd_nxt: %lu, snd_una: %lu, m_inflate: %u, m_cwnd: %f\n", snd_nxt, snd_una, m_inflate, m_cwnd);
        // return m_cwnd - ((snd_nxt - snd_una) - m_inflate);
        return m_cwnd + m_inflate - (snd_done - snd_una);
    }

    /**
     * MpRdmaRxQueuePair class implementation
     */
    MpRdmaRxQueuePair::MpRdmaRxQueuePair()
        : m_bitmap(m_bitmapSize, 0),
          aack(0),
          aack_idx(0),
          max_rcv_seq(0),
          m_ipid(0),
          sip(0),
          dip(0),
          sport(0),
          dport(0)
    {
    }

    TypeId MpRdmaRxQueuePair::GetTypeId(void)
    {
        static TypeId tid = TypeId("ns3::MpRdmaRxQueuePair")
                                .SetParent<Object>()
                                .AddConstructor<MpRdmaRxQueuePair>();
        return tid;
    }

    uint32_t MpRdmaRxQueuePair::GetHash(void)
    {
        union
        {
            struct
            {
                uint32_t sip, dip;
                uint16_t sport, dport;
            };
            char c[12];
        } buf;
        buf.sip = sip;
        buf.dip = dip;
        buf.sport = sport;
        buf.dport = dport;
        return Hash32(buf.c, 12);
    }

    /**
     * MpRdmaQueuePairGroup class implementation
     */
    TypeId MpRdmaQueuePairGroup::GetTypeId(void)
    {
        static TypeId tid = TypeId("ns3::MpRdmaQueuePairGroup")
                                .SetParent<Object>();
        return tid;
    }

    MpRdmaQueuePairGroup::MpRdmaQueuePairGroup(void)
    {
    }

    uint32_t MpRdmaQueuePairGroup::GetN(void)
    {
        return m_qps.size();
    }

    Ptr<MpRdmaQueuePair> MpRdmaQueuePairGroup::Get(uint32_t idx)
    {
        return m_qps[idx];
    }

    Ptr<MpRdmaQueuePair> MpRdmaQueuePairGroup::operator[](uint32_t idx)
    {
        return m_qps[idx];
    }

    void MpRdmaQueuePairGroup::AddQp(Ptr<MpRdmaQueuePair> qp)
    {
        m_qps.push_back(qp);
    }

    void MpRdmaQueuePairGroup::Clear(void)
    {
        m_qps.clear();
    }
} // namespace ns3