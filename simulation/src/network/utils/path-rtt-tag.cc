/* -*- Mode:C++; c-file-style:"gnu"; indent-tabs-mode:nil; -*- */
/*
 * Copyright (c) 2008 INRIA
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
#include "path-rtt-tag.h"

namespace ns3 {

NS_OBJECT_ENSURE_REGISTERED (PathRttTag);

TypeId 
PathRttTag::GetTypeId (void)
{
  static TypeId tid = TypeId ("ns3::PathRttTag")
    .SetParent<Tag> ()
    .AddConstructor<PathRttTag> ()
  ;
  return tid;
}
TypeId 
PathRttTag::GetInstanceTypeId (void) const
{
  return GetTypeId ();
}
uint32_t 
PathRttTag::GetSerializedSize (void) const
{
  return 4;
}
void 
PathRttTag::Serialize (TagBuffer buf) const
{
  buf.WriteU32 (m_pathRtt);
}
void 
PathRttTag::Deserialize (TagBuffer buf)
{
  m_pathRtt = buf.ReadU32 ();
}
void 
PathRttTag::Print (std::ostream &os) const
{
  os << "PathRtt=" << m_pathRtt;
}
PathRttTag::PathRttTag ()
  : Tag () 
{
}

PathRttTag::PathRttTag (uint64_t id)
  : Tag (),
    m_pathRtt (id)
{
}

void
PathRttTag::SetPathRtt (uint64_t id)
{
  m_pathRtt = id;
}
uint64_t
PathRttTag::GetPathRtt (void) const
{
  return m_pathRtt;
}

} // namespace ns3

