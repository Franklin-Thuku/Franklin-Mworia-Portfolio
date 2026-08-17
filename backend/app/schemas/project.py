from datetime import datetime
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, ConfigDict, Field


class MetricItem(BaseModel):
    val: str = Field(..., example="< 3.8ms")
    desc: str = Field(..., example="Median Latency Overhead")


class TopologyStep(BaseModel):
    type: str = Field(..., example="node")  # 'node' or 'arrow'
    label: Optional[str] = None
    sublabel: Optional[str] = None
    highlighted: Optional[bool] = False
    text: Optional[str] = None


class TopologyData(BaseModel):
    title: str = Field(..., example="TOPOLOGY: SENTINELGATE PIPELINE")
    version: str = Field(..., example="v2.4.1")
    steps: List[Dict[str, Any]] = Field(default_factory=list)


class ProjectBase(BaseModel):
    slug: str = Field(..., example="sentinelgate")
    serial_tag: str = Field(..., example="CASE STUDY // 01")
    category: str = Field(..., example="SECURITY & INFRASTRUCTURE")
    category_slug: str = Field(..., example="security backend")
    title: str = Field(..., example="SentinelGate: Reverse Proxy & Threat Mitigator")
    lead: str = Field(..., example="A high-throughput API gateway and defensive firewall engine...")
    description: Optional[str] = None
    metrics: List[MetricItem] = Field(default_factory=list)
    technologies: List[str] = Field(default_factory=list)
    topology: Optional[TopologyData] = None
    github_url: Optional[str] = None
    demo_url: Optional[str] = None
    is_featured: bool = True


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(BaseModel):
    title: Optional[str] = None
    lead: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    category_slug: Optional[str] = None
    metrics: Optional[List[MetricItem]] = None
    technologies: Optional[List[str]] = None
    topology: Optional[TopologyData] = None
    github_url: Optional[str] = None
    demo_url: Optional[str] = None
    is_featured: Optional[bool] = None


class ProjectResponse(ProjectBase):
    id: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
