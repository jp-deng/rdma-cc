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
#include "path-id-tag.h"

namespace ns3 {

NS_OBJECT_ENSURE_REGISTERED (PathIdTag);

TypeId 
PathIdTag::GetTypeId (void)
{
  static TypeId tid = TypeId ("ns3::PathIdTag")
    .SetParent<Tag> ()
    .AddConstructor<PathIdTag> ()
  ;
  return tid;
}
TypeId 
PathIdTag::GetInstanceTypeId (void) const
{
  return GetTypeId ();
}
uint32_t 
PathIdTag::GetSerializedSize (void) const
{
  return 4;
}
void 
PathIdTag::Serialize (TagBuffer buf) const
{
  buf.WriteU32 (m_pathId);
}
void 
PathIdTag::Deserialize (TagBuffer buf)
{
  m_pathId = buf.ReadU32 ();
}
void 
PathIdTag::Print (std::ostream &os) const
{
  os << "PathId=" << m_pathId;
}
PathIdTag::PathIdTag ()
  : Tag () 
{
}

PathIdTag::PathIdTag (uint32_t id)
  : Tag (),
    m_pathId (id)
{
}

void
PathIdTag::SetPathId (uint32_t id)
{
  m_pathId = id;
}
uint32_t
PathIdTag::GetPathId (void) const
{
  return m_pathId;
}

uint32_t 
PathIdTag::AllocatePathId (void)
{
  static uint32_t nextPathId = 1;
  uint32_t pathId = nextPathId;
  nextPathId++;
  return pathId;
}

} // namespace ns3

