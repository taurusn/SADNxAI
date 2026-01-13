#   


|  |
|---|
| College of Computer Science & Information Technology <br>Department of Computer Science |


**CS 511 - Project Proposal**
**Term 1 – 2021/2022**



# Software Design Specifications

# For

# Saudi Anonymization Data-Masking Network



### Version 01



### SADN:  CS Year 4, G1


Advisor: Dr. Muawia Abdelmagid Elsadig

1/12/2025
This Software Design Specification was prepared and provided as a deliverable for [Course Name, number, term], and it will be used by [name of end user]. 
This document is based in part on the IEEE Recommended Practice for Software Design Descriptions.
### Table of Content

[Revision History	12](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.48rkl1q6wwm5)
[1. Introduction	13](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.j60s76squ3xt)
[1.1 Purpose	13](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.m7u51auesyqk)
[1.2 Scope	13](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.2883umqqa78p)
[1.3 Definitions, Acronyms, and Abbreviations	15](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.5nee7yy5tb83)
[1.3.1 Definitions	15](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.utwcaoowylff)
[1.3.2 Acronyms	16](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.m5748sma27qc)
[1.4 References	17](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.gwhb6caxpxja)
[2. System overview	19](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.e1jwz56uyui1)
[2.1 System Overview - Security Perspective	19](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.um35eo3o51ib)
[3. Design Considerations	21](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.1g7otqbvdv18)
[3.1 Assumptions and Dependencies	21](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.qujnj1729cy7)
[3.1.1 Environmental Assumptions	21](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.ya975jjabhtl)
[3.1.2 Operational Assumptions	21](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.6s3ukflxrpzu)
[3.1.3 Data & Processing Assumptions	21](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.mw92z1geebkl)
[3.1.4 Infrastructure Dependencies	22](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.wkfezhnhqth8)
[3.1.5 Security-Critical Assumptions	22](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.p99fhbit2tv7)
[3.1.6 Developer-Oriented Architectural Assumptions \(Tech Lead\)	22](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.eaxzy0nlbfkt)
[3.1.7 Developer-Oriented Architectural Assumptions \(Devops\)	25](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.3hw4i4lwkgx2)
[3.1.8 Developer-Oriented Architectural Assumptions \(NLP\)	28](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.uv66fu90peu3)
[3.1.9 Team Responsibilities Assumptions	28](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.qzcmgpfie07a)
[3.2 General Constraints	28](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.ex8mz4qcrbo3)
[3.2.1 Regulatory Constraints	28](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.rvpc3b9j4gw9)
[3.2.2 Security Constraints	28](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.xnt3r2up2o7p)
[3.2.3 Architecture & Technology Constraints	29](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.v1omggn2hhi3)
[3.2.4 Operational Constraints	29](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.nrmdg2max8lw)
**[4. User Interface Design	29](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.buuddbx6hut1)**
[4.1 Overview of User Interface	29](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.o5f2nmeorc27)
[4.2 Interface Design Rules	31](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.r88sbkqb2g58)
[4.3 Screen Images	32](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.vm114vgf7hux)
[4.4 Screen Objects and Actions	39](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.nwq4dorfkw6v)
[4.5 Other Interfaces	43](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.kvyde6w9cmyn)
[5. System Architecture	48](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.3ypi10fjg8kc)
[5.1 Architectural Design Approach	48](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.ahedvlgej57i)
[5.1.1 Design Methodology	48](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.fyj7pky8asrl)
[5.1.2 Core Architectural Principles	49](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.um3cshica3n2)
[5.1.3 Design Constraints	52](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.hja8u8p08qtt)
[5.1.4 Architectural Trade-off Decisions	53](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.7212n9a3avga)
[5.2 Architectural Design	56](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.5hcqw1la2ncp)
[5.2.1 System Context	56](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.oi1elbdtw556)
[5.2.2 High-Level Architecture	57](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.czw7excxy32)
[5.2.3 Communication Patterns	59](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.55c3kksfm5tu)
[5.2.4 Data Flow Overview	61](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.qwsewte8m46j)
[5.2.5 Job Status Lifecycle	64](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.9b0650t3d4xr)
[5.2.6 Technology Stack	65](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.yv4u2c2qh43n)
[5.3 Subsystem Architecture	66](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.pjymxkp9erkl)
[5.3.1 Overview	66](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.bi5dbq8bsnoa)
[5.3.2 Processing Pipeline Decomposition	66](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.ovhi0w1rcx9x)
[5.3.3 Orchestrator Service	71](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.fz4newmjsx08)
[5.3.4 Storage Service	75](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.x67szz4yiwh)
[5.3.5 Validation Service	80](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.92wvdgroq3hb)
[5.3.6 NLP Service	87](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.c2i41djp6gnn)
[5.3.7 Masking Service	91](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.jceb6bd5xrj2)
[5.3.8 Audit Service	94](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.a147zt2h5w61)
[5.3.9 Federation Gateway	97](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.67clht1zmpwl)
[5.3.10 Inter-Service Communication	101](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.nianshqf2fj9)
[5.3.11 Sequence Diagrams	105](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.e5mblu1fg0bd)
[6. Data Design	108](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.7r7tlm7vgf8f)
[6.1 Data Description	108](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.azf8vtnvd6ok)
[6.1.1 Information Domain Overview	108](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.n00csl6xv1mp)
[6.1.2 Data Transformation into System Data Structures	109](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.8t9sb7le9f1f)
[6.1.3 Organization of System Entities	110](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.x1dbaong2amx)
[6.1.4 Databases and Storage Components	111](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.85yg3ng2lf51)
[6.1.5 Summary	111](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.jlsaeis8n70u)
[6.2 Data Dictionary	112](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.cyba1oeq3kpt)
[6.2.1 Major System Entities \(Alphabetical Order\)	112](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.ftvfscmnjgb9)
[6.2.2 Data Dictionary Table	112](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.71ml6q5w4307)
[6.2.3 Object Storage Metadata Entities	116](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.jz2qmfcd6m4)
[6.2.4 Summary	117](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.i4psnbuieg1k)
[6.3 Database Description	117](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.mv78mx5gftbq)
[6.3.1 Database Architecture Overview	117](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.qpvmvwhsujk3)
[6.3.2 Entity Overview	117](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.lrki04jsjfqr)
[6.3.3 Data Model and Table Relationships	118](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.c4or251xjqxu)
[6.3.4 Rationale for Using PostgreSQL	119](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.qp187s7jpot)
[6.3.5 Storage and Indexing Strategy	120](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.24ck1spk0506)
[6.3.6 Data Volume and Growth Expectations	121](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.nk1flpp5da02)
[6.3.7 Integration with Other System Components	121](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.9wv2lcon42j2)
[6.3.8 Summary	121](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.3a9ew0wre4pq)
**[7. Component Design	121](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.gsh0jwxa56qm)**
[7.1 Orchestrator Component	122](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.3cu3n7c3mwep)
[7.1.1 Overview	122](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.1k4cx7isonrf)
[7.1.2 Job Lifecycle Management	122](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.ga4x5imit9su)
[7.1.3 User Approval Workflow	124](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.z3ofe8o9ixqj)
[7.1.4 Result Delivery	125](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.o1pa9ure3wu8)
[7.1.5 Federation Initiation	126](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.l8ftniq75bvu)
[7.1.6 Interface Specification	126](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.k2yftmw1z9s3)
[7.1.7 Data Access	127](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.egfg6nfvc1u8)
[7.1.8 Error Handling	127](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.tvs8oyhbj7lh)
[7.1.9 Configuration	128](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.nh4935z7bme0)
[7.1.10 Security Considerations	129](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.g34xm3q4i6vo)
[7.2 NLP Component	129](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.7by9dgrlnk1d)
[7.2.1 Purpose and Scope	129](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.540kh19yo3wp)
[7.2.2 Responsibilities	130](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.49po7nek1azv)
[7.2.3 Position in System Architecture	132](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.yui5x11m5g05)
[7.2.4 External Interfaces and Dependencies	133](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.g6xoi7181m6a)
[7.2.5 Internal Structure of NLP Component	135](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.hhch9gjspl)
[7.2.6 Data Inputs and Outputs	141](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.r0ndbkda1vw1)
[7.2.7 Processing Workflow Overview	143](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.7zcbdayi2oc4)
[7.2.8 Performance Considerations	145](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.v3b35hfv7krs)
[7.2.9 Security Considerations	146](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.f3hm1tm8yp09)
[7.2.10 Error Handling	147](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.svnhm1kqg4ts)
[7.3 Masking Service Component	148](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.bit4obaxxyww)
[7.3.1 Overview	149](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.779440ehfgn6)
[7.3.2 Transformation Algorithms	150](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.pq6rkhwzms2m)
[7.3.3 Interface Specification	161](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.fq49ch8jtedw)
[7.3.4 Data Access	167](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.fy977blmuoqm)
[7.3.5 Error Handling	169](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.lom3o2idde24)
[7.3.6 Configuration	172](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.t11udck6d5mp)
[7.3.7 Security Considerations	176](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.8mihfp7u42ou)
[7.4 Validation Component	177](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.513683dqxs1o)
[7.4.1 Purpose	177](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.p935v04y1cwz)
[7.4.2 Responsibilities	177](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.jy9gpubftu1n)
[7.4.3 Inputs	178](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.31pfwu9gcah)
[7.4.4 Processing Workflow	179](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.lpzm7uykxo4h)
[7.4.5 Outputs	179](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.djxjhss0mliy)
[7.4.6 Security Considerations	180](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.5ablkawi3cpj)
[7.4.7 Failure Handling	180](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.qc3d06dplt6r)
[7.5 Storage Component	180](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.v7kjf2srs1e8)
[7.5.1 Component Overveiw	181](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.aofe8z8bedr8)
[7.5.2 Provided Interfaces	181](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.tjjvgumqhmqg)
[7.5.3 Required Interfaces	182](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.9b0jz6nd8m6f)
[7.5.4 Internal Architecture	183](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.vpucxj4k81ja)
[7.5.5 Internal Data Structures	183](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.3zvo6yc9r6ue)
[7.5.6 Processing Logic	184](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.m8u26r7crpy5)
[7.5.7 Error Handling	185](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.q9kyzxl3fivb)
[7.5.8 Security Considerations	185](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.xile0r62gbj1)
[7.5.9 Performance Considerations	186](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.d9h8ke7rdx9k)
[7.5.10 Component Dependencies	186](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.tabvf8q9gnl2)
[7.5.11 Design Rationale	187](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.ibsorweym0il)
[7.6 Audit Component	187](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.e5dxym7p7gjn)
[7.6.1 Component Overview	187](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.afbyjlqrmrjr)
[7.6.2 Audit Event Model	188](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.r9svhxs2uyh8)
[7.6.3 Tunable Parameters	193](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.mwts78lza7z4)
[7.6.4 Security Considerations	196](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.ivry5pu201gi)
[7.6.5 Audit Trail Structure	200](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.lfnaza5tb3ho)
[7.7 Federation Gateway Component	206](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.54nxzex5ustv)
[7.7.1 Overview	206](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.lzs5m45sii44)
[7.7.2 Internal Modules	208](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.jbn9wvox7atx)
[7.7.3 Federation Protocol	209](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.tycjiubsktau)
[7.7.4 Interface Specification	214](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.ail5zfuw0l0r)
[7.7.5 Data Access	216](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.birtnui40ix9)
[7.7.6 Error Handling	216](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.jomw10la48r9)
[7.7.7 Configuration	217](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.5d45c9i44fal)
[7.7.8 Security Considerations	218](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.3lbkxet162to)
[8. Detailed System Design	219](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.trz2h4af1jaj)
[8.1 Orchestrator Service	219](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.ten9cq3tgeu8)
[8.1.1 Classification	219](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.fvcuc59qjkzd)
[8.1.2 Definition	219](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.adlis1g8pkfh)
[8.1.3 Responsibilities	220](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.n59os6txkngy)
[8.1.4 Constraints	220](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.3067nvah0r4u)
[8.1.5 Composition	221](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.i2kwdvo29ei)
[8.1.6 Uses/Interactions	221](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.u2g7757w2pmg)
[8.1.7 Resources	221](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.bq9q57jipjck)
[8.1.8 Processing	222](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.a57wlawnn94t)
[8.1.9 Interface/Exports	222](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.ez9j3aa0go4a)
[8.2 NLP Detailed System Design	223](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.3kdp5vpq1t88)
[8.2.1 Classification	223](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.s1ov58m4add5)
[8.2.2 Definition	223](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.wnb3u4e9qm0p)
[8.2.3 Responsibilities	224](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.7cn44sgnl5jy)
[8.2.4 Constraints	224](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.c85qdpqsqupk)
[8.2.5 Composition	225](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.nu52mrq2s65n)
[8.2.6 Uses / Interactions	225](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.5wp0922m40id)
[8.2.7 Resources	226](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.8yqxm2tp3t3a)
[8.2.8 Processing	226](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.fcerldfonxi5)
[8.2.9 Interface / Exports	226](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.icvxso5s7gzl)
[8.2.10 Detailed Subsystem Design	227](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.oy6hc73z0fe1)
[8.3 Masking Service	227](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.w68qi73bccws)
[8.3.1 Classification	227](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.vrsri2v8bftd)
[8.3.2 Definition	227](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.m1p779weenvb)
[8.3.3 Responsibilities	228](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.cf9nnlwfvftz)
[8.3.4 Constraints	228](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.trnsjthh6s5a)
[8.3.5 Composition	228](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.n6uuqrdj0v0m)
[8.3.6 Uses/Interactions	228](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.prp7psy33pn8)
[8.3.7 Resources	228](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.jam7e0stponh)
[8.3.8 Processing	229](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.acg55ttffeum)
[8.3.9 Interface/Exports	229](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.febx7jc1idsh)
[8.4 Validation Service	229](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.dzirv6fdozzl)
[8.4.1 Classification	229](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.c9ahjr8kkjcl)
[8.4.2 Definition	230](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.2u6qpfoyoi9o)
[8.4.3Responsibilities	230](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.mtja7d6136u2)
[8.4.4 Constraints	231](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.w32cbirqcal3)
[8.4.5 . Composition	232](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.ikceeeo8j4cj)
[8.4.6 Interactions	233](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.nngk79we0a9l)
[8.4.7 Resources	233](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.xp1lrmwlqnsd)
[8.4.8 Processing Logic	234](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.j0gpe6nlmmgv)
[8.5 Storage Service	236](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.fm65gtsb57jq)
[8.5.1 Classification	236](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.v2fitwcgguuk)
[8.5.2 Definition	238](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.nst3d38bvjbs)
[8.5.3 Responsibilities	240](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.k05anji389tu)
[8.5.4 Constraints	243](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.yqwtqzvgt8o2)
[8.5.5 Composition	244](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.ysd96888a9wt)
[8.5.6 Uses / Interactions	245](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.kjpd35hqqbe1)
[8.5.7 Resources	246](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.xa0xish39gp8)
[8.5.8 Processing Logic	248](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.2ml1k0kv93cr)
[8.6 Audit Service	249](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.v967fecm41vb)
[8.6.1 Classification	249](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.kfrkocuenhq3)
[8.6.2 Definition	249](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.pj7mcb1adq8a)
[8.6.3 Responsibilities	250](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.j7z4eos8nn70)
[8.6.4 Constraints	250](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.9sc0fgthq3p7)
[8.6.5 Composition	251](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.oouia0j7slfx)
[8.6.6 Uses / Interactions	251](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.5lwgu0sx639u)
[8.6.7 Resources	252](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.vv8tvahnm7fu)
[8.6.8 Processing Logic	252](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.4q0tcjxp3i6m)
[8.7 Federation Gateway	253](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.2qa2pkqf8tlx)
[8.7.1 Classification	253](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.4u55lstq3a1z)
[8.7.2 Definition	254](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.roccnwi694l6)
[8.7.3 Responsibilities	254](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.vvooenk4hnvh)
[8.7.4 Constraints	255](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.gs14bndsv0bo)
[8.7.5 Composition	255](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.ny5a5463o3ke)
[8.7.6 Uses/Interactions	256](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.xpm4be6j8kdb)
[8.7.7 Resources	256](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.88o6vdwmocuw)
[8.7.8 Processing	257](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.b7lltbpl1691)
[8.7.9 Interface/Exports	258](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.dzasgzn8yg7y)
**[9. Other Design Features	258](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.fivbamj5acdh)**
[9.1 Performance & Reliability	258](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.j0gucohalsg9)
[9.1.1 Performance Objectives	258](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.u37miz99fbm)
[9.1.2 Scalability Architecture	260](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.74pehwcsylvo)
[9.1.3 Reliability Mechanisms	261](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.1zss5l4gfxf3)
[9.1.4 Fault Tolerance and Recovery	263](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.882aabonxob8)
[9.1.5 Backup and Recovery	265](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.p50ad4r13not)
[9.1.6 Monitoring with Prometheus	266](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.8xqce5nsa0ma)
[9.1.7 Design Rationale	269](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.at8ui1aukzd6)
[9.2 Security Feature	269](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.svwhkpa9l5py)
[9.3 Monitoring & Logging	272](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.asyxytwfpcfj)
[9.3.1 Monitoring Overview	272](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.bvfob3gqz7dm)
[9.3.2 Logging Framework	272](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.re813cm1bjsc)
[9.3.3 Metrics Collection	273](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.mndk546081jp)
[9.3.4 Distributed Tracing	273](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.y9q9z0x2ihij)
[9.3.5 Log Retention & Rotation	273](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.tp1wn1a24k7t)
[9.3.6 Alerting & Thresholds	274](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.9n6y46d4a49y)
[9.3.7 Monitoring Integration Points	274](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.ryo7g98f4std)
[9.3.8 Design Rationale	274](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.pthk1gvp5niw)
[10. Requirements Traceability Matrix	275](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.4apf1icm2dfw)
[10.1 Requirements Traceability Matrix \(RTM\)	275](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.w0ib0wmzphs8)
[10.1.1 RTM Table	275](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.r18v8lnok0ta)
[10.1.2 RTM Coverage Summary	277](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.ypmv5ue9gsla)

| *List Of Images* |
* *~[Figure 1.](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1#bookmark=id.l6e76sh4ixci)~*
* *~[Figure 2.](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1#bookmark=id.v6pn8gdbvhdi)~*
* *~[Figure 3.](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1#bookmark=id.jc7849dljd1d)~*
* *~[Figure 4.](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1#bookmark=id.nlq5bi6sc1uk)~*
* *~[Figure 5.](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1#bookmark=id.ndyvny27dnfu)~*
* *~[Figure 6.](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1#bookmark=id.z2107sgeabwf)~*
* *~[Figure 7.](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1#bookmark=id.5kh0gv8u2oa3)~*
* *~[Figure 8.](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1#bookmark=id.fz4jpvwyfyme)~*
* *~[Figure 9.](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1#bookmark=id.9i5s0le5zh5g)~*
* *~[Figure 10.](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1#bookmark=id.134lu6ovv7co)~*
* *~[Figure 11.](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1#bookmark=id.xwd0gxraovht)~*
* *~[Figure 12.](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1#bookmark=id.e906jg5sst0t)~*
* *~[Figure 13.](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1#bookmark=id.yawosnvnci95)~*
* *~[Figure 14.](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1#bookmark=id.t95ivkgw8vpu)~*
* *~[Figure 15.](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1#bookmark=id.8k1lhp89s14i)~*

⠀
| *~List Of Tables~* |
* *~[Table 1.](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1#bookmark=id.fudqr0cim67w)~*
* *~[Table 2. - Revision History.](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1#bookmark=id.gjyygurow5of)~*
* *~[Table 3. - Prepare By.](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1#bookmark=id.uzunlk15mclv)~*
* *~[Table 4. - Prepare By.](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1#bookmark=id.s3v3eoa9fovc)~*
* *~[Table 5. - Infrastructure Dependencies.](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1#bookmark=id.bm582s7flvi3)~*
* *~[Table 6.](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1#bookmark=id.k029sgsm7bz5)~*
* *~[Table 7.](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1#bookmark=id.8rf6ay833wdn)~*
* *~[Table 8.](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1#bookmark=id.nj39bqgiptsi)~*
* *~[Table 9.](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1#bookmark=id.noxb2n9slg9b)~*
* *~[Table 10.](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1#bookmark=id.m73k4t50fouz)~*
* *~[Table 11.](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1#bookmark=id.xe15hb59qqhz)~*
* *~[Table 12.](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1#bookmark=id.xhk0bzhhvg1s)~*
* *~[Table 13.](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1#bookmark=id.l8mik2rac114)~*
* *~[Table 14.](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1#bookmark=id.xats21r3d9xw)~*
* *~[Table 15.](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1#bookmark=id.bimc4a28xpk8)~*
* *~[Table 16.](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1#bookmark=id.okpe2ebz0g93)~*
* *~[Table 17.](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1#bookmark=id.vhj4z79utalh)~*
* *~[Table 18.](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1#bookmark=id.61bxpqno8w2z)~*
* *~[Table 19.](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1#bookmark=id.e6400uu5f4l4)~*
* *~[Table 20.](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1#bookmark=id.p02kb2ohabtv)~*
* *~[Table 21.](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1#bookmark=id.xlwgusz3fvby)~*
* *~[Table 22.](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1#bookmark=id.nzcqgx49qa2q)~*
* *~[Table 23.](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1#bookmark=id.8photxqgl15r)~*
* *~[Table 24.](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1#bookmark=id.qb7eihuaznig)~*
* *~[Table 25.](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1#bookmark=id.rtz607l2yqu1)~*
* *~[Table 26.](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1#bookmark=id.ibzns9fkyusa)~*
* *~[Table 27.](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1#bookmark=id.8uo51w17vozd)~*
* *~[Table 28.](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1#bookmark=id.t95htylewk2f)~*
* *~[Table 29.](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1#bookmark=id.cm7vfr6z05wc)~*
* *~[Table 30.](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1#bookmark=id.7w0kcaqi4osz)~*
* *~[Table 31.](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1#bookmark=id.8qfz6gl1jvjq)~*
* *~[Table 32.](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1#bookmark=id.xos3jilzwec)~*
* *~[Table 33.](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1#bookmark=id.b8biy4xa2goc)~*
* *~[Table 34.](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1#bookmark=id.53md45k0alv)~*
* *~[Table 35.](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1#bookmark=id.k1mg9fszi2n1)~*
* *~[Table 36.](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1#bookmark=id.kb1it7li5xvh)~*
* *~[Table 37.](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1#bookmark=id.qh1v4u9yb7nz)~*
* *~[Table 38.](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1#bookmark=id.mjrjjtz5gbug)~*
* *~[Table 39.](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1#bookmark=id.rnygmldgd6l1)~*
* *~[Table 40.](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1#bookmark=id.afafc1uz2sxs)~*
* *~[Table 41.](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1#bookmark=id.ox59oh9nrd4k)~*
* *~[Table 42.](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1#bookmark=id.66u24zyi5v07)~*
* *~[Table 43.](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1#bookmark=id.uenpy3n6j2y4)~*
* *~[Table 44.](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1#bookmark=id.jgl68oc7ftr4)~*
* *~[Table 45.](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1#bookmark=id.g22vrufoqqes)~*
* *~[Table 46.](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1#bookmark=id.iida9ez1o0b5)~*
* *~[Table 47.](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1#bookmark=id.4g4udsgsrnkg)~*
* *~[Table 48.](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1#bookmark=id.ig9hrml6d5hr)~*
* *~[Table 49.](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1#bookmark=id.pcb4xw4b1dnf)~*
* *~[Table 50.](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1#bookmark=id.lgxpfytof52x)~*
* *~[Table 51.](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1#bookmark=id.4gyta6wvt9n3)~*
* *~[Table 52.](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1#bookmark=id.tmywitwdsxju)~*
* *~[Table 53.](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1#bookmark=id.oplnf6mhwxuo)~*
* *~[Table 54.](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1#bookmark=id.8rqa5o9y3c64)~*
* *~[Table 55.](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1#bookmark=id.tauoaw2cvo8j)~*
* *~[Table 56.](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1#bookmark=id.keym4xsj7h8b)~*
* *~[Table 57.](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1#bookmark=id.eiwuwx749gym)~*
* *~[Table 58.](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1#bookmark=id.93i3w7bz0250)~*
* *~[Table 59.](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1#bookmark=id.qa2as11u5zxv)~*
* *~[Table 60.](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1#bookmark=id.3ailqujbu64d)~*
* *~[Table 61.](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1#bookmark=id.1i12iq9tn6o)~*
* *~[Table 62.](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1#bookmark=id.uzfx7sydsom7)~*
* *~[Table 63.](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1#bookmark=id.qphvi4ay8msl)~*
* *~[Table 64.](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1#bookmark=id.qv2qgvcmfbnk)~*
* *~[Table 65.](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1#bookmark=id.9bj4hnvq69tz)~*
* *~[Table 66.](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1#bookmark=id.7ey2nvgnp84v)~*
* *~[Table 67.](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1#bookmark=id.9fpvph516l5y)~*
* *~[Table 68.](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1#bookmark=id.3zrlogmtr1x5)~*
* *~[Table 69.](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1#bookmark=id.33kpokhdkkq4)~*
* *~[Table 70.](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1#bookmark=id.os8w3ri5i37p)~*
* *~[Table 71.](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1#bookmark=id.se731xjjjc45)~*
* *~[Table 72.](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1#bookmark=id.2zmwi7uwhwqe)~*
* *~[Table 73.](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1#bookmark=id.iahbgv1dj164)~*
* *~[Table 74.](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1#bookmark=id.svmgqtsj7tbi)~*
* *~[Table 75.](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1#bookmark=id.r9nljgmb7fjg)~*
* *~[Table 76.](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1#bookmark=id.a5lmmb7tv2m6)~*
* *~[Table 77.](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1#bookmark=id.hv3dvsg9y4l4)~*
* *~[Table 78.](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1#bookmark=id.knqezx26sbpm)~*
* *~[Table 79.](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1#bookmark=id.7xtubbkisy82)~*
* *~[Table 80.](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1#bookmark=id.t8nakq2oru8l)~*
* *~[Table 81.](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1#bookmark=id.qab01e92l5rq)~*
* *~[Table 82.](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1#bookmark=id.hc8rpdijawl7)~*
* *~[Table 83.](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1#bookmark=id.hsg83hexvkhi)~*
* *~[Table 84.](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1#bookmark=id.vw8091d1vv7u)~*
* *~[Table 85.](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1#bookmark=id.w99e8xuaqe4z)~*
* *~[Table 86.](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1#bookmark=id.bkj8axe4okrd)~*
* *~[Table 87.](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1#bookmark=id.qehkp7j8x7ci)~*
* *~[Table 88.](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1#bookmark=id.g27eafwjmjex)~*
* *~[Table 89.](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1#bookmark=id.nc9h8hqdkcvr)~*
* *~[Table 90.](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1#bookmark=id.pon6lzis995m)~*
* *~[Table 91.](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1#bookmark=id.bb6qh8bfccl2)~*
* *~[Table 92.](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1#bookmark=id.b0iwi4ne4az)~*
* *~[Table 93.](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1#bookmark=id.nj7msbeajwap)~*
* *~[Table 94.](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1#bookmark=id.o0339mmz6334)~*
* *~[Table 95.](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1#bookmark=id.690m8yj0yucz)~*
* *~[Table 96.](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1#bookmark=id.tnp7q4c978lm)~*
* *~[Table 97.](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1#bookmark=id.2imehctch7mc)~*
* *~[Table 98.](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1#bookmark=id.snzpzu4vklbl)~*
* *~[Table 99.](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1#bookmark=id.plvydb8qea1b)~*
* *~[Table 100.](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1#bookmark=id.l8vxjrngheke)~*
* *~[Table 101.](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1#bookmark=id.eb8uyd9qmn90)~*
* *~[Table 102.](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1#bookmark=id.srg8gyqm9te3)~*
* *~[Table 103.](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1#bookmark=id.h5vwpd4k9cfy)~*
* *~[Table 104.](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1#bookmark=id.fy5mj2y7xz4u)~*
* *~[Table 105.](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1#bookmark=id.3rbtt04q3jqp)~*
* *~[Table 106.](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1#bookmark=id.2lg552q6t67n)~*
* *~[Table 107.](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1#bookmark=id.dajsvsx2nfg0)~*
* *~[Table 108.](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1#bookmark=id.eb6bosas1gbz)~*
* *~[Table 109.](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1#bookmark=id.zef6dbfdg8y8)~*
* *~[Table 110.](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1#bookmark=id.ybkctx29kv7t)~*
* *~[Table 111.](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1#bookmark=id.oqx3nptw23bs)~*
* *~[Table 112.](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1#bookmark=id.nn3ki0r6yel8)~*
* *~[Table 113.](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1#bookmark=id.ed6l0awf82gk)~*
* *~[Table 114.](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1#bookmark=id.rrm5aq9xc93r)~*
* *~[Table 115.](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1#bookmark=id.nyhey19yz2pk)~*
* *~[Table 116.](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1#bookmark=id.ai7kf1x8i5ry)~*
* *~[Table 117.](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1#bookmark=id.g8gm1h6orgd1)~*
* *~[Table 118.](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1#bookmark=id.isz1mdjg3ovy)~*
* *~[Table 119.](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1#bookmark=id.3wwiyv8jwmqs)~*
* *~[Table 120.](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1#bookmark=id.qkroyrvvil6b)~*
* *~[Table 121.](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1#bookmark=id.bt014wc0uh8j)~*
* *~[Table 122.](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1#bookmark=id.trvxk790qjzw)~*
* *~[Table 123.](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1#bookmark=id.n2ce1j3wynfo)~*
* *~[Table 124.](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1#bookmark=id.xyawacm98qf0)~*
* *~[Table 125.](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1#bookmark=id.kwuuosef8hov)~*
* *~[Table 126.](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1#bookmark=id.y2mcxt3w8hrc)~*
* *~[Table 127.](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1#bookmark=id.4ylsvlwb58to)~*
* *~[Table 128.](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1#bookmark=id.7m38k1hmyfxp)~*
* *~[Table 129.](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1#bookmark=id.pvuwfoc4474q)~*
* *~[Table 130.](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1#bookmark=id.gq8u23zaqoc2)~*
* *~[Table 131.](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1#bookmark=id.n2y4g01lkvbk)~*
* *~[Table 132.](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1#bookmark=id.82rtlm7x4ycg)~*
* *~[Table 133.](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1#bookmark=id.ahweugyahg7x)~*
* *~[Table 134.](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1#bookmark=id.ti0fyroz0co)~*
* *~[Table 135.](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1#bookmark=id.xrcfn2n2p3p5)~*
* *~[Table 136.](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1#bookmark=id.93dw006zyywl)~*
* *~[Table 137.](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1#bookmark=id.nxmtw6c9zicq)~*
* *~[Table 138.](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1#bookmark=id.d3nsbevzuyxh)~*
* *~[Table 139.](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1#bookmark=id.2tjcv25v9ugd)~*
* *~[Table 140.](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1#bookmark=id.nk5iszop9tj4)~*
* *~[Table 141.](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1#bookmark=id.dn0y9g3wwj28)~*
* *~[Table 142.](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1#bookmark=id.ly5bsc16ost7)~*
* *~[Table 143.](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1#bookmark=id.q5l800875ryu)~*
* *~[Table 144.](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1#bookmark=id.ijouyeefjpnu)~*
* *~[Table 145.](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1#bookmark=id.vsnm3leowcns)~*
* *~[Table 146.](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1#bookmark=id.4iu3rs1oy6sz)~*
* *~[Table 147.](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1#bookmark=id.7zeo8g57t3fh)~*
* *~[Table 148.](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1#bookmark=id.1wmo9ca187bx)~*
* *~[Table 149.](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1#bookmark=id.f8g5ivdx3srl)~*
* *~[Table 150.](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1#bookmark=id.6tssrhoyzqxu)~*
* *~[Table 151.](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1#bookmark=id.3hteytpvjjcq)~*
* *~[Table 152.](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1#bookmark=id.m3sadert3v8t)~*
* *~[Table 153.](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1#bookmark=id.6waholvuw68w)~*
* *~[Table 154.](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1#bookmark=id.1dbkhsfoaffh)~*
* *~[Table 155.](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1#bookmark=id.j6gr7nj490jp)~*
* *~[Table 156.](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1#bookmark=id.y245mw87kpoa)~*
* *~[Table 157.](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1#bookmark=id.dfzybiarr5n4)~*
* *~[Table 158.](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1#bookmark=id.yy5mj34j7wo9)~*
* *~[Table 159.](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1#bookmark=id.2fbfdq60ypb4)~*
* *~[Table 160.](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1#bookmark=id.k208y89347m1)~*
* *~[Table 161.](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1#bookmark=id.5wt3js74bfh9)~*
* *~[Table 162.](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1#bookmark=id.bl8a64bglhx4)~*
* *~[Table 163.](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1#bookmark=id.axjsdrfp76wq)~*
* *~[Table 164.](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1#bookmark=id.c893683n1v50)~*
* *~[Table 165.](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1#bookmark=id.3frur683wcy6)~*
* *~[Table 166.](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1#bookmark=id.7pdz85ltmpm)~*

⠀
| Student Name | ID |
|:-:|:-:|
| Mojeb Faiz Alotaibi | 2210002058 |
| Hatim Abdulelah Alshehri | 2220002490 |
| Mohammed Abdulmohsen Jablawi | 2210002275 |
| Abdullah Ahmed Al Abdulatif | 2220006525 |
*Table 1.* 


**Revision History**

| **Name** | **Date** | **Reason For Changes** | **Version** |
|---|---|---|---|
| All members | Dec 1, 2025 | Prepared initial version | 0.1 |
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |
*Table 2. - Revision History.*

### 1 Introduction
### 1 Purpose	

⠀
           	The purpose of this Software Design Specification (SDS) is to provide a complete, structured, and technically accurate description of the internal architecture, components, data flows, and processing logic of the **Saudi Anonymization and Data Masking Network (SADN)**.
  	This document defines how each subsystem operates, how services interact, and how the system enforces **privacy, security, reliability, and regulatory compliance** in alignment with Saudi national data governance frameworks.
This SDS ensures:
* A unified reference for developers, privacy engineers, and system architects.
* A consistent technical foundation for implementing all SADN microservices.
* Clear documentation of anonymization, validation, audit, storage, and orchestration mechanisms.
* Alignment with PDPL, NDMO, NCA ECC-2, and MOH IS0303 requirements.
* Support for secure data sharing between institutions through the Federation Gateway.
* Complete clarity on the responsibilities, interfaces, workflows, and processing pipelines within the system.

⠀Ultimately, this SDS defines **how SADN is designed to transform sensitive data into compliant, anonymized datasets**, while maintaining full auditability, high performance, and strict adherence to national privacy laws.



### 2 Scope

⠀This Software Design Specification (SDS) defines the complete technical design of the **Saudi Anonymization and Data Masking Network (SADN)**.
  	It establishes a unified and authoritative reference for the system’s architecture, internal components, data flows, and processing logic.  The SDS specifies *how* SADN is built, *how* its services interact, and *how* it enforces privacy, security, reliability, and compliance with national regulatory frameworks.
**In-Scope**
The SDS includes a comprehensive design description for the following areas:
**1\. System Architecture**
* Event-driven microservices architecture
* Inter-service communication patterns (RabbitMQ, REST)
* Storage lifecycle and pipeline coordination

⠀**2. Component-Level Design**
Detailed specifications for all seven SADN microservices:
1 Orchestrator
2 NLP Service
3 Masking Service
4 Validation Service
5 Storage Service
6 Audit Service
7 Federation Gateway

⠀Each component includes:
* Responsibilities
* Processing workflows
* Interfaces and message structures
* Subsystem architecture

⠀**3. Data Design**
* Data dictionaries
* Database schema (PostgreSQL)
* File lifecycle (intake → staging → safe → archive)
* Metadata structures
* Audit chain integrity

⠀**4. Security & Privacy Engineering**
* Design-level implementation of PDPL, NDMO, MOH IS0303, and NCA ECC-2
* Anonymization and masking controls
* Privacy metric validation (k-anonymity, l-diversity, t-closeness)
* Access control, encryption, and tamper-evident audit mechanisms

⠀**5. Processing Pipeline**
1 End-to-end workflow from data ingestion to anonymized output
2 Phase transitions and validation logic
3 Message publishing and consumption rules
4 Fault-tolerance and error-recovery design

⠀**Out of Scope**
The SDS excludes:
* Project management activities or team workflows
* Deployment and environment-specific configurations
* User training, manuals, or operational procedures
* Real-time streaming or external EHR integrations
* Business-level data governance policies
* Performance benchmarking beyond the design requirements
* UI/UX guidelines unrelated to technical UI integration

⠀

### 3 Definitions, Acronyms, and Abbreviations

⠀This section provides clear definitions and standardized terminology used throughout the Software Design Specification (SDS).
  	It ensures that all readers, developers, architects, auditors, and stakeholders , share a consistent understanding of SADN’s components, processes, and technical language.
**1.3.1 Definitions**
| **Term** | **Definition** |
|---|---|
| **Anonymization** | **A privacy-preserving process that transforms personal data into a state where no individual can be identified, directly or indirectly, in accordance with PDPL and NDMO standards.** |
| **Masking** | **A technical transformation applied to sensitive data using methods such as generalization, pseudonymization, tokenization, redaction, and format-preserving encryption (FPE).** |
| **PII (Personally Identifiable Information)** | **Any data that can uniquely identify an individual (e.g., national ID, full name, IBAN, phone number).** |
| **PHI (Protected Health Information)** | **Medical data that identifies a patient (e.g., diagnosis, medications, procedures), subject to MOH IS0303 requirements.** |
| **Quasi-Identifiers** | **Non-PII attributes that may reveal identity when combined with other data (e.g., age, gender, zipcode).** |
| **k-Anonymity** | **A privacy metric ensuring each quasi-identifier group contains at least** ***k*** **similar records.** |
| **l-Diversity** | **A privacy metric requiring every group to contain at least** ***l*** **distinct sensitive attribute values.** |
| **t-Closeness** | **A metric comparing the distribution of sensitive attributes in a group with the overall dataset distribution to ensure similarity.** |
| **Job** | **A complete anonymization workflow instance starting from file upload and ending with a validated anonymized dataset.** |
| **Pipeline** | **The automated, multi-stage workflow executed by the seven SADN microservices.** |
| **Storage Phase** | **A MinIO-based file lifecycle stage: intake → staging → quarantine → safe → archive.** |
| **Federation Peer** | **An approved external institution authorized to exchange anonymized datasets via the Federation Gateway.** |
*Table 3. - Prepare By.*
**1.3.2 Acronyms**

| **Acronym** | **Meaning** |
|---|---|
| **SADN** | Saudi Anonymization and Data Masking Network |
| **SDS** | Software Design Specification |
| **PII** | Personally Identifiable Information |
| **PHI** | Protected Health Information |
| **PDPL** | Personal Data Protection Law (Saudi Arabia) |
| **NDMO** | National Data Management Office |
| **NCA ECC-2** | National Cybersecurity Authority – Essential Cybersecurity Controls |
| **MOH IS0303** | Ministry of Health Information Security Standard |
| **NLP** | Natural Language Processing |
| **FPE** | Format-Preserving Encryption |
| **RBAC** | Role-Based Access Control |
| **mTLS** | Mutual Transport Layer Security |
| **API** | Application Programming Interface |
| **DLQ** | Dead Letter Queue |
| **ETL** | Extract, Transform, Load |
| **DB** | Database |
| **CI/CD** | Continuous Integration / Continuous Deployment |
*Table 4. - Prepare By.*

### 4 References

⠀
	This SDS references the following documents, standards, and technical sources that guided the specification and design of the SADN platform:
1 IEEE Std 830-1998 - IEEE Recommended Practice for Software Requirements Specifications. Institute of Electrical and Electronics Engineers, 1998.
2 IEEE Std 1016-2009 - IEEE Standard for Information Technology-Systems Design-Software Design Descriptions. IEEE Computer Society, 2009.
3 Saudi Data and AI Authority (SDAIA). (2021). *Personal Data Protection Law (PDPL).* Retrieved from~[https://sdaia.gov.sa](https://sdaia.gov.sa/)~
4 National Data Management Office (NDMO). (2023). *Data Governance and Anonymization Frameworks.* Retrieved from~[https://sdaia.gov.sa/ndmo/Files/PoliciesEn001.pdf](https://sdaia.gov.sa/ndmo/Files/PoliciesEn001.pdf)~
5 Python Software Foundation. (2024). *Python Documentation – SSL Library and Cryptography Toolkit.* Retrieved from~[https://docs.python.org/3/library/ssl.html](https://docs.python.org/3/library/ssl.html)~
6 FastAPI Documentation. (2024). *High-Performance Web Framework for APIs in Python.* Retrieved from~[https://fastapi.tiangolo.com](https://fastapi.tiangolo.com/)~
7 Docker Inc. (2024). *Docker and Docker Compose User Guide.* Retrieved from~[https://docs.docker.com](https://docs.docker.com/)~
8 Bonawitz, K. et al. (2019). *Federated Learning at Scale: Design and Implementation.* Google AI Research.
9 Li, N., & Li, T. (2007). *t-Closeness: Privacy Beyond k-Anonymity and l-Diversity.* IEEE ICDE.
10 Dwork, C. (2006). *Differential Privacy.* Theory of Cryptography Conference (TCC).
11 Oracle Corporation. (2021). *Oracle Data Masking and Subsetting Guide.* Oracle Database 19c Documentation.
12 Saudi Data & AI Authority (SDAIA). (2022). *Regulation on the Transfer of Personal Data Outside the Kingdom*. Riyadh, Saudi Arabia. Retrieved from:~[https://sdaia.gov.sa](https://sdaia.gov.sa/)~
13 Saudi Data & AI Authority (SDAIA). (2021). *National Data Sharing and Privacy Policy*. Riyadh, Saudi Arabia. Retrieved from:~[https://sdaia.gov.sa](https://sdaia.gov.sa/)~
14 Saudi Ministry of Health (MOH) - National eHealth Strategy & Change Management Office (SCMO). *eHealth Strategy and Change Management Publications*. Riyadh, Saudi Arabia.
15 Saudi Ministry of Health (MOH). (2021). *Health Information Exchange Policies (IS0303)*. Riyadh, Saudi Arabia. Retrieved from:~[https://www.moh.gov.sa](https://www.moh.gov.sa/)~
16 Saudi Data & AI Authority (SDAIA). (2021). *National Data Governance Policies*. Riyadh, Saudi Arabia. Retrieved from:~[https://sdaia.gov.sa](https://sdaia.gov.sa/)~
17 National Cybersecurity Authority (NCA). (2022/2024). *Essential Cybersecurity Controls (ECC)*. Riyadh, Saudi Arabia. Retrieved from:~[https://nca.gov.sa](https://nca.gov.sa/)~

⠀

### 2 System overview

⠀
SADN is a modular, event-driven, privacy-preserving data anonymization platform designed to transform sensitive datasets into research-ready anonymized outputs while maintaining full compliance with Saudi regulatory frameworks such as PDPL, NDMO, MOH IS0303, and NCA ECC-2.
The system operates as a collection of independent microservices that coordinate through RabbitMQ message queues while persisting their state in PostgreSQL and managing all data files through a controlled five-phase storage lifecycle in MinIO. SADN is designed to process structured and unstructured data, detect PII/PHI in both Arabic and English, apply cryptographic and statistical anonymization techniques, and verify the resulting privacy guarantees before releasing datasets for research use.
At the highest level, the SADN pipeline consists of:
**1** **Dataset Intake & Validation** – receiving uploaded datasets via the Orchestrator, validating integrity, file format, malware scanning, and initial compliance checks.
**2** **PII/PHI Detection** – analyzing datasets using bilingual NLP and Saudi-specific pattern recognition to detect sensitive attributes.
**3** **Privacy-Preserving Masking** – applying seven anonymization techniques including pseudonymization, generalization, FPE, suppression, tokenization, perturbation, and text redaction.
**4** **Privacy Metrics Validation** – calculating k-anonymity, l-diversity, t-closeness, and deriving a risk score that determines whether the dataset is approved for release.
**5** **Secure Storage Lifecycle** – managing files across five isolated phases (intake, staging, quarantine, safe, archive) with AES-256 encryption and strict access controls.
**6** **Audit & Compliance Logging** – recording all events in an immutable Merkle-chained audit log to meet regulatory and evidentiary standards.
**7** **Federated Data Sharing** – optionally enabling institutions to share validated anonymized datasets through an mTLS-secured Federation Gateway.

⠀SADN uses an event-driven “choreography” pattern where each service autonomously consumes messages, processes data independently, updates its state in PostgreSQL, and emits new events into RabbitMQ. This architecture ensures loose coupling, high scalability, fault tolerance, and independent deployability of components.
The system is deployed entirely on-premises using Docker and Docker Compose, ensuring full data sovereignty and compliance with local regulations regarding the handling of sensitive personal and health data.

### 2.1 System Overview - Security Perspective
From a security and privacy perspective, SADN is designed as a high-assurance platform that enforces strict confidentiality, integrity, and compliance requirements throughout the entire data anonymization pipeline. The system applies a layered security architecture (defense-in-depth) that integrates authentication, authorization, cryptographic controls, secure storage, event integrity, and regulatory compliance into every stage of processing.
Security controls begin at dataset intake, where files undergo integrity verification, malware scanning, and strict validation to ensure that no harmful or malformed data enters the processing pipeline. All inter-service communication is isolated within an internal Docker network, while external access is limited to the Orchestrator API and the Federation Gateway-both protected using TLS 1.3, authenticated access, and strict RBAC.
SADN enforces *least privilege* at every layer:
* each microservice uses dedicated credentials stored in HashiCorp Vault,
* permissions are scoped only to the operations required,
* users can access only the safe/ (final anonymized) datasets,
* and sensitive phases (staging, intake, quarantine) remain isolated from all external users.

⠀Data is protected at rest using AES-256 encryption through MinIO, and in transit using TLS-secured channels. For PII transformation, SADN uses strong cryptographic techniques including SHA-256 hashing, AES-256 Format-Preserving Encryption (FF3-1), and randomized tokenization. These controls ensure both privacy preservation and regulatory compliance.
Integrity is guaranteed through a Merkle-chained audit log that detects tampering with any event in the system, providing non-repudiation and a complete accountability trail across Orchestrator, NLP, Masking, Validation, Storage, and Federation services.
From an overall security standpoint, SADN is architected to meet the requirements of PDPL, NDMO Data Governance, NCA ECC-2, and MOH IS0303 through enforced access controls, cryptographic safeguards, strict lifecycle isolation, continuous integrity verification, and full auditability of all actions.






### 3 Design Considerations

⠀
This section defines the architectural assumptions, dependencies, and constraints that influence the overall design of SADN. These considerations ensure that all services operate consistently within the expected environment, comply with regulatory requirements, and align with the system’s security and privacy objectives.


### 1 Assumptions and Dependencies

⠀The design of SADN relies on a set of foundational assumptions and external dependencies that must be satisfied for the system to function as intended. These include environmental, operational, regulatory, and technical expectations.
**3.1.1 Environmental Assumptions**
1 The system is deployed **on-premises** within a controlled environment that meets PDPL and NCA ECC-2 physical and network security requirements.
2 All data processed by SADN remains within Saudi Arabia’s jurisdiction and under the organization’s full data sovereignty.
3 The deployment environment provides sufficient compute, storage, and network resources to support parallel microservice execution.

⠀**3.1.2 Operational Assumptions**
1 All users accessing SADN are authenticated and authorized through the Orchestrator using RBAC-enforced roles.
2 Dataset uploads originate from trusted institutional users (researchers, analysts, DPOs).
3 Administrators properly maintain HashiCorp Vault, ensuring periodic key rotation and secure token management.
4 Docker and Docker Compose are installed, updated, and configured according to security best practices.
5 The federation partners (if enabled) follow mTLS and DUA requirements.

⠀**3.1.3 Data & Processing Assumptions**
1 Uploaded datasets conform to supported formats (CSV, JSON, Parquet, Excel).
2 Text fields may contain Arabic, English, or mixed content requiring multilingual detection.
3 All datasets include at least one quasi-identifier required for privacy metric computation.
4 The NLP models (spaCy) and FPE libraries (FF3-1) are available at runtime.
5 There is no requirement for real-time processing-batch-style asynchronous processing is acceptable.

⠀**3.1.4 Infrastructure Dependencies**
SADN depends on the following components being available and properly configured:
| **Component** | **Dependency Description** |
|---|---|
| **PostgreSQL** | Central metadata, NLP/masking/validation results, audit logs |
| **RabbitMQ** | Message choreography across microservices |
| **MinIO** | Five-phase storage lifecycle |
| **HashiCorp Vault** | Secret management + encryption keys |
| **Docker Network** | Internal communication and isolation |
| **spaCy Models** | Arabic/English PII detection |
| **ClamAV** | Intake malware scanning |
*Table 5. - Infrastructure Dependencies.*
**3.1.5 Security-Critical Assumptions**
1\.     All security controls (TLS configurations, Vault secrets, RBAC roles, audit verification scripts) must be reviewed and approved by the Security & Privacy Leader before deployment.
2\.      No microservice is allowed to store or log raw PII/PHI at any stage, including debug logs.
3\.      Any policy updates (masking rules, privacy thresholds, federation permissions) require explicit sign-off from the Security & Privacy Leader to prevent misconfiguration–based data leakage.
4\.      Any failure in masking or validation automatically triggers a security event, not just a system error, and must be logged for investigation.
5\.      Cryptographic keys used for FPE, HMAC, and TLS must be rotated quarterly or upon incident escalation.
**3.1.6 Developer-Oriented Architectural Assumptions (Tech Lead)**
This subsection defines the architectural expectations, coding standards, and development conventions that all SADN developers must adhere to when implementing, extending, or maintaining system components. These assumptions ensure consistency across the microservices architecture and establish clear boundaries that prevent architectural drift during development.
**3.1.6.1 Service Ownership and Boundaries**
Each microservice within SADN is treated as an independent unit of ownership. A single developer or sub-team is responsible for the complete lifecycle of each service, including implementation, testing, documentation, and ongoing maintenance. This ownership model ensures accountability and prevents ambiguity when issues arise during development or production operation.
Services must not contain logic that belongs to another service's domain. The Masking Service, for example, must not implement validation logic, and the Validation Service must not perform any data transformation. If a capability appears to span multiple services, the appropriate solution is to coordinate through message queues rather than embedding cross-domain logic within a single service.
Database tables are logically partitioned by service responsibility. While all services connect to the same PostgreSQL instance, each service writes only to tables within its domain. The Validation Service writes to validation_results, the Masking Service writes to masking_results, and the Audit Service writes to audit_logs. No service may directly modify tables owned by another service; all cross-service state changes must occur through published messages that the owning service consumes and processes.
Shared code libraries between services are discouraged. Each service should be self-contained and independently deployable without requiring synchronized updates to other services. Where common data structures are necessary, such as job status enumerations or standard message formats, these should be defined through explicit interface contracts rather than shared compiled libraries.
**3.1.6.2 Code Organization Standards**
All SADN microservices must follow a consistent internal organization to ensure that developers can navigate unfamiliar services efficiently and that code reviews remain productive across team members.
Source code resides within a dedicated directory that separates concerns by functional area. API-related code, including HTTP endpoint definitions and request handlers, is isolated from core business logic. Business logic and domain services are centralized in a dedicated module that contains no framework-specific dependencies, enabling unit testing without infrastructure concerns. Data models, including both database entities and message schemas, reside in a dedicated models area. Queue-related code, including consumers and publishers, is grouped separately from HTTP-related code to maintain clarity between synchronous and asynchronous interfaces. Storage operations, including MinIO interactions, are encapsulated within a dedicated module that abstracts file system details from business logic.
Configuration is managed exclusively through environment variables. No service may contain hardcoded connection strings, credentials, queue names, or operational parameters. All configurable values are loaded at startup and validated before the service begins accepting requests or consuming messages. Missing required configuration must cause the service to fail immediately with a clear error message rather than proceeding with undefined behavior.
Naming conventions are enforced consistently across all services. File names use lowercase with underscores to separate words. Class names use Pascal case with descriptive nouns indicating purpose. Function and method names use lowercase with underscores and begin with verbs describing the action performed. Constants use uppercase with underscores and are defined at module level rather than embedded within functions. Queue names use lowercase with underscores matching the consuming service's domain. External API endpoints use lowercase with hyphens separating words in URL paths.
**3.1.6.3 API and Message Schema Conventions**
External APIs exposed by the Orchestrator follow a versioned path structure beginning with the version identifier. All current endpoints use version one, and future breaking changes will introduce version two while maintaining version one for backward compatibility during a defined deprecation period. Internal endpoints used for service-to-service communication follow a distinct naming pattern that clearly identifies them as non-public interfaces.
Error responses follow a consistent structure across all services. Every error response includes an error code using uppercase with underscores, a human-readable message suitable for logging, and a details object containing context-specific information relevant to the failure. This consistency enables client applications and monitoring systems to handle errors uniformly regardless of which service produced the error.
Queue message schemas include mandatory fields that appear in every message regardless of purpose. Every message includes the job identifier linking the message to a specific processing job, an action field indicating the requested operation, and a timestamp recording when the message was created. Additional fields are defined per message type and documented in the corresponding service specification.
Schema evolution requires backward compatibility. New fields may be added to existing message schemas, but existing fields may not be removed or have their types changed without introducing a new message version. Consumers must ignore unrecognized fields to ensure that older service versions can process messages from newer publishers during rolling deployments.
**3.1.6.4 Testing Expectations**
Every service must include unit tests covering core business logic. These tests validate the correctness of algorithms, transformations, and decision logic independent of external systems. Unit tests must not require running instances of PostgreSQL, RabbitMQ, or MinIO; all external dependencies are replaced with test doubles that simulate expected behavior.
Integration tests verify that services correctly interact with their external dependencies. These tests run against containerized instances of PostgreSQL, RabbitMQ, and MinIO to confirm that connection handling, query execution, message publishing, and file operations function correctly. Integration tests also verify queue consumer behavior, ensuring that messages are acknowledged only after successful processing and that failures result in appropriate retry or dead letter queue routing.
No service deployment proceeds without passing all automated tests through the continuous integration pipeline. Test failures block deployment regardless of urgency. This constraint ensures that production stability is never sacrificed for delivery speed and that regressions are caught before reaching production environments.
Test coverage expectations vary by module type. Core business logic requires high coverage ensuring that all significant code paths are exercised. API endpoint tests verify request validation, authorization checks, and response formatting. Queue consumer tests verify message parsing, processing logic, and acknowledgment behavior. Infrastructure modules such as database connectors and storage clients require integration tests demonstrating correct behavior against real service instances.
**3.1.6.5 Extensibility Assumptions**
New capabilities are added through well-defined extension points rather than modifications to existing service internals. New microservices are introduced by subscribing to existing queues and publishing to existing or new queues without requiring changes to established services. This approach ensures that existing functionality remains stable while new capabilities are developed and deployed independently.
New external endpoints are added exclusively through the Orchestrator. No new service may expose external HTTP interfaces; all external access flows through the single entry point to maintain consistent authentication, authorization, and audit logging. Internal endpoints may be added to any service as needed to support new inter-service communication requirements.
Database schema changes follow a migration-based approach. Python services use Alembic for managing PostgreSQL schema evolution, while the Masking Service uses Entity Framework migrations. All migrations are version-controlled alongside application code and executed as part of the deployment process. Destructive migrations that remove columns or tables require a multi-phase approach: first deploying code that no longer depends on the removed elements, then executing the migration in a subsequent deployment.
Message schema extensions must not break existing consumers. New optional fields may be added freely, but existing fields remain stable. If a fundamental schema change is required, a new message type is introduced while the original message type continues to function until all consumers are updated. This gradual transition approach prevents coordination challenges during deployments and allows services to be updated independently.

**3.1.7 Developer-Oriented Architectural Assumptions (Devops)**
This subsection outlines the architectural assumptions and dependencies that influence how the system is developed, deployed, and operated from a DevOps perspective. These assumptions relate to required software components, hosting environment, operating system expectations, end-user behavior, and anticipated future changes.
**3.1.7.1 Software & Platform Dependencies**
* The system is deployed as a **containerized microservices architecture** using Docker.
* A standard orchestration layer (Docker Compose or Kubernetes) is assumed for:
  * service networking
  * environment variable injection
  * persistent volume management
  * health-check orchestration
* The following infrastructure components must be available in all environments:
  * **PostgreSQL** (primary database)
  * **RabbitMQ** (message queues: storage_queue, validation_queue, audit_queue, etc.)
  * **MinIO or S3-compatible object storage** for dataset and metadata files
* The application stack assumes:
  * Most services run on **Python** (FastAPI)
  * Masking Service runs on **.NET 8 (C#)** but is containerized and treated like any other service
* CI/CD expectations:
  * A Git-based repository with a branching strategy (main, develop, feature branches)
  * Automated pipelines capable of building images, running tests, and deploying via push to registry

⠀**3.1.7.2 Hardware & Environment Assumptions**
The system is hosted on **Linux-based servers** with container runtime support.
Each environment (dev / stage / prod) provides enough compute and memory to process datasets up to 500MB per job.
Persistent storage is provisioned for:
* PostgreSQL data directory
* MinIO buckets
* Log retention for monitoring and audit purposes

⠀Internal networking assumptions:
* All microservices communicate over a **private internal network**.
* Public access passes only through the orchestrator/dashboard layer behind TLS.
* Network latency is expected to be local or low-latency-architecture is not tuned for cross-region high-latency links.

⠀**3.1.7.3 Operating System & Runtime Assumptions**
* All containers run on **Linux-compatible base images** (Debian/Ubuntu/Alpine).
* Hosts run 64-bit Linux distributions with:
  * systemd or containerd runtime
  * secure random sources for crypto operations (/dev/urandom)
* Python and .NET runtimes rely on:
  * built-in cryptographic libraries
  * TLS 1.3 support
  * secure SSL configurations for client/server communication

⠀**3.1.7.4 End-User & Operator Characteristics**
End users (Data Owners, Data Consumers, DPOs, Auditors) interact **only through the dashboard/Orchestrator**.
No end user directly accesses internal microservices.
Operational DevOps responsibilities assume:
* Basic familiarity with Docker logs, queue monitoring, and service restarts
* Ability to manage environment variables and secrets (via Vault, .env files, or cloud secret managers)
* Ability to review health metrics, logs, and queue backlogs

⠀Workload assumptions:
* Moderate concurrency (multiple jobs active simultaneously).
* Horizontal scaling may be required in heavy load scenarios.

⠀**3.1.7.5 Functionality Evolution & Scalability Assumptions**
* Future feature growth is expected to occur through:
  * New microservices
  * Additional queue consumers
  * New endpoints exposed through the Orchestrator
* Architectural contracts assume:
  * Message formats on queues may evolve, but will remain backward-compatible and versioned.
  * Database schema changes follow migration tooling (Alembic for Python, EF migrations for C#).
  * Storage and audit services are expected to grow in size; therefore, archival, partitioning, and pruning mechanisms must remain configurable.
* The system is designed to scale via:
  * **Horizontal scaling** (replicas of Python/Masking/Validation workers)
  * **Stateless services** where possible
  * **Configurable resource allocation** via container limits
* Cloud/on-prem neutrality:
  * The architecture assumes only standard container runtimes and network protocols.
  * Cloud-managed alternatives (e.g., AWS S3, Cloud SQL, managed RabbitMQ) can replace self-hosted components if protocol-compatible.

⠀**3.1.8 Developer-Oriented Architectural Assumptions (NLP)**
**3.1.9 Team Responsibilities Assumptions**
* **Security Leader (Mojeb):** Validates all security configurations, cryptographic settings, masking policy changes, and oversees all audit/incident-related processes.
* **Tech Lead (Hatim):** Owns architectural consistency, service boundaries, communication patterns, and ensures all services follow the microservice choreography model.
* **DevOps & Storage (Abdullah):** Ensures infrastructure stability, secure bucket policies, correct Docker networking, and enforcement of lifecycle rules.
* **NLP & UI (Mohammed):** Maintains bilingual PII detection accuracy, ensures UI privacy compliance, and updates Saudi-specific pattern rules.

⠀

### 2 General Constraints

⠀This section outlines the architectural, regulatory, technical, and operational constraints that restrict system design choices. These constraints directly influence how SADN must be implemented, secured, and validated.
**3.2.1 Regulatory Constraints**
1 All processing must comply with **Saudi PDPL**, especially Articles related to data minimization, purpose limitation, storage limitation, and security requirements.
2 Compliance with **NCA ECC-2** is mandatory for access control, audit logging, system integrity, and secure communications.
3 The system must support **MOH IS0303** for healthcare datasets, particularly around PHI protection and 7-year minimum retention.
**4** **Data cannot leave Saudi Arabia**, reinforcing the on-prem deployment model.

⠀**3.2.2 Security Constraints**
1 All data at rest must be encrypted using **AES-256**, and all data in transit must use **TLS 1.3** or higher.
2 Secrets, credentials, and encryption keys cannot be stored in code or config files-**Vault is mandatory**.
3 Only anonymized data stored in safe/ may be accessible to researchers, staging/intake/quarantine are isolated.
4 All services must enforce **least privilege** and use service-specific credentials.

⠀**3.2.3 Architecture & Technology Constraints**
1 The system must use an **event-driven choreography** model, no direct service-to-service API calls.
2 Docker is required; bare-metal or monolithic deployments are **not supported**.
3 File operations between storage phases must be **atomic**, no partial copies or inconsistent states.
4 NLP processing is CPU-heavy; real-time performance is **not achievable nor required**.

⠀**3.2.4 Operational Constraints**
1 Dataset size is capped at **500 MB** to ensure acceptable processing time.
2 Quarantine datasets may only be reviewed by the **DPO**, per PDPL requirements.
3 Data retention rules (7 years → archive, 30-day quarantine cleanup) must be strictly enforced.
4 Audit logs must be **append-only**, with UPDATE/DELETE operations prohibited.
### 4 User Interface Design

⠀
This section describes the graphical user interface (GUI) of the SADN platform as implemented in the current React-based frontend. The interface is a web application composed of multiple views controlled by application state (currentView) and role-based behavior (userRole). The UI is designed to support different user classes (Data Engineer, DPO, Auditor, Admin, etc.) while enforcing least-privilege access and presenting anonymization workflows in a clear and interactive manner.
The main UI is rendered by the App component, which conditionally displays either the **Login View** or the **Main Layout** (navigation shell + content views) depending on the authentication state.

### 1 Overview of User Interface

⠀The SADN user interface is organized into two major layers:
* Authentication Layer (Login + MFA)
* Main Operational Dashboard (Role-based Navigation + Feature Views)

⠀**4.1.1 Authentication Flow (LoginView)**
The **Login View** provides the initial entry point to the system:
* Username and password input fields.
* Role selection dropdown (Engineer, Auditor, DPO, Admin) used for demo and UI behavior.
* A **two-step authentication process**:
  * Step 1: User enters username/password; if both are present, the “Login” button becomes enabled.
  * Step 2: The UI switches to an MFA screen requiring a 6-digit code; only after entering 6 digits is the “Verify” button enabled and, on success, the user is transitioned to the main dashboard.

⠀From the user’s perspective, the login flow guides them through:
* Credential entry
* MFA verification
* Automatic redirection to the **Dashboard** upon successful authentication

⠀A demo hint is displayed to clarify that any credentials and any 6-digit code are accepted in the current prototype.
**4.1.2 Main Layout and Navigation**
Once authenticated, the UI renders the **MainLayout**, consisting of:
* A fixed **left sidebar** with:
  * System branding (SADN name and subtitle “Secure Data Anonymization”).
  * Navigation items (Dashboard, Upload, Policies, Jobs, Validation, Audit, Federation, Admin), each mapped to a logical view.
  * Current role label and a Logout button.
* A scrollable **content area** that dynamically renders different views based on currentView:
  * dashboard → DashboardView
  * upload → UploadView
  * policies → PoliciesView
  * jobs → JobsView
  * validation → ValidationView
  * audit → AuditView
  * federation → FederationView
  * admin → AdminView

⠀**4.1.3 Functional Views from the User Perspective**
From the user’s point of view, the main functional views are:
* **Dashboard**
  * High-level summary of running, completed, and failed jobs.
  * Display of global privacy thresholds (k, l, t) as cards.
  * System alerts (e.g., dead-letter queue warnings).
  * For DPO users, display of “Pending Approvals”.
  * Quick actions to navigate to Upload, Policies, and Audit.
* **Dataset Upload**
  * Guided file selection and upload.
  * Automatic file analysis (mocked in the prototype) showing:
    * File type, size, row count.
    * Detected columns and inferred data types.
    * Columns flagged as PII with sample values.
  * Summary explaining how many columns contain PII.
  * Call-to-action to start the anonymization process.
* **Policy Management**
  * Table of active masking/anonymization policies (field → action → status).
  * Inline rule editor to define new rules (field name + action: Mask, Generalize, Suppress, FPE).
* **Job Monitoring**
  * Filterable table of anonymization jobs (Job ID, Status, Stage, Date).
  * Filters for status, job ID, and date, allowing the user to quickly locate specific jobs.
* **Privacy Validation**
  * Detailed view of a selected job’s validation outcome (pass/fail).
  * Display of computed metrics: k-anonymity, l-diversity, t-closeness.
  * Privacy compliance summary (all thresholds met vs. violations detected).
  * When failing, list of detected violations per attribute.
  * Masked sample preview table.
  * Action buttons allowing the user to view reports, send to safe storage, move to quarantine, request re-run, and download the dataset.
  * A pipeline status sidebar showing the current stage in the overall processing pipeline (Intake → NLP → Masking → Validation → Storage).
* **Audit Logs**
  * Filterable audit log table with timestamp, user, operation, job ID, status, and hash.
  * Ability to filter by user, operation type, job ID, and date.
  * Hash chain visualization, showing a sequence of blocks representing log integrity.
  * Export capabilities (CSV and PDF).
* **Federation Gateway**
  * Form to initiate secure data transfer to external partners:
    * Select anonymized dataset.
    * Select destination partner.
  * Security status indicators (encryption, digital signature, certificate validity, TLS version).
  * Transfer history list with direction (inbound/outbound), status, size, and progress.
  * Statistics cards summarizing transfer volume and success rate.
  * List of active partners and their status.
* **Administration**
  * System health cards (API, database, message queue, storage).
  * User management table with roles, MFA status, account status, and last login.
  * MFA policy configuration (enforce MFA, backup codes, session timeout).
  * Certificate and encryption key management views (validity, expiration, rotation actions).
  * Configuration cards for database connections, API rate limits, and backup status.

⠀Overall, the user can complete the full anonymization lifecycle-from upload to validation, audit, and external sharing-through clearly separated and role-oriented screens.
### 2 Interface Design Rules

⠀**4.2.1 Visual and Layout Principles**
The implemented UI follows a consistent visual language:
* **Color Palette:**
  * Primary: #03514D (teal/green)
  * Dark accent: #012F2D
  * Used across headers, buttons, table headers, and gradient backgrounds.
* **Card-Based Layout:**
  * Key information is grouped into rectangular cards with rounded corners and soft shadows.
  * Cards are used for metrics, file info, alerts, health status, and configuration summaries.
* **Grid and Responsiveness:**
  * grid and responsive classes are used to adapt layouts from single-column on small screens to multi-column on larger screens.
  * The main layout splits into a fixed-width sidebar and a flexible content area.
* **Iconography:**
  * Icons from lucide-react (e.g., Shield, Upload, Activity, AlertTriangle) are used to provide visual cues for actions and statuses.

⠀**4.2.2 Interaction and Behavior Rules**
* **State-driven Navigation:**
  * Navigation is handled by currentView; selecting a sidebar item updates this state and renders the corresponding view without reloading the page.
* **Role Awareness:**
  * This supports the design principle of least privilege and role-based UI tailoring.
* **Form Validation:**
  * Client-side validation controls button enabled states:
    * Login button disabled until username and password are provided.
    * MFA verify button disabled until a 6-digit code is entered.
    * “Initiate Secure Transfer” disabled until both dataset and partner are selected.
* **Feedback and Loading States:**
  * Upload analysis shows a spinner and loading message while “Analyzing file structure...”
  * Validation view offers a dynamic pass/fail banner and metric cards indicating PASS/FAIL status against thresholds.
  * System alerts and warnings use color-coded badges (red/yellow/green).

⠀**4.2.3 Security and Privacy Rules**
While the current code uses mock data, the UI is designed according to:
* **Clear Separation of Concerns:**
  * Views related to raw data (upload, analysis, masking preview) are separate from views dealing with external sharing (federation) and security configuration (admin).
* **Explicit Warnings and Status:**
  * PII detection in the upload view is highlighted visually and summarized.
  * Validation view explicitly labels violations and severity.
* **No Direct Raw PII Exposure in UI Logic:**
  * Sample data used in the prototype is obscured (masked IDs, generalized age ranges, obfuscated ZIP codes).

⠀**4.2.4 Accessibility and Localization Considerations**
* Layout and typography are kept clean and readable to simplify future localization (e.g., English/Arabic).
* Button sizes, spacing, and color contrast are suitable for enterprise environments.
* The component-based structure allows easy replacement of labels and text with localized strings in future revisions.

⠀
### 3 Screen Images

⠀
The following screen images shall be included in the SDS (as actual screenshots or high-fidelity mockups), corresponding directly to the React views defined in the code:
**1** **Login and MFA Screen (LoginView)**

⠀

 Shows username/password fields, role selection, and MFA code step.
**2** **Main Dashboard (DashboardView)**

⠀

Shows running/completed/failed job cards, privacy threshold cards, alerts, and quick action 
Tiles.













**3** **Dataset Upload & Column Analysis (UploadView)** 

⠀




 Shows upload drop zone, file info summary, PII column detection, and “Start Anonymization Process” call-to-action.
**4** **Policy Management Screen (PoliciesView)**

⠀

 Shows the active policies table and the rule editor (field/action selection).
**5** **Job Monitoring Screen (JobsView)**

⠀
 Shows filters and the job table with status badges and stages.
**6** **Privacy Validation Screen (ValidationView)**

⠀

Shows pass/fail banner, metric cards, compliance summary, violations table (for failing cases), masked sample preview, actions, and pipeline sidebar.














**7** **Audit Logs and Hash Chain Visualization (AuditView)**

⠀ Shows filterable audit log table and visual representation of hash chain blocks.
**8** **Federation Gateway Screen (FederationView)**

⠀
 Shows dataset and partner selection, security indicators, transfer history, and statistics.
**9** **Administration Screen (AdminView)**

⠀ Shows health cards, user management table, MFA settings, certificate/key management, and system configuration cards.

### 4 Screen Objects and Actions

⠀
This subsection defines the key interactive elements of the SADN user interface and specifies the actions associated with each object. Each screen object is mapped to one or more user-triggered behaviors, and the resulting system responses are captured to ensure predictable, role-aligned interaction patterns.
The design follows a **deterministic and state-driven interaction model**, where every button, field, dropdown, or navigation element produces a well-defined effect within the system. This mapping is essential for ensuring consistency across views, supporting least-privilege role restrictions, and enabling traceability of user interactions when connected to backend services such as the Orchestrator, Validation Engine, Policy Manager, Audit Log Service, and Federation Gateway.
The tables below summarize the primary UI components, their corresponding user actions, and the expected system behavior from the user's perspective. These mappings cover the complete workflow of SADN, including authentication, dataset ingestion, policy management, job tracking, validation, auditing, and administrative security controls.


**1** **Authentication**

⠀
| **Object** | **Action** | **Result** |
|:-:|:-:|:-:|
| Username field | Enter text | Updates local login state |
| Password field | Enter text | Updates local login state |
| Role dropdown | Select role | Sets userRole for subsequent UI behavior |
| **Login** button | Click (when enabled) | Switches to MFA step |
| MFA code field | Enter digits (max 6) | Validates length; enables Verify button |
| **Verify** button | Click with 6-digit code | Sets isAuthenticated = true; opens MainLayout |
| **Logout** button | Click | Resets auth state; returns to LoginView |
*Table 6.* 


**2** **Navigation and Dashboard**

⠀
| **Object** | **Action** | **Result** |
|:-:|:-:|:-:|
| Sidebar item “Dashboard” | Click | currentView = 'dashboard' |
| Sidebar item “Upload” | Click | currentView = 'upload' |
| Sidebar item “Policies” | Click | currentView = 'policies' |
| Sidebar item “Jobs” | Click | currentView = 'jobs' |
| Sidebar item “Validation” | Click | currentView = 'validation' |
| Sidebar item “Audit” | Click | currentView = 'audit' |
| Sidebar item “Federation” | Click | currentView = 'federation' |
| Sidebar item “Admin” | Click | currentView = 'admin' |
| Dashboard CTA “Upload Dataset” | Click | Navigates to UploadView |
| Dashboard CTA “Manage Policies” | Click | Navigates to PoliciesView |
| Dashboard CTA “Audit Logs” | Click | Navigates to AuditView |
*Table 7.* 


**3** **Upload and Column Analysis**

⠀
| **Object** | **Action** | **Result** |
|:-:|:-:|:-:|
| Drag-and-drop area | Drop file | Triggers analyzeFile and shows analysis UI |
| “Load Demo Data” button | Click | Creates mock file object and triggers analysis |
| “X” (remove file) button | Click | Clears file, fileInfo, and columns; returns to idle |
| “Start Anonymization Process” | Click | Navigates to JobsView (representing pipeline start) |
*Table 8.* 

**4** **Jobs and Validation**

⠀
| **Object** | **Action** | **Result** |
|:-:|:-:|:-:|
| Audit filters (user/op/job/date) | Change value | Filters displayed logs |
| “Export as CSV / PDF” | Click | Initiates log export (mock in prototype) |
| Dataset dropdown (Federation) | Select dataset | Stores selected dataset for transfer |
| Partner dropdown (Federation) | Select partner | Stores selected partner |
| “Initiate Secure Transfer” | Click (when enabled) | Initiates outbound transfer (in full implementation) |
| “Add User” (Admin) | Click | Opens user creation flow (future extension) |
| Role dropdown in user table | Change role | Would update user role mapping in full system |
| MFA toggles | Toggle | Updates MFA policy settings |
| “Rotate Certificate/Key” | Click | Would trigger rotation workflow |
*Table 9.* 


**5** **Audit, Federation, and Administration**

⠀
| **Object** | **Action** | **Result** |
|:-:|:-:|:-:|
| Audit filters (user/op/job/date) | Change value | Filters displayed logs |
| “Export as CSV / PDF” | Click | Initiates log export (mock in prototype) |
| Dataset dropdown (Federation) | Select dataset | Stores selected dataset for transfer |
| Partner dropdown (Federation) | Select partner | Stores selected partner |
| “Initiate Secure Transfer” | Click (when enabled) | Initiates outbound transfer (in full implementation) |
| “Add User” (Admin) | Click | Opens user creation flow (future extension) |
| Role dropdown in user table | Change role | Would update user role mapping in full system |
| MFA toggles | Toggle | Updates MFA policy settings |
| “Rotate Certificate/Key” | Click | Would trigger rotation workflow |
*Table 10.* 

**Summary of Interaction Behavior**
The mapping above describes the full set of interface actions that constitute all user-visible interactions within the SADN platform. Every UI component-whether a button, dropdown, table element, or navigation control-has an explicitly defined purpose, input behavior, and corresponding system reaction. This ensures that user interactions remain:
* **Predictable**, by associating each object with a consistent system response.
* **Secure**, by enforcing role-based access restrictions at both UI and backend levels.
* **Traceable**, with actions integrated into SADN's audit and evidence logging subsystem.
* **Aligned with workflow logic**, ensuring each action transitions the system into the correct anonymization stage.

⠀By formalizing object–action relationships, the UI supports operational clarity, reduces the likelihood of user error, and maintains compliance with privacy and security requirements dictated by PDPL and enterprise governance policies. This level of definition is essential for high-assurance anonymization systems such as SADN, enabling reliable integration with backend microservices and ensuring a seamless experience across all user classes
### 4.5 Other Interfaces
This section documents the additional interfaces used by the SADN web-based UI to communicate with the backend microservices. These interfaces are derived directly from the SADN Source-of-Truth architecture and describe the technologies, protocols, message formats, handshake semantics, initiation and closure behavior, and error-handling rules relevant to each subsystem. Although the current UI prototype uses simulated data, the following interface specifications represent the expected production-level design.
**4.5.1 Web Front-End to Ingestion Service Interface**
The Ingestion Service interface enables dataset upload, schema extraction, and initial job creation. The interface uses a synchronous request–response pattern over HTTPS.
**Technology and Protocol:**
* HTTPS over TLS 1.2+
* REST-style endpoints exposed by the SADN API Gateway
* Mixed payload formats: multipart/form-data for file upload, JSON for metadata

⠀**Initiation and Closure:**
* Initiation occurs when the user selects a file in the UploadView.
* Upon submission, the browser performs a POST request including the file contents.
* Once the Ingestion service extracts schema information and assigns a Job ID, the HTTP transaction is closed.

⠀**Request Format:**
POST /api/v1/ingest/upload  
Content-Type: multipart/form-data  
file=<binary>  
uploaderRole=engineer
**Response Format:**
{
  "jobId": "job_20250114_001",
  "columns": [
    { "name": "email", "type": "string", "pii": true },
    { "name": "age", "type": "integer", "pii": false }
  ],
  "rowCount": 1250
}
**Error Conditions:**
* 415 Unsupported Media Type (invalid or corrupted file format)
* 422 Unprocessable Entity (empty file or unreadable schema)
* 403 Forbidden (role not permitted to upload datasets)

⠀**4.5.2 Web Front-End to Orchestrator / Workflow Engine Interface**
The Orchestrator manages all pipeline transitions-Intake, NLP, Masking, Validation, and Storage. The UI interacts with this service to retrieve job state.
**Technology and Protocol:**
* HTTPS REST polling
* JSON request and response bodies

⠀**Interaction Behavior:**
* No persistent connection is maintained.
* UI periodically polls /jobs/{jobId}/status to update the pipeline indicator.

⠀**Response Example:**
{
  "status": "Running",
  "stage": "NLP",
  "progress": 47
}
**Error Conditions:**
* 404 Not Found (job does not exist)
* 409 Conflict (invalid transition attempted)
* 500 Internal Server Error

⠀**4.5.3 Web Front-End to NLP Engine Interface**
The NLP Engine provides structured PII/PHI detection results used during column analysis and masking verification.
**Technology and Protocol:**
* HTTPS REST
* JSON responses
* NLP engine internally uses spaCy/transformer models and regex pattern matching

⠀**Request Format:**
GET /api/v1/nlp/{jobId}/entities
**Response Format:**
{
  "detectedEntities": [
    { "column": "email", "type": "EMAIL", "count": 1240 },
    { "column": "phone_number", "type": "PHONE", "count": 980 }
  ]
}
**Error Conditions:**
* 503 Service Unavailable (NLP engine offline)
* 424 Failed Dependency (Ingestion failed earlier)

⠀**4.5.4 Web Front-End to Masking Engine Interface**
The Masking Engine interface provides masked sample previews and applies field-level anonymization policies (Mask/Generalize/Suppress/FPE).
**Technology and Protocol:**
* HTTPS REST
* JSON messages

⠀**Request:**
GET /api/v1/masking/{jobId}/preview
**Response:**
{
  "sample": [
    { "id": "****1234", "zipcode": "12***", "diagnosis": "Type-A" }
  ],
  "policyVersion": "v47"
}
**Error Conditions:**
* 409 Policy Version Conflict
* 500 Masking Transformation Error

⠀**4.5.5 Web Front-End to Validation Engine Interface**
The Validation Engine computes privacy metrics (k-anonymity, l-diversity, t-closeness) and determines dataset PASS/FAIL status.
**Technology:**
* HTTPS-based REST interface
* JSON responses
* Thresholds defined in the Policy Service

⠀**Request:**
GET /api/v1/validation/{jobId}
**Response:**
{
  "k": 12,
  "l": 3,
  "t": 0.09,
  "status": "PASS",
  "violations": []
}
**Handshake:** Validation computations happen asynchronously; UI only retrieves final metrics.
**Error Conditions:**
* 422 Metrics Not Ready (job still running)
* 500 Validation Computation Error

⠀**4.5.6 Web Front-End to Storage & Quarantine Manager Interface**
This interface handles the final classification of datasets into Safe Storage or Quarantine based on validation outcomes.
**Technology:**
* HTTPS REST
* JSON request bodies
* Secure role-based authorization (DPO-only)

⠀**Request:**
POST /api/v1/storage/{jobId}/decision
{
  "decision": "safe",
  "approvedBy": "dpo@example.com"
}
**Response:**
{
  "result": "stored_in_safe_area"
}
**Error Conditions:**
* 403 Forbidden (only DPO allowed)
* 409 Conflict (decision already applied)

⠀**4.5.7 Web Front-End to Audit & Evidence Chain Interface**
The Audit Service provides immutable logs of system activity using a hash-chained ledger.
**Technology and Protocol:**
* HTTPS REST
* JSON for logs
* PDF/CSV file streaming for exports

⠀**Request:**
GET /api/v1/audit/logs?user=jane&operation=job_start
**Response:**
{
  "logs": [
    {
      "timestamp": "2025-01-14T10:30:15Z",
      "event": "Job Start",
      "user": "jane.smith@company.com",
      "status": "Success",
      "hash": "9d4e7f..."
    }
  ]
}
**Error Conditions:**
* 403 Forbidden (auditors only)
* 413 Payload Too Large
* 500 Internal Error

⠀**4.5.8 Web Front-End to Federation Gateway Interface**
The Federation Gateway manages secure external data transfers using presigned URLs.
**Control Plane (REST JSON):**
POST /api/v1/federation/transfer
{
  "datasetId": "customer_data_anon",
  "partnerId": "research_A"
}
**Data Plane (Presigned URL):**
GET https://gateway.example.com/download/xf-20250114-001?signature=...
**Error Conditions:**
* 403 Dataset Not Approved for Sharing
* 410 Gone (expired presigned URL)
* 500 Signing Service Unavailable

⠀**4.5.9 Web Front-End to Admin/Security Configuration Interface**
This interface manages system configuration, health monitoring, MFA policies, certificates, and user roles.
**Technology:**
* HTTPS REST
* JSON responses

⠀**Examples:**
GET /api/v1/admin/health
Response:
{
  "api": "online",
  "db": "healthy",
  "queue": "warning",
  "storage": "78% used"
}
**Error Conditions:**
* 403 Admin Privileges Required
* 503 Service Unavailable
### 5 System Architecture

⠀
This section should provide a high-level overview of how the functionality and responsibilities of the system were partitioned and then assigned to subsystems or components. 
Don't go into too much detail about the individual components themselves (there is a subsequent section for detailed component descriptions). The main purpose here is to gain a general understanding of how and why the system was decomposed, and how the individual parts work together to provide the desired functionality.

At the top-most level, describe the major responsibilities that the software must undertake and the various roles that the system (or portions of the system) must play. Describe how the system was broken down into its components/subsystems (identifying each top-level component/subsystem and the roles/responsibilities assigned to it). Describe how the higher-level components collaborate with each other in order to achieve the required results. Don't forget to provide some sort of rationale for choosing this particular decomposition of the system (perhaps discussing other proposed decompositions and why they were rejected). Feel free to make use of design patterns, either in describing parts of the architecture (in pattern format), or for referring to elements of the architecture that employ them.

If there are any diagrams, models, flowcharts, documented scenarios or use-cases of the system behavior and/or structure, they may be included here (unless you feel they are complex enough to merit being placed in the Detailed System Design section). Diagrams that describe a particular component or subsystem should be included within the particular subsection that describes that component or subsystem.


### 1 Architectural Design Approach

⠀5.1.1 Design Methodology
The Saudi Anonymization and Data Masking Network adopts a microservices-based architecture with event-driven choreography as its foundational design methodology. This approach was selected following a systematic evaluation of alternative architectural patterns against the system's core requirements: regulatory compliance, data privacy assurance, and operational resilience.
**Architectural Pattern Evaluation**
| **Pattern** | **Evaluation Status** | **Decision** | **Rationale** |
|:-:|:-:|:-:|:-:|
| Monolithic | Evaluated | Rejected | Single point of failure unacceptable for privacy-critical systems; compliance boundaries cannot be enforced at module level; horizontal scaling requires replicating the entire application |
| Microservices | Evaluated | Adopted | Clear service boundaries align with compliance domains; enables independent deployment and scaling; fault isolation prevents cascade failures across processing stages |
| Serverless | Not Evaluated | Not Applicable | Institutional deployment requirement necessitates on-premises installation, which is incompatible with cloud-dependent serverless execution models |
*Table 11.* 
**Rationale for Monolithic Architecture Rejection**
A monolithic architecture would consolidate all processing logic-including natural language processing detection, data masking, privacy validation, secure storage, and audit logging-into a single deployable unit. This architectural pattern presents unacceptable risks for the Saudi Anonymization and Data Masking System:
First, regarding compliance boundaries, the Personal Data Protection Law and National Cybersecurity Authority Essential Cybersecurity Controls require explicit separation between data processing stages. A monolithic architecture obscures these boundaries, complicating the enforcement and verification of audit trails required for regulatory compliance.
Second, concerning fault isolation, a failure in the natural language processing module within a monolithic system would render the entire application unavailable. The microservices architecture ensures that a failure in the NLP Service only affects NLP-dependent processing jobs while permitting other system operations to continue uninterrupted.
Third, with respect to independent scalability, healthcare datasets exhibit significant variance in size and complexity. The microservices architecture permits independent scaling of computationally intensive services, such as the Masking Service, without necessitating proportional scaling of lightweight services such as the Audit Service.
### 5.1.2 Core Architectural Principles
The architecture of the Saudi Anonymization and Data Masking System is guided by six foundational principles that collectively ensure the system satisfies its privacy, security, and operational objectives:

*Figure 1.* 
### Architectural Design Principles
**Principle Definitions and Applications**
| **Principle** | **Definition** | **Application** |
|:-:|:-:|:-:|
| Single Responsibility | Each service shall perform exactly one well-defined function within the system | The NLP Service is responsible exclusively for personally identifiable information detection; the Masking Service is responsible exclusively for data transformation; the Validation Service is responsible exclusively for privacy metric verification |
| Loose Coupling | Services shall not directly depend on the internal implementation of other services | Inter-service coordination occurs through asynchronous message queues; file transfers use internal HTTP endpoints as message queues cannot efficiently handle large binary payloads |
| Event-Driven Communication | Services shall react to events published to message queues rather than being explicitly invoked by a central controller | The NLP Service consumes messages from the NLP queue and publishes results to the masking queue; no central controller coordinates the processing pipeline |
| Defense in Depth | The system shall implement multiple independent security layers such that compromise of one layer does not compromise the entire system | Data is encrypted both at rest and in transit; authentication and authorization are enforced independently; input validation and output validation occur at separate processing stages |
| Compliance by Design | Regulatory requirements shall be embedded within the architectural structure rather than implemented as supplementary controls | The Audit Service exists as a first-class architectural component; storage phases enforce retention policies programmatically; the Federation Gateway enforces cross-border data transfer regulations |
| Single Entry Point | All external requests shall enter the system through a single controlled gateway | Only the Orchestrator Service receives external HTTP requests; all other services expose internal endpoints only; Data Owners never communicate directly with processing services |
*Table 12.* 
**Communication Pattern Rationale**
The system employs a hybrid communication pattern that optimizes for both loose coupling and operational efficiency:
| **Communication Type** | **Mechanism** | **Rationale** |
|:-:|:-:|:-:|
| Workflow Coordination | RabbitMQ Message Queues | Provides temporal decoupling, automatic retry via dead letter queues, and resilience for long-running jobs |
| File Transfer | Internal HTTP Endpoints | Message queues are unsuitable for large binary payloads (up to 500MB); HTTP provides efficient streaming transfer |
| Audit Logging | RabbitMQ Message Queues | Asynchronous logging ensures audit operations do not block processing; guarantees delivery through persistence |
*Table 13.* 
Internal HTTP endpoints follow a strict naming convention (/internal/*) and are accessible only within the Docker network. These endpoints transfer file data exclusively; all workflow state and coordination messages flow through RabbitMQ queues.
### 5.1.3 Design Constraints
External regulatory and operational requirements impose constraints that have materially influenced the architectural decisions of the Saudi Anonymization and Data Masking System:
| **Constraint Source** | **Requirement** | **Architectural Impact** |
|:-:|:-:|:-:|
| Saudi Personal Data Protection Law | Personal data must be irreversibly anonymized prior to external sharing | The Validation Service shall verify k-anonymity and l-diversity metrics before data transitions from the staging phase |
| Saudi Personal Data Protection Law | A complete audit trail shall be maintained for all data operations | A dedicated Audit Service maintains Merkle-chained cryptographic logs; all services publish audit events to the audit queue |
| Saudi Personal Data Protection Law | Data subjects retain rights over their personal data | User approval is required before anonymized data moves to the safe phase; original data is preserved until explicit approval |
| National Cybersecurity Authority ECC-2 | Data shall be encrypted at rest and in transit | AES-256-GCM encryption is applied to all stored data; TLS 1.3 is required for all network communications; mutual TLS is required for federation |
| National Cybersecurity Authority ECC-2 | Access control and authentication mechanisms shall be enforced | Role-based access control is enforced at the Orchestrator; service-to-service authentication utilizes X.509 certificates |
| Ministry of Health IS0303 | Healthcare data shall be retained for a minimum of seven years | The five-phase storage lifecycle implements automated archival; retention policies are enforced programmatically by the Storage Service |
| Ministry of Health IS0303 | Protected health information requires heightened security controls | The NLP Service incorporates healthcare-specific entity detection including diagnoses, medications, and medical record numbers |
| National Data Management Office | Data classification shall occur prior to processing | Automated column classification is performed by the Validation Service; columns are categorized as direct identifiers, quasi-identifiers, or sensitive attributes |
*Table 14.* 
### 5.1.4 Architectural Trade-off Decisions
The design of the Saudi Anonymization and Data Masking System required resolution of several trade-offs between competing architectural concerns. The following table documents these decisions and their technical justifications:



### Architectural Trade-off Resolutions
*Figure 2.* 

| **Decision Domain** | **Selected Approach** | **Alternative Considered** | **Trade-off Analysis** |
|:-:|:-:|:-:|:-:|
| Inter-Service Communication | Hybrid: Queues for coordination, HTTP for file transfer | Pure queue-based communication | Pure queue-based communication cannot efficiently handle files up to 500MB; hybrid approach preserves loose coupling for workflow coordination while enabling efficient binary transfer |
| Pipeline Coordination | Choreography with<br>self-coordinating services | Centralized orchestration | Choreography eliminates single points of failure within the processing pipeline; the Orchestrator component functions exclusively as an entry point and status tracking mechanism rather than as a step-by-step workflow coordinator |
| User Approval Workflow | Explicit approval required before finalization | Automatic transition upon validation pass | Explicit approval ensures Data Owners verify anonymization quality before data becomes available; supports PDPL requirements for data subject control; enables review of privacy-utility trade-offs |
| Masking Service Implementation Language | C# with .NET 8 runtime | Python to maintain stack homogeneity | C# provides superior computational performance for intensive masking algorithms and access to mature cryptographic libraries within the .NET ecosystem; the introduction of stack heterogeneity is acceptable given well-defined service boundaries and API contracts |
| Storage Volume Architecture | Single Docker volume with phase-based directory structure | Separate volumes for each storage phase | A single volume architecture simplifies backup and restoration procedures and enables atomic phase transitions via directory renaming rather than cross-volume data copying; phase isolation is achieved through directory structure and file system access controls |
| Intake Validation Architecture | Internal module within Storage Service | Separate microservice | The decision to implement intake validation as an internal module avoids unnecessary architectural complexity; intake validation is inherently coupled to storage operations and does not benefit from the additional network latency of a separate service |
| Original File Retention | Preserved in staging until user approval | Deleted immediately after masking | Preserving original files enables re-processing if masking parameters require adjustment; deletion occurs only upon explicit user approval, ensuring compliance with data minimization principles |
*Table 15.* 


### 2 Architectural Design

⠀5.2.1 System Context
The Saudi Anonymization and Data Masking Network operates within an institutional environment, providing privacy-preserving data transformation services to healthcare and educational organizations. The system receives sensitive datasets from data owners, processes them through classification, anonymization, and validation pipelines, and produces compliant datasets suitable for sharing.
### System Context Diagram
*Figure 3.* 
**External Actors**
| **Actor** | **Description** |
|:-:|:-:|
| Data Owner | Healthcare professionals, researchers, or institutional staff who possess sensitive datasets requiring anonymization; responsible for reviewing and approving anonymization results |
| Data Consumer | Researchers, analysts, or authorized personnel who require access to anonymized datasets for analysis |
| Data Protection Officer | Institutional compliance officer responsible for privacy oversight and regulatory adherence |
| System Administrator | Technical personnel responsible for system operation and maintenance |
| Auditor | Internal or external compliance auditor verifying regulatory adherence |
| Peer Institution Node | External Saudi Anonymization and Data Masking Network instance operated by a partner institution |
*Table 16.* 
### 5.2.2 High-Level Architecture
The Saudi Anonymization and Data Masking Network comprises seven microservices supported by three infrastructure components. Each microservice fulfills a single responsibility within the anonymization pipeline, communicating through asynchronous message queues for coordination and internal HTTP endpoints for file transfer.

*Figure 4.* 
### High-Level Architecture
**Microservices**
| **Service** | **Responsibility** |
|:-:|:-:|
| Orchestrator | Single entry point for all external requests; job registration and status tracking; user approval workflow management; initiates processing pipeline |
| NLP Service | Detects personally identifiable information in unstructured text fields; supports Arabic and English languages |
| Masking Service | Applies transformation techniques including suppression, generalization, pseudonymization, date shifting, and redaction |
| Validation Service | Performs column classification and calculates privacy metrics (k-anonymity, l-diversity, t-closeness) and utility metrics (GIL, suppression rate) |
| Storage Service | Manages five-phase storage lifecycle; enforces retention policies; handles file operations; receives files via internal HTTP endpoints |
| Audit Service | Maintains tamper-evident Merkle-chained logs; records all system events for compliance |
| Federation Gateway | Enables secure data sharing with peer institutions via mutual TLS on port 8443 |
*Table 17.* 
**Infrastructure Components**
| **Component** | **Purpose** |
|:-:|:-:|
| PostgreSQL | Stores job metadata, user accounts, classification results, privacy metrics, audit records, and federation agreements |
| RabbitMQ | Message broker enabling asynchronous coordination between microservices |
| MinIO | S3-compatible object storage for dataset files across all storage phases |
*Table 18.* 
### 5.2.3 Communication Patterns
The Saudi Anonymization and Data Masking Network employs three distinct communication patterns to address different operational requirements.
**External Communication**
External actors interact with the system through RESTful APIs exposed exclusively by the Orchestrator service. All external communications are secured using TLS 1.3 encryption. No other service exposes external endpoints.
| **Endpoint Category** | **Examples** | **Purpose** |
|:-:|:-:|:-:|
| Job Management | POST /api/v1/jobs, GET /api/v1/jobs/{job_id} | Submit datasets, check status |
| Results Access | GET /api/v1/jobs/{job_id}/download, GET /api/v1/jobs/{job_id}/report | Retrieve anonymized data and metrics |
| User Decisions | POST /api/v1/jobs/{job_id}/approve, POST /api/v1/jobs/{job_id}/reject | Approve or reject anonymization results |
| Federation | POST /api/v1/federation/share/{job_id} | Initiate secure sharing with peer institutions |
*Table 19.* 
**Internal Communication**
Microservices communicate through two mechanisms, each optimized for its purpose:
| **Mechanism** | **Used For** | **Examples** |
|:-:|:-:|:-:|
| RabbitMQ Queues | Workflow coordination, event notification | Classification requests, masking triggers, audit events |
| Internal HTTP | File transfer (up to 500MB) | Orchestrator uploading files to Storage Service; Masking Service sending masked files to Storage Service |
*Table 20.* 
Internal HTTP endpoints follow the /internal/* naming convention and are accessible only within the Docker network. This hybrid approach ensures loose coupling for workflow coordination while providing efficient binary transfer for large files.
**Queue Topology**
| **Queue** | **Publishers** | **Consumer** | **Purpose** |
|:-:|:-:|:-:|:-:|
| storage_queue | Validation Service | Storage Service | Phase transition commands |
| validation_queue | Storage Service, Masking Service | Validation Service | Classification and privacy validation requests |
| nlp_queue | Validation Service | NLP Service | Text analysis requests for Free Text columns |
| masking_queue | Validation Service, NLP Service | Masking Service | Transformation requests with classification configuration |
| audit_queue | All services | Audit Service | Event logging for compliance |
*Table 21.* 
**Federation Communication**
The Federation Gateway enables secure data exchange with peer Saudi Anonymization and Data Masking Network instances. Federation communication employs mutual TLS authentication on port 8443, separated from standard API traffic.
### 5.2.4 Data Flow Overview
Data progresses through the Saudi Anonymization and Data Masking Network in a sequential pipeline, transitioning through five storage phases as it moves from raw input to validated output.
**Pipeline Summary**
Upon receiving a dataset from a Data Owner, the system performs intake validation, classifies columns to determine appropriate transformation techniques, applies anonymization transformations, validates privacy metrics, and awaits user approval. The Data Owner reviews the privacy and utility metrics, then explicitly approves or rejects the result. Upon approval, the anonymized dataset moves to the safe phase and the original is deleted. Upon rejection or validation failure, both files move to quarantine.

*Figure 5.* 
### Data Flow Pipeline
**Storage Phases**
| **Phase** | **Purpose** | **Contents** | **Retention** |
|:-:|:-:|:-:|:-:|
| intake | Initial upload and validation | original.csv | Temporary (until validation completes) |
| staging | Active processing | original.csv + masked.csv | Until user decision |
| safe | Validated and approved output | masked.csv only | 5 years |
| quarantine | Failed validation or user rejection | original.csv + masked.csv | 30 days |
| archive | Long-term retention | masked.csv (compressed) | 7 years |
*Table 22.* 
**File Handling Rules**
| **Rule** | **Description** |
|:-:|:-:|
| Original file preserved | original.csv stays in staging/ until user approves or rejects |
| Only masked.csv to safe/ | When user approves, only masked.csv moves to safe/ |
| Original deleted on approval | After user approves, original.csv is deleted from staging/ |
| Both to quarantine on rejection | If user rejects OR metrics fail, both files move to quarantine/ |
*Table 23.* 
The detailed processing steps, conditional logic, and service interactions are documented in Section 5.3: Subsystem Architecture.
### 5.2.5 Job Status Lifecycle
Jobs progress through a defined set of statuses that provide visibility into processing progress:
| **Status** | **Meaning** | **Triggered By** |
|:-:|:-:|:-:|
| PENDING | Job created, file received | Orchestrator upon job submission |
| INTAKE_VALIDATING | Storage Service validating file integrity, format, security | Storage Service upon receiving file |
| CLASSIFYING | Validation Service analyzing columns | Validation Service upon receiving classification request |
| NLP_PROCESSING | NLP Service detecting PII in text columns | NLP Service upon receiving NLP request (conditional) |
| MASKING | Masking Service applying transformations | Masking Service upon receiving masking request |
| VALIDATING_PRIVACY | Validation Service calculating privacy metrics | Validation Service upon receiving validation request |
| AWAITING_APPROVAL | Metrics calculated, waiting for user decision | Validation Service upon successful metric calculation |
| COMPLETED | User approved, masked file available in safe/ | Storage Service upon successful phase transition |
| FAILED | Validation failed OR user rejected | Validation Service or Orchestrator |
*Table 24.* 
### 5.2.6 Technology Stack
| **Category** | **Technology** | **Purpose** |
|:-:|:-:|:-:|
| API Framework | FastAPI | RESTful API for Orchestrator and Python services |
| Runtime (Python) | Python 3.11+ | Primary language for six microservices |
| Runtime (.NET) | .NET 8.0 | Runtime for Masking Service |
| NLP Framework | spaCy 3.7+ | PII detection with Arabic language support |
| Message Broker | RabbitMQ 3.12+ | Asynchronous inter-service communication |
| Database | PostgreSQL 15+ | Metadata, audit logs, and job state storage |
| Object Storage | MinIO | S3-compatible file storage for all phases |
| Containerization | Docker 24.0+ | Service isolation and deployment |
| Encryption (At Rest) | AES-256-GCM | Data encryption in storage |
| Encryption (In Transit) | TLS 1.3 | Secure network communications |
*Table 25.* 

### 3 Subsystem Architecture

⠀**5.3.1 Overview**
This section provides a detailed decomposition of the subsystems introduced in Section 5.2. The Saudi Anonymization and Data Masking Network follows a functional description approach, documenting the internal structure of each microservice, the data transformations performed at each processing stage, and the interfaces through which services communicate.
The architectural decomposition presented herein serves two purposes. First, it establishes a clear understanding of how each microservice fulfills its designated responsibility within the overall system architecture. Second, it documents the interfaces and message formats that enable loosely coupled communication between services. The detailed implementation specifications, including algorithm pseudocode, database schemas, and API request/response examples, are reserved for Section 6: Detailed System Design.
The processing pipeline forms the backbone of the system's data transformation capabilities. Understanding this pipeline is essential before examining individual service architectures, as each service's design is informed by its position and responsibilities within the overall flow.

**5.3.2 Processing Pipeline Decomposition**
The data processing pipeline transforms sensitive datasets into privacy-compliant outputs through a sequence of discrete steps. Each step is executed by a dedicated microservice, ensuring clear separation of concerns and enabling independent scaling and failure isolation.
The pipeline begins when a Data Owner submits a dataset through the Orchestrator's REST API. The Orchestrator creates a job record in PostgreSQL and transfers the file to the Storage Service via internal HTTP endpoint. From this point forward, the pipeline operates asynchronously, with each service consuming messages from its designated queue and publishing results to the next service in the sequence.

*Figure 6.* 
### Detailed Processing Pipeline
**5.3.2.1 Processing Steps**
The following table summarizes the processing steps, identifying the responsible service, the action performed, and the storage phase in which data resides during each step:
| **Step** | **Service** | **Action** | **Storage Phase** |
|:-:|:-:|:-:|:-:|
| 1 | Orchestrator | Receives upload request; creates job record in PostgreSQL; transfers file to Storage Service | - |
| 2 | Storage Service | Validates file integrity, format, and security via IntakeValidator module | intake |
| 3 | Storage Service | Moves validated file to staging phase; publishes classification request | staging |
| 4 | Validation Service | Classifies columns as Direct Identifier, Quasi-Identifier, Sensitive, or Free Text | staging |
| 5 | NLP Service | Detects PII in Free Text columns (conditional: executes only if Free Text columns exist) | staging |
| 6 | Masking Service | Applies transformations based on classification configuration; sends masked file to Storage Service | staging |
| 7 | Validation Service | Calculates privacy, risk, and utility metrics; determines pass or fail | staging |
| 8 | User Decision | Data Owner reviews metrics and approves or rejects (conditional: only if metrics pass) | staging |
| 9 | Storage Service | Moves approved data to safe phase (masked only); moves rejected/failed data to quarantine phase (both files) | safe / quarantine |
*Table 26.* 
**5.3.2.2 Conditional Processing Paths**
The pipeline includes two conditional branches that optimize processing based on data characteristics and validation outcomes:
**NLP Conditional Path (Step 5):** The Validation Service, upon completing column classification in Step 4, examines whether any columns have been classified as Free Text. Free Text columns are identified through a combination of signals: column names containing keywords such as "notes", "comment", or "description"; average text length exceeding 50 characters; or low pattern uniformity indicating unstructured content. If Free Text columns are present, the Validation Service publishes a message to the NLP queue, and the pipeline proceeds through the NLP Service before reaching the Masking Service. If no Free Text columns are detected, the pipeline bypasses the NLP Service entirely, publishing directly to the masking queue.
**User Approval Conditional Path (Step 8):** Following privacy metric calculation, the pipeline behavior depends on whether metrics pass or fail minimum thresholds:
| **Outcome** | **Action** |
|:-:|:-:|
| Metrics PASS | Job status set to AWAITING_APPROVAL; Data Owner reviews metrics via report endpoint; explicit approval or rejection required |
| Metrics FAIL | Job status set to FAILED; Storage Service automatically moves files to quarantine; no user decision required |
*Table 27.* 
This approval workflow ensures Data Owners verify anonymization quality before data becomes available, supporting PDPL requirements for data subject control and enabling review of privacy-utility trade-offs.
**5.3.2.3 Storage Phases**
The storage phases through which data transitions during processing serve distinct purposes and are governed by retention policies aligned with regulatory requirements:
| **Phase** | **Purpose** | **Contents** | **Retention Period** |
|:-:|:-:|:-:|:-:|
| intake | Initial upload validation; malware scanning and format verification | original.csv | Temporary (until validation completes) |
| staging | Active processing; data undergoes classification, transformation, and validation | original.csv + masked.csv | Until user decision |
| safe | Validated and approved output; compliant datasets available for download or federation | masked.csv only | 5 years |
| quarantine | Failed validation or user rejection; retained for review and potential reprocessing | original.csv + masked.csv | 30 days |
| archive | Long-term retention; compressed storage for regulatory compliance | masked.csv (compressed) | 7 years |
*Table 28.* 
These retention periods are derived from Ministry of Health IS0303 requirements, which mandate seven-year retention for healthcare records, and institutional policies that establish 30-day quarantine periods for failed datasets to permit investigation and remediation.
**5.3.2.4 File Handling Rules**
The pipeline enforces strict file handling rules to ensure privacy compliance and data integrity:
| **Rule** | **Description** | **Rationale** |
|:-:|:-:|:-:|
| Original file preserved | original.csv remains in staging/ until user explicitly approves or rejects | Enables re-processing if masking parameters require adjustment |
| Only masked.csv to safe/ | Upon approval, only the anonymized file moves to the safe phase | Original data with PII never enters the accessible safe phase |
| Original deleted on approval | After user approves, original.csv is deleted from staging/ | Data minimization principle; PII retained only as long as necessary |
| Both to quarantine on rejection | If user rejects OR metrics fail, both files move to quarantine/ | Preserves evidence for investigation; enables remediation attempts |
*Table 29.* 

**5.3.3 Orchestrator Service**
The Orchestrator Service functions as the sole entry point for all external interactions with the Saudi Anonymization and Data Masking Network. This architectural decision centralizes authentication, authorization, and request validation at a single point, simplifying security enforcement and providing a consistent interface for all external actors regardless of the underlying processing complexity.
The Orchestrator does not perform data transformation itself. Rather, it delegates processing to specialized services through a combination of internal HTTP calls (for file transfer) and asynchronous message publication (for workflow coordination). This delegation pattern ensures that the Orchestrator remains responsive to client requests even when processing pipelines require extended execution times. Clients submit jobs and receive immediate acknowledgment; subsequent status queries allow clients to monitor progress without blocking.
**5.3.3.1 Internal Modules**
The internal architecture of the Orchestrator comprises five modules, each addressing a distinct aspect of request handling and coordination:
| **Module** | **Responsibility** |
|:-:|:-:|
| API Controller | Exposes RESTful endpoints for job submission, status queries, result retrieval, and user decisions; validates request payloads against defined schemas |
| Job Manager | Creates and tracks job records in PostgreSQL; manages job state transitions through the processing lifecycle |
| File Transfer Handler | Transfers uploaded files to Storage Service via internal HTTP endpoint; handles large file streaming |
| Queue Publisher | Publishes audit events to RabbitMQ queues; handles connection pooling and retry logic |
| Authentication Handler | Validates user credentials against the institution's identity provider; enforces role-based access control policies |
*Table 30.* 
The API Controller module implements the external interface specification. All endpoints follow RESTful conventions, using standard HTTP methods and returning responses in JSON format. Request validation occurs at this layer, rejecting malformed requests before they reach internal processing logic.
The Job Manager module maintains job state within PostgreSQL, enabling persistent tracking of processing progress. Job states include PENDING, INTAKE_VALIDATING, CLASSIFYING, NLP_PROCESSING, MASKING, VALIDATING_PRIVACY, AWAITING_APPROVAL, COMPLETED, and FAILED. State transitions are recorded with timestamps, providing a complete audit trail of job progression.
**5.3.3.2 Interface Specification**
The Orchestrator exposes seven endpoints through which external actors interact with the system:
| **Endpoint** | **Method** | **Description** | **Authorization** |
|:-:|:-:|:-:|:-:|
| /api/v1/jobs | POST | Submit new anonymization job with dataset file | Data Owner, System Administrator |
| /api/v1/jobs/{job_id} | GET | Retrieve job status, current phase, and metadata | Data Owner (own jobs), DPO, System Administrator |
| /api/v1/jobs/{job_id}/download | GET | Download anonymized dataset upon successful completion | Data Owner (own jobs), Data Consumer (with approval) |
| /api/v1/jobs/{job_id}/report | GET | Retrieve validation report including privacy and utility metrics | Data Owner (own jobs), DPO, Auditor |
| /api/v1/jobs/{job_id}/approve | POST | Approve anonymization result; triggers transition to safe phase | Data Owner (own jobs) |
| /api/v1/jobs/{job_id}/reject | POST | Reject anonymization result; triggers transition to quarantine phase | Data Owner (own jobs) |
| /api/v1/federation/share/{job_id} | POST | Initiate secure sharing with peer institution | Data Owner (own jobs), DPO |
*Table 31.* 
Authorization requirements vary by endpoint and are enforced by the Authentication Handler module. The role-based access control model permits Data Owners to access only their own jobs, while Data Protection Officers and System Administrators have broader visibility for oversight purposes.
**5.3.3.3 Internal Service Calls**
The Orchestrator communicates with other services through internal HTTP endpoints for file operations:
| **Target Service** | **Endpoint** | **Purpose** |
|:-:|:-:|:-:|
| Storage Service | POST /internal/files/{job_id} | Transfer uploaded file for intake validation |
| Storage Service | POST /internal/files/{job_id}/approve | Trigger phase transition to safe upon user approval |
| Storage Service | POST /internal/files/{job_id}/reject | Trigger phase transition to quarantine upon user rejection |
| Federation Gateway | POST /internal/federation/share/{job_id} | Initiate federated transfer to peer institution |
*Table 32.* 
These internal endpoints are accessible only within the Docker network and are not exposed to external actors.
**5.3.3.4 Queue Publications**
The Orchestrator publishes audit events to record significant actions:
| **Queue** | **Event Type** | **Trigger** |
|:-:|:-:|:-:|
| audit_queue | JOB_CREATED | Upon successful job submission |
| audit_queue | JOB_APPROVED | Upon user approval of anonymization result |
| audit_queue | JOB_REJECTED | Upon user rejection of anonymization result |
*Table 33.* 
The separation of user actions and audit logging into distinct operations ensures that audit records are created for all significant decisions, providing compliance evidence for regulatory review.
**5.3.3.5 MinIO Access**
The Orchestrator requires read access to MinIO for serving download requests:
| **Phase** | **Access** | **Purpose** |
|:-:|:-:|:-:|
| safe/ | READ | Serve masked file downloads to authorized users |
*Table 34.* 
The Orchestrator does not write directly to MinIO; all file storage operations are delegated to the Storage Service.
**5.3.4 Storage Service**
The Storage Service manages the five-phase storage lifecycle that governs dataset progression through the processing pipeline. This service handles all file operations, receiving files via internal HTTP endpoints and managing phase transitions based on queue messages.
The decision to centralize storage operations within a dedicated service reflects the architectural principle of single responsibility. Other services interact with datasets through messages that reference file paths and read directly from MinIO for processing, but all write operations flow through the Storage Service. This pattern ensures consistent enforcement of storage policies and simplifies audit logging of file operations.
**5.3.4.1 Internal Modules**
The Storage Service comprises four modules that collectively manage file operations and lifecycle enforcement:
| **Module** | **Responsibility** |
|:-:|:-:|
| IntakeValidator | Performs checksum verification, malware scanning via ClamAV integration, format validation, and size limit enforcement (maximum 500 MB per file) |
| Phase Manager | Executes atomic file transitions between storage phases; ensures consistency through transaction-like semantics |
| Retention Enforcer | Background process that monitors file ages and enforces retention policies; triggers archival and deletion operations |
| File Handler | Abstracts MinIO operations for upload, download, move, and delete; manages connection pooling and error handling |
*Table 35.* 
**5.3.4.2 Interface Specification**
The Storage Service exposes four internal HTTP endpoints:
| **Endpoint** | **Method** | **Description** | **Called By** |
|:-:|:-:|:-:|:-:|
| /internal/files/{job_id} | POST | Receive file from Orchestrator; initiate intake validation | Orchestrator |
| /internal/files/{job_id}/approve | POST | Move masked.csv to safe/; delete staging files | Orchestrator |
| /internal/files/{job_id}/reject | POST | Move both files to quarantine/ | Orchestrator |
*Table 36.* 
**5.3.4.3 Intake Validation Process**
The IntakeValidator module serves as the first line of defense against malformed or malicious uploads. Files must pass five validation checks before proceeding to the staging phase:
| **Step** | **Validation** | **On Success** | **On Failure** |
|:-:|:-:|:-:|:-:|
| 1 | Receive file; write to intake/{job_id}/original.csv | Proceed to step 2 | Reject upload; return error |
| 2 | Checksum verification (confirm file integrity during transfer) | Proceed to step 3 | Mark job FAILED; delete file |
| 3 | ClamAV malware scan (detect known threats) | Proceed to step 4 | Mark job FAILED; delete file |
| 4 | Format validation (confirm supported type: CSV, JSON, Parquet, XLSX) | Proceed to step 5 | Mark job FAILED; delete file |
| 5 | Size validation (confirm ≤ 500 MB) | Proceed to step 6 | Mark job FAILED; delete file |
| 6 | All passed | Move to staging/; publish to validation_queue | - |
*Table 37.* 
**5.3.4.4 Queue Interactions**
The Storage Service consumes from and publishes to the following queues:
**Consumes from storage_queue:**
| **Action** | **Trigger** | **Operation** |
|:-:|:-:|:-:|
| MOVE_TO_QUARANTINE | Validation Service determines metrics fail | Move staging/{job_id}/ to quarantine/{job_id}/ (both files) |
*Table 38.* 
**Publishes to validation_queue:**
| **Message** | **Trigger** | **Content** |
|:-:|:-:|:-:|
| CLASSIFY | Intake validation passes | {job_id, file_path, action: CLASSIFY} |
*Table 39.* 
**Publishes to audit_queue:**
| **Event Type** | **Trigger** |
|:-:|:-:|
| INTAKE_VALIDATED | File passes all intake validation checks |
| PHASE_TRANSITION | File moves between storage phases |
*Table 40.* 
**5.3.4.5 Phase Transition Logic**
Phase transitions are governed by explicit triggers and conditions:
| **From Phase** | **To Phase** | **Trigger** | **Condition** |
|:-:|:-:|:-:|:-:|
| - | intake | File received via HTTP | Always (initial state) |
| intake | staging | Intake validation complete | IntakeValidator returns success |
| intake | (rejected) | Intake validation complete | IntakeValidator returns failure |
| staging | safe | User approval via Orchestrator | Job status is AWAITING_APPROVAL; approval endpoint called |
| staging | (deleted) | Retention period expired | File age exceeds 7 days (scheduled job) |
| staging | quarantine | User rejection OR validation failure | Rejection endpoint called OR MOVE_TO_QUARANTINE message received |
| safe | archive | Retention threshold reached | File age exceeds 5 years (scheduled job) |
| quarantine | (deleted) | Retention period expired | File age exceeds 30 days (scheduled job) |
*Table 41.* 
The Phase Manager implements transitions as atomic operations. When moving files from staging to safe upon approval:
1 Copy masked.csv to safe/{job_id}/masked.csv
2 Verify copy integrity via checksum
3 Update job record in PostgreSQL (status: COMPLETED, phase: safe)
4 Delete staging/{job_id}/ directory (both original.csv and masked.csv)
5 Publish PHASE_TRANSITION event to audit_queue

⠀This sequence ensures that system failures during transition do not result in data loss or inconsistent state.
**5.3.4.6 Archive Process**
The archive process is triggered by a scheduled background job, not by the main processing pipeline:
| **Step** | **Action** |
|:-:|:-:|
| 1 | Scheduled job runs daily |
| 2 | Query PostgreSQL for jobs in safe/ phase older than 5 years |
| 3 | For each qualifying job: compress masked.csv using gzip |
| 4 | Move to archive/{job_id}/masked.csv.gz |
| 5 | Update job record in PostgreSQL (phase: archive) |
| 6 | Publish PHASE_TRANSITION event to audit_queue |
*Table 42.* 
**Archive Retention & Secure Deletion**
Archived jobs are retained for a total of 7 years from original intake. After 7 years, archived datasets SHALL be securely deleted with:
* Scheduled job runs daily to check archive age
* Query PostgreSQL for jobs in archive/ phase older than 7 years
* Secure deletion of archived files
* Update job record in PostgreSQL (status: DELETED)
* Publish RETENTION_CLEANUP_EXECUTED event to audit_queue

⠀**5.3.5 Validation Service**
The Validation Service performs two distinct functions within the processing pipeline: column classification prior to masking and privacy metrics validation after masking. This dual responsibility reflects the service's core competency in data analysis and assessment, applied at two different stages of the pipeline for different purposes.
The decision to consolidate these functions within a single service, rather than creating separate Classification and Validation services, was evaluated during architectural design. The analysis determined that both functions share common analytical capabilities, including statistical analysis, pattern recognition, and metric calculation. Separating them would introduce additional network latency and operational complexity without commensurate benefit. The service maintains clear internal separation between classification and validation modules, preserving conceptual clarity while optimizing operational efficiency.
**5.3.5.1 Internal Modules**
The Validation Service comprises six modules organized into two functional groups:
**Classification Modules:**
| **Module** | **Responsibility** |
|:-:|:-:|
| Column Classifier | Analyzes column names, data patterns, and statistical distributions to classify each column |
| Classification Engine | Applies weighted scoring algorithm to determine column type with associated confidence level |
*Table 43.* 
**Validation Modules:**
| **Module** | **Responsibility** |
|:-:|:-:|
| Privacy Calculator | Computes k-anonymity, l-diversity, and t-closeness metrics for masked datasets |
| Risk Assessor | Calculates re-identification risk scores based on quasi-identifier combinations |
| Utility Calculator | Computes information loss metrics including GIL, suppression rate, and discernibility |
| Report Generator | Produces validation reports documenting metrics, pass/fail determination, and recommendations |
*Table 44.* 
**5.3.5.2 Classification Engine**
The Classification Engine employs a weighted scoring algorithm that evaluates multiple signals to determine column type. Each signal category contributes points to the classification decision, and the column type with the highest aggregate score is assigned.
**Signal Weights:**
| **Signal Category** | **Maximum Points** | **Description** |
|:-:|:-:|:-:|
| Column Name Patterns | 30 points | Matches against keyword patterns such as *_id, name, phone, email, notes, comment |
| Data Pattern Matching | 40 points | Detection of Saudi-specific patterns including National ID, IBAN, phone numbers, and email formats |
| Statistical Analysis | 25 points | Uniqueness ratio, cardinality, and value distribution characteristics |
| Text Length Analysis | 35 points | Average character count and text structure indicators |
*Table 45.* 
**Confidence Calculation:**
The confidence level for each classification is computed as:
Confidence = highest_category_score / total_possible_score
For example, if a column scores 40 points from data pattern matching (National ID detected) and 25 points from statistical analysis (uniqueness > 90%), the total score is 65 points. If the maximum possible score is 130 points, the confidence level is 50%. However, because the National ID pattern is a definitive signal, the Classification Engine applies pattern-specific overrides that elevate confidence to 95% for known Saudi identifier formats.
**Confidence-Based Actions:**
| **Confidence Level** | **Action** |
|:-:|:-:|
| ≥ 90% | Classification applied automatically without human intervention |
| 70% – 89% | Classification applied with warning flag; logged for potential review |
| 50% – 69% | Flagged for manual review; processing pauses until confirmed |
| < 50% | Requires mandatory human classification before processing continues |
*Table 46.* 
**Classification Categories:**
| **Column Type** | **Detection Signals** | **Assigned Transformation** |
|:-:|:-:|:-:|
| Direct Identifier | Column names matching patterns (*_id, name, phone, email); uniqueness exceeding 90%; Saudi National ID pattern (^1\d{9});IQAMApattern(2\d9); IQAMA pattern (^2\d{9}<br>);IQAMApattern(2\d9) | SUPPRESS |
| Quasi-Identifier | Column names matching demographic patterns (age, gender, city, *_date); uniqueness between 10% and 90% | GENERALIZE |
| Sensitive Attribute | Column names indicating protected information (diagnosis, treatment, salary); low uniqueness; high sensitivity classification | KEEP (protected by k-anonymity) |
| Free Text | Column names containing text indicators (notes, comment, description); average text length exceeding 50 characters; low pattern uniformity | NLP_REDACT |
*Table 47.* 
**5.3.5.3 Privacy Metrics**
Following masking operations, the Validation Service calculates privacy metrics to verify that the transformed dataset meets regulatory thresholds. The privacy assessment encompasses three categories of metrics.
**Anonymity Metrics:**
| **Metric** | **Definition** | **Minimum Threshold** | **Target Threshold** |
|:-:|:-:|:-:|:-:|
| k-Anonymity | Each record is indistinguishable from at least k-1 other records based on quasi-identifiers | k ≥ 5 (research use) | k ≥ 10 (PDPL compliance) |
| l-Diversity | Each equivalence class contains at least l distinct values for sensitive attributes | l ≥ 2 (minimum) | l ≥ 3 (healthcare data) |
| t-Closeness | Distribution of sensitive attributes within each equivalence class differs from overall distribution by at most t | t ≤ 0.20 | t ≤ 0.15 |
*Table 48.* 
**Re-identification Risk Metrics:**
The Validation Service calculates three distinct risk scores, each modeling a different adversarial scenario:
| **Risk Type** | **Definition** | **Formula** | **Maximum Threshold** |
|:-:|:-:|:-:|:-:|
| Prosecutor Risk | Probability of identifying a specific targeted individual known to be in the dataset | 1/k_min | < 20% (min), < 10% (target) |
| Journalist Risk | Probability of identifying any individual from the dataset | num_classes/|D| | < 33% (min), < 20% (target) |
| Marketer Risk | Expected fraction of records that can be re-identified across the entire dataset | Σ(1/|Eᵢ|)/|D| | < 20% (min), < 10% (target) |
*Table 49.* 
The prosecutor risk model assumes an adversary who knows a specific individual is present in the dataset and possesses the individual's quasi-identifier values. The journalist risk model assumes an adversary attempting to identify anyone from the dataset, regardless of prior knowledge. The marketer risk model estimates the expected number of successful re-identifications across all records, relevant when an adversary seeks to identify as many individuals as possible.
**5.3.5.4 Utility Metrics**
In addition to privacy metrics, the Validation Service calculates utility metrics to quantify information loss resulting from anonymization. These metrics enable Data Owners to assess the privacy-utility trade-off and adjust anonymization parameters if the resulting dataset suffers excessive information loss.
| **Metric** | **Definition** | **Threshold** | **Pass/Fail?** |
|:-:|:-:|:-:|:-:|
| Generalization Information Loss (GIL) | Average ratio of generalized range to domain size across all quasi-identifiers | < 40% | Yes |
| Suppression Rate | Percentage of records removed to achieve k-anonymity | < 15% | Yes |
| Discernibility Metric (DM) | Normalized sum of squared equivalence class sizes: Σ|Eᵢ|² / |D|² | Lower is better; typical range 0.01-0.10 | No (report only) |
| Average Equivalence Class Size | Total records divided by number of equivalence classes: |D| / num_classes | Reported for analysis | No (report only) |
*Table 50.* 
The Generalization Information Loss metric quantifies precision degradation. For example, generalizing age from exact values to 10-year ranges (e.g., 34 → 30-40) introduces a GIL of approximately 10% for that attribute if the domain spans 100 years. High GIL values indicate that the anonymized data may be too imprecise for certain analytical purposes.
The Suppression Rate measures data loss. If achieving k-anonymity requires suppressing more than 15% of records, the validation report recommends reviewing the generalization hierarchy or relaxing the k threshold if permissible under the applicable data use agreement.
**5.3.5.5 Queue Interactions**
**Consumes from validation_queue:**
| **Action** | **Source** | **Operation** |
|:-:|:-:|:-:|
| CLASSIFY | Storage Service | Perform column classification; route to NLP or Masking |
| VALIDATE_PRIVACY | Masking Service | Calculate privacy, risk, and utility metrics |
*Table 51.* 
**Publishes to nlp_queue (conditional):**
| **Condition** | **Message Content** |
|:-:|:-:|
| Free Text columns detected | {job_id, file_path, text_columns, classification_config} |
*Table 52.* 
**Publishes to masking_queue:**
| **Condition** | **Message Content** |
|:-:|:-:|
| No Free Text columns | {job_id, file_path, classification_config} |
*Table 53.* 
**Publishes to storage_queue:**
| **Condition** | **Message Content** |
|:-:|:-:|
| Metrics FAIL | {action: MOVE_TO_QUARANTINE, job_id, failure_reasons} |
*Table 54.* 
**Publishes to audit_queue:**
| **Event Type** | **Trigger** |
|:-:|:-:|
| CLASSIFICATION_COMPLETE | Column classification finished |
| VALIDATION_COMPLETE | Privacy metrics calculation finished (includes pass/fail result) |
*Table 55.* 
**5.3.5.6 PostgreSQL Interactions**
| **Operation** | **Table** | **Trigger** |
|:-:|:-:|:-:|
| UPDATE | jobs | Status transitions: CLASSIFYING, VALIDATING_PRIVACY, AWAITING_APPROVAL, FAILED |
| INSERT | classification_results | Column classification complete |
| INSERT | privacy_metrics | Privacy and risk metrics calculated |
| INSERT | utility_metrics | Utility metrics calculated |
*Table 56.* 
**5.3.6 NLP Service**
The NLP Service detects personally identifiable information within unstructured text columns, addressing a category of privacy risk that cannot be mitigated through traditional tabular anonymization techniques. Free text fields, such as clinical notes or case descriptions, may contain names, identification numbers, and other sensitive information embedded within narrative content.
The service supports both Arabic and English languages, reflecting the bilingual nature of documentation within Saudi healthcare and educational institutions. Language detection occurs automatically, enabling the service to select the appropriate processing model without requiring explicit language specification from upstream services.
**5.3.6.1 Internal Modules**
The NLP Service comprises four modules that collectively implement the detection pipeline:
| **Module** | **Responsibility** |
|:-:|:-:|
| Language Detector | Analyzes text samples to identify the primary language; supports Arabic, English, and mixed-language content |
| Entity Recognizer | Executes named entity recognition using spaCy pipelines; identifies persons, organizations, locations, and dates |
| Pattern Matcher | Applies regular expression patterns to detect structured PII such as National IDs, IBANs, and phone numbers |
| Annotation Generator | Produces redaction annotations specifying entity positions, types, and suggested replacement tokens |
*Table 57.* 
The Entity Recognizer module utilizes spaCy's transformer-based models for both Arabic and English. The Arabic model (ar_core_news_lg) provides named entity recognition capabilities trained on Arabic news corpora, while the English model (en_core_web_trf) offers state-of-the-art accuracy for English text. For mixed-language documents, the service processes text segments independently based on detected language.
**5.3.6.2 Supported Entity Types**
The NLP Service detects the following entity types, employing either statistical models or pattern matching as appropriate. Entities are processed in priority order to resolve pattern overlaps:
| **Priority** | **Entity Type** | **Examples** | **Detection Method** |
|:-:|:-:|:-:|:-:|
| 1 | IQAMA | 2123456789 | Regex pattern: ^2\d{9}$ (checked first to resolve overlap with National ID) |
| 2 | NATIONAL_ID | 1234567890 | Regex pattern: ^1\d{9}$ |
| 3 | IBAN | SA1234567890123456789012 | Regex pattern: ^SA\d{22}$ |
| 4 | PHONE | +966501234567, 0501234567 | Regex pattern: ^(+966|00966|05|5)\d{8,9}$ |
| 5 | EMAIL | user@domain.com | Regex pattern for standard email format |
| 6 | PERSON | Ahmed Al-Saud, محمد العلي | spaCy NER; Saudi name list matching |
| 7 | LOCATION | Dammam, الدمام, Eastern Province | spaCy NER; Saudi city/district list |
| 8 | ORGANIZATION | ARAMCO, SABIC, STC, Ministry of Health | spaCy NER; Saudi organization list |
| 9 | DATE | 2024-03-15, 15 مارس 2024 | spaCy NER with custom date patterns |
| 10 | MEDICAL_RECORD | MRN-12345, MRN12345 | Custom regex patterns |
| 11 | INSURANCE_ID | INS123456 | Regex pattern: ^INS\d{6}$ |
*Table 58.* 
**Note on IQAMA vs NATIONAL_ID:** IQAMA numbers start with 2, Saudi National IDs start with 1. To avoid overlap, IQAMA pattern is checked first. If a 10-digit number starts with 2, it's classified as IQAMA. If it starts with 1, it's classified as NATIONAL_ID. Context from column names (e.g., "iqama_number", "national_id") can override pattern-based detection.
The combination of statistical and pattern-based detection ensures comprehensive coverage. Statistical models excel at identifying entities that vary in form, such as person names and locations. Pattern matching provides precise detection of structured identifiers that follow predictable formats, such as National IDs and IBANs. List-based matching supplements both approaches for Saudi-specific entities.
**5.3.6.3 Queue Interactions**
The NLP Service communicates asynchronously using RabbitMQ message queues, including nlp_queue for task consumption, masking_queue for downstream signaling, and audit_queue for governance events.  Failed or unrecoverable messages are routed to a dedicated Dead-Letter Queue (nlp_dlq) for inspection and retry handling, as defined in the SRS.
**Consumes from nlp_queue:**
| **Message Content** | **Operation** |
|:-:|:-:|
| {job_id, file_path, text_columns, classification_config} | Process text columns; detect PII entities |
*Table 59.* 
**Publishes to masking_queue:**
| **Message Content** | **Trigger** |
|:-:|:-:|
| {job_id, file_path, classification_config} | NLP processing complete |
*Table 60.* 
**Publishes to audit_queue:**
| **Event Type** | **Trigger** |
|:-:|:-:|
| NLP_COMPLETE | Entity detection finished |
*Table 61.* 
**5.3.6.4 PostgreSQL Interactions**
| **Operation** | **Table** | **Trigger** |
|:-:|:-:|:-:|
| UPDATE | jobs | Status transition: NLP_PROCESSING |
| INSERT | nlp_annotations | Entity detection complete; stores all detected entities with positions |
*Table 62.* 
**5.3.7 Masking Service**
The Masking Service applies transformation techniques to anonymize data based on the classification configuration provided by the Validation Service. This service is implemented in C# using the .NET 8 runtime, diverging from the Python-based implementation of other services. This technology choice reflects the computational intensity of masking operations and the availability of mature cryptographic libraries within the .NET ecosystem.
The service receives classification configurations specifying the transformation technique to apply to each column. For datasets that have passed through the NLP Service, the service also reads annotation data from PostgreSQL identifying PII locations within text fields. The Masking Service applies all specified transformations and sends the masked dataset to the Storage Service via internal HTTP endpoint.
**5.3.7.1 Internal Modules**
The Masking Service comprises six modules, each implementing a specific transformation technique:
| **Module** | **Responsibility** |
|:-:|:-:|
| Transformation Engine | Orchestrates application of transformation techniques per column; manages processing order and dependencies |
| Suppressor | Removes direct identifier columns entirely from the output dataset |
| Generalizer | Applies hierarchical generalization to quasi-identifiers, replacing specific values with broader categories |
| Pseudonymizer | Generates consistent pseudonyms using HMAC-SHA256 with job-specific salts; enables longitudinal analysis while preventing identification |
| Date Shifter | Applies random temporal offset to date columns while preserving relative intervals between dates within the same record |
| Text Redactor | Replaces detected PII entities with placeholder tokens based on NLP annotations |
*Table 63.* 
The Transformation Engine coordinates the application of techniques in a specific order: suppression first (removing columns), followed by date shifting (adjusting temporal values), generalization (modifying categorical and numerical values), pseudonymization (replacing identifiers), and finally text redaction (processing free text). This ordering ensures that dependencies between transformations are respected and that the output dataset is internally consistent.
**5.3.7.2 Transformation Techniques**
| **Technique** | **Applied To** | **Reversibility** | **Example Transformation** |
|:-:|:-:|:-:|:-:|
| Suppression | Direct Identifiers | Irreversible | Column removed entirely from dataset |
| Date Shifting | Date fields requiring interval preservation | Irreversible | Surgery date 2024-01-15 → 2024-03-20 (shifted by +64 days); all dates in record shifted by same offset |
| Generalization | Quasi-Identifiers | Irreversible | Age 34 → Age range 30-40; City "Dammam" → Region "Eastern Province" |
| Pseudonymization | Linkage columns requiring longitudinal consistency | Reversible with key | patient_id "P12345" → pseudonym "a7b3c9d2e1f4" |
| NLP Redaction | Free Text columns | Irreversible | "Ahmed visited the clinic" → "[PERSON] visited the clinic" |
*Table 64.* 
**Date Shifting Considerations:** When multiple date fields exist within a record (e.g., admission_date, surgery_date, discharge_date), the Date Shifter applies an identical offset to all dates, preserving the clinically meaningful intervals between events. For longitudinal datasets where the same patient appears in multiple records, the offset is derived deterministically from the patient identifier, ensuring consistent shifting across all records belonging to the same individual.
**Pseudonymization Considerations:** The technique employs HMAC-SHA256 with a job-specific salt, generating consistent pseudonyms for identical input values within a single job. This consistency enables longitudinal analysis across records belonging to the same individual. The salt is retained in secure storage, permitting authorized re-identification if required by legal process. However, the salt is never transmitted with the anonymized dataset, ensuring that recipients cannot reverse the pseudonymization.
**5.3.7.3 Service Interactions**
**Internal HTTP Call:**
| **Target** | **Endpoint** | **Purpose** |
|:-:|:-:|:-:|
| Storage Service | POST /internal/files/{job_id}/masked | Send masked file for storage in staging/ |
*Table 65.* 
**Queue Interactions:**
**Consumes from masking_queue:**
| **Message Content** | **Operation** |
|:-:|:-:|
| {job_id, file_path, classification_config} | Apply transformations to dataset |
*Table 66.* 
**Publishes to validation_queue:**
| **Message Content** | **Trigger** |
|:-:|:-:|
| {action: VALIDATE_PRIVACY, job_id, masked_file_path} | Masking complete |
*Table 67.* 
**Publishes to audit_queue:**
| **Event Type** | **Trigger** |
|:-:|:-:|
| MASKING_COMPLETE | All transformations applied |
*Table 68.* 
**5.3.7.4 Data Access**
| **Source** | **Access Type** | **Purpose** |
|:-:|:-:|:-:|
| MinIO (staging/) | READ | Read original.csv for transformation |
| PostgreSQL (classification_results) | READ | Retrieve column classifications |
| PostgreSQL (nlp_annotations) | READ | Retrieve entity annotations for text redaction |
| PostgreSQL (jobs) | UPDATE | Status transition: MASKING |
*Table 69.* 
**5.3.8 Audit Service**
The Audit Service maintains tamper-evident logs of all system operations, providing the compliance evidence required by Saudi Personal Data Protection Law and National Cybersecurity Authority Essential Cybersecurity Controls. Every significant system event, from job creation through final phase transition, is recorded in a cryptographically chained log that resists modification and enables verification of log integrity.
The service operates as a terminal node in the message flow architecture. It subscribes to the audit queue, consuming events published by all other services, but publishes no messages itself. This unidirectional flow ensures that audit logging cannot create feedback loops or circular dependencies within the processing pipeline.
**5.3.8.1 Internal Modules**
The Audit Service comprises four modules:
| **Module** | **Responsibility** |
|:-:|:-:|
| Event Consumer | Subscribes to audit_queue; deserializes incoming events; validates event structure |
| Merkle Chain Builder | Computes cryptographic hashes linking each event to its predecessor; maintains chain integrity |
| Log Writer | Persists audit records to PostgreSQL with appropriate indexing for query performance |
| Report Generator | Produces compliance reports in formats aligned with NDMO requirements |
*Table 70.* 
The Merkle Chain Builder module implements the tamper-evidence mechanism. Each audit event includes the SHA-256 hash of the previous event, creating a chain in which modification of any historical event would invalidate all subsequent hashes. Verification of chain integrity can be performed at any time by recomputing hashes and comparing them to stored values.
**5.3.8.2 Audit Event Types**
| **Event Type** | **Source Service** | **Trigger** |
|:-:|:-:|:-:|
| JOB_CREATED | Orchestrator | Job submission accepted |
| INTAKE_VALIDATED | Storage Service | File passes intake validation |
| CLASSIFICATION_COMPLETE | Validation Service | Column classification finished |
| NLP_COMPLETE | NLP Service | Entity detection finished |
| MASKING_COMPLETE | Masking Service | Transformations applied |
| VALIDATION_COMPLETE | Validation Service | Privacy metrics calculated |
| JOB_APPROVED | Orchestrator | User approves anonymization result |
| JOB_REJECTED | Orchestrator | User rejects anonymization result |
| PHASE_TRANSITION | Storage Service | File moves between storage phases |
| FEDERATION_TRANSFER | Federation Gateway | Dataset shared with peer institution |
*Table 71.* 
**5.3.8.3 Audit Record Structure**
Each audit event captures comprehensive information about the recorded operation:
| **Field** | **Type** | **Description** |
|:-:|:-:|:-:|
| event_id | UUID | Unique identifier for this event |
| job_id | UUID | Associated job identifier; null for system events |
| event_type | Enum | Category of event |
| timestamp | ISO 8601 | Time of event occurrence with millisecond precision |
| actor_id | String | User identifier or service name that triggered the event |
| details | JSON | Event-specific payload containing relevant parameters and outcomes |
| previous_hash | String (64 chars) | SHA-256 hash of the preceding event in the chain |
| current_hash | String (64 chars) | SHA-256 hash of this event (computed over all preceding fields) |
*Table 72.* 

**5.3.9 Federation Gateway**
The Federation Gateway enables secure dataset sharing with peer Saudi Anonymization and Data Masking Network instances operated by partner institutions. This capability supports collaborative research scenarios in which anonymized datasets must be shared across organizational boundaries while maintaining compliance with data protection regulations.
The Federation Gateway operates on an outbound-only model for the initial capstone deployment. The local SADN instance can transmit validated datasets to authorized peer institutions, but does not accept inbound transfers. This asymmetric design simplifies security considerations and aligns with the initial deployment scope. Bidirectional federation may be enabled in future releases.
**5.3.9.1 Internal Modules**
The Federation Gateway comprises four modules:
| **Module** | **Responsibility** |
|:-:|:-:|
| Certificate Manager | Manages X.509 certificates for mutual TLS authentication; handles certificate rotation and revocation checking |
| Peer Registry | Maintains list of authorized peer institutions, their endpoints, and associated Data Use Agreements |
| Transfer Handler | Executes encrypted dataset transmission to peer nodes; implements retry logic and transfer verification |
| DUA Validator | Verifies that an active Data Use Agreement exists for the requested transfer; enforces agreement terms |
*Table 73.* 
The Certificate Manager module implements mutual TLS (mTLS) authentication, requiring both the local gateway and the peer gateway to present valid X.509 certificates before establishing a connection. This mutual authentication ensures that datasets are transmitted only to verified peer institutions and that transmission occurs over encrypted channels.
**5.3.9.2 Interface Specification**
| **Endpoint** | **Method** | **Description** | **Called By** |
|:-:|:-:|:-:|:-:|
| POST /internal/federation/share/{job_id} | POST | Initiate federated transfer; body contains {peer_id} | Orchestrator |
*Table 74.* 
**5.3.9.3 Federation Protocol**
The federation process follows a defined sequence of steps:
| **Step** | **Action** | **Responsible Module** |
|:-:|:-:|:-:|
| 1 | Receive transfer request from Orchestrator | - |
| 2 | Verify job status is COMPLETED | Transfer Handler |
| 3 | Verify active Data Use Agreement exists for the peer | DUA Validator |
| 4 | Retrieve peer endpoint and certificate from registry | Peer Registry |
| 5 | Initiate mTLS handshake with peer gateway | Certificate Manager |
| 6 | Read masked file from MinIO safe/{job_id}/ | Transfer Handler |
| 7 | Encrypt and transmit dataset with metadata | Transfer Handler |
| 8 | Receive acknowledgment from peer; verify transfer integrity | Transfer Handler |
| 9 | Record transfer in PostgreSQL | Transfer Handler |
| 10 | Publish audit event | - |
| 11 | Return success response to Orchestrator | - |
*Table 75.* 
Federation communication occurs exclusively on port 8443, separated from the standard HTTPS port used for API traffic. This port separation enables network-level access controls that restrict federation traffic to authorized peer networks.
**5.3.9.4 Federation Rules**
| **Rule** | **Description** |
|:-:|:-:|
| Outbound only | For capstone, only SEND to peers (no inbound) |
| Only safe/ files | Can only share jobs with status COMPLETED |
| DUA required | Must have active Data Use Agreement with peer |
| mTLS required | Port 8443 with mutual TLS authentication |
*Table 76.* 
**5.3.9.5 Queue Publications**
| **Queue** | **Event Type** | **Trigger** |
|:-:|:-:|:-:|
| audit_queue | FEDERATION_TRANSFER | Transfer completed (success or failure) |
*Table 77.* 
**5.3.9.6 PostgreSQL Interactions**
| **Operation** | **Table** | **Trigger** |
|:-:|:-:|:-:|
| SELECT | jobs | Verify job status |
| SELECT | federation_peers | Retrieve peer endpoint and certificate |
| SELECT | data_use_agreements | Verify active DUA exists |
| INSERT | federation_transfers | Record completed transfer |
*Table 78.* 
**5.3.10 Inter-Service Communication**
The microservices within the Saudi Anonymization and Data Masking Network communicate through a hybrid pattern: RabbitMQ message queues for workflow coordination and internal HTTP endpoints for file transfer. This section documents the communication topology and message specifications.
**5.3.10.1 Communication Pattern Summary**
| **Communication Type** | **Mechanism** | **Use Cases** |
|:-:|:-:|:-:|
| Workflow Coordination | RabbitMQ Queues | Classification requests, validation triggers, phase transitions, audit events |
| File Transfer | Internal HTTP (/internal/*) | Orchestrator → Storage (upload), Masking → Storage (masked file), Orchestrator → Storage (approve/reject) |
| Peer Communication | mTLS on port 8443 | Federation Gateway → Peer SADN instances |
*Table 79.* 
**5.3.10.2 Queue Topology**
The system employs five persistent queues, each dedicated to a specific category of messages:
| **Queue Name** | **Publisher(s)** | **Consumer** | **Purpose** |
|:-:|:-:|:-:|:-:|
| storage_queue | Validation Service | Storage Service | Phase transition commands (MOVE_TO_QUARANTINE) |
| validation_queue | Storage Service, Masking Service | Validation Service | Classification and privacy validation requests |
| nlp_queue | Validation Service | NLP Service | Text analysis requests for Free Text columns |
| masking_queue | Validation Service, NLP Service | Masking Service | Transformation requests with classification configuration |
| audit_queue | All services | Audit Service | Event logging for compliance |
*Table 80.* 
Each queue is configured with persistence enabled, ensuring that messages survive broker restarts. Dead letter exchanges are configured for each queue, capturing messages that cannot be processed after a configurable number of retry attempts.
**5.3.10.3 Internal HTTP Endpoints**
| **Service** | **Endpoint** | **Method** | **Called By** | **Purpose** |
|:-:|:-:|:-:|:-:|:-:|
| Storage Service | /internal/files/{job_id} | POST | Orchestrator | Upload file for intake validation |
| Storage Service | /internal/files/{job_id}/masked | POST | Masking Service | Store masked file in staging/ |
| Storage Service | /internal/files/{job_id}/approve | POST | Orchestrator | Trigger transition to safe/ |
| Storage Service | /internal/files/{job_id}/reject | POST | Orchestrator | Trigger transition to quarantine/ |
| Federation Gateway | /internal/federation/share/{job_id} | POST | Orchestrator | Initiate federated transfer |
*Table 81.* 
**5.3.10.4 Message Specifications**
Messages published to each queue follow defined JSON schemas:
**storage_queue:**
json
{
  "job_id": "UUID",
  "action": "MOVE_TO_QUARANTINE",
  "failure_reasons": ["string"]
}
**validation_queue:**
json
{
  "job_id": "UUID",
  "action": "CLASSIFY | VALIDATE_PRIVACY",
  "file_path": "string",
  "classification_config": { }
}
**nlp_queue:**
json
{
  "job_id": "UUID",
  "file_path": "string",
  "text_columns": ["column_name_1", "column_name_2"],
  "classification_config": { }
}
**masking_queue:**
json
{
  "job_id": "UUID",
  "file_path": "string",
  "classification_config": {
    "columns": [
      {
        "name": "string",
        "type": "DIRECT_ID | QUASI_ID | SENSITIVE | FREE_TEXT",
        "transformation": "SUPPRESS | GENERALIZE | PSEUDONYMIZE | DATE_SHIFT | NLP_REDACT | KEEP"
      }
    ]
  }
}
**audit_queue:**
json
{
  "event_id": "UUID",
  "job_id": "UUID | null",
  "event_type": "string",
  "timestamp": "ISO 8601",
  "actor_id": "string",
  "details": { }
}
**5.3.11 Sequence Diagrams**
The following sequence diagrams illustrate the message flow for key processing scenarios. These diagrams complement the static architectural views presented in preceding sections by depicting the dynamic interactions between services during job processing.
**5.3.11.1 Standard Processing Flow (No Free Text)**
The standard processing flow applies to datasets containing no Free Text columns, bypassing the NLP Service. This flow represents the most common processing path for structured tabular datasets.

*Figure 7.* 
### Standard Processing Sequence Diagram
**5.3.11.2 NLP Processing Flow (With Free Text)**
The NLP processing flow applies to datasets containing one or more Free Text columns requiring natural language processing for PII detection.


*Figure 8.* 
### NLP Processing Sequence Diagram
**5.3.11.3 Validation Failure Flow**
When privacy metrics fail minimum thresholds, the pipeline automatically moves files to quarantine without user approval:

*Figure 9.* 

### Validation Failure Sequence Diagram


### 6\. Data Design
### 6.1 Data Description
The SADN platform processes sensitive institutional datasets and transforms them into structured, secure, and verifiably anonymized data artifacts. This section describes how the system's information domain is represented as data structures, how these structures flow through the microservice pipeline, and how they are organized across the database and storage layers.
**6.1.1 Information Domain Overview**
SADN operates on two major data domains:
**6.1.1.1 Dataset Files (Primary Domain)**
Uploaded by institutional users in the following formats: CSV, JSON, Parquet, and Excel (XLSX). These files contain sensitive attributes such as:
* Personal identifiers (e.g., names, national IDs, phone numbers)
* Health information (e.g., diagnoses, medications)
* Demographic attributes (e.g., age, region, gender)

⠀**6.1.1.2 System-Generated Metadata (Secondary Domain)**
During the anonymization pipeline, SADN produces structured metadata including:
* Job metadata and processing state
* Column classification results and NLP annotations
* Masking transformation logs
* Privacy metric validation results
* Cryptographically chained audit logs
* Policy configuration snapshots with classification and technique mappings

⠀**6.1.2 Data Transformation into System Data Structures**
The information domain is systematically transformed into structured data stored across:
**PostgreSQL (Relational Database)**
Represents the authoritative system-of-record for all job metadata, processing results, policies, and audit logs. The database is organized into three logical table groups:
* **Configuration Tables:** policies, classifications, masking_techniques, policy_rules
* **Operational Tables:** users, jobs
* **Result Tables:** masking_results, validation_results, column_classification_results, nlp_annotations, audit_logs

⠀**MinIO (Object Storage)**
MinIO stores all dataset files following a strict five-phase lifecycle:
* **intake/** - Raw uploaded files (pre-validation)
* **staging/** - Files during NLP, masking, and validation
* **quarantine/** - Files failing validation
* **safe/** - Validated, anonymized datasets
* **archive/** - Long-term retention (7 years)

⠀**6.1.3 Organization of System Entities**
The system organizes major entities into three structured layers:
**6.1.3.1 Data Layer (Primary Storage)**
* MinIO bucket structure for physical data
* PostgreSQL tables for metadata and processing results
* Versioned policy definitions with classification mappings

⠀**6.1.3.2 Processing Layer (Derived Data)**
* Column classification results
* NLP-detected entity annotations
* Masking transformation logs
* Privacy validation outcomes
* Audit events with Merkle hash chaining

⠀**6.1.3.3 Governance Layer (Compliance Data)**
* Audit logs (append-only)
* Privacy metric verification
* Policy versioning with rule associations
* Retention/archival metadata

⠀**6.1.4 Databases and Storage Components**
| **Component** | **Purpose** | **Technology** |
|:-:|:-:|:-:|
| PostgreSQL | Metadata, results, audit logs, configurations | Relational DB, JSONB support |
| MinIO | Dataset storage across all lifecycle phases | S3-compatible Object Storage |
| Vault | Credentials, encryption keys | Secret Manager |
| Docker Volumes | Persistence for DB and message queues | Local storage |
**6.1.5 Data Flow**
The SADN platform follows a defined data flow through processing stages: **Login → Upload → Intake → Classify → NLP → Mask → Validate → Approve → Audit**
**6.1.6 Summary**
SADN transforms sensitive institutional datasets into a set of well-structured data entities that are securely stored, cryptographically auditable, rich in metadata, organized across relational and object storage, and traceable through every processing stage.



### 6.2 Data Dictionary
This section provides a complete listing of the major data entities used within the SADN platform, organized by functional category.
**6.2.1 Configuration Tables**
**Entity: policies**
| **Field** | **Type** | **Description** |
|:-:|:-:|:-:|
| policy_id | SERIAL (PK) | Unique identifier for the policy |
| policy_name | VARCHAR(100) | Descriptive name of the policy |
| description | TEXT | Detailed description of policy purpose |
| compliance_standard | VARCHAR(50) | Compliance framework (e.g., PDPL, HIPAA) |
| retention_days | INTEGER | Number of days to retain processed data |
| is_active | BOOLEAN | Indicates if policy is currently active |
| rules | JSONB | Policy-specific configuration rules |
| created_at | TIMESTAMP | Record creation timestamp |
| created_by | VARCHAR(255) | User who created the record |
| updated_at | TIMESTAMP | Last modification timestamp |
| updated_by | VARCHAR(255) | User who last modified the record |
| deleted_at | TIMESTAMP | Soft delete timestamp |
| deleted_by | VARCHAR(255) | User who deleted the record |
**Entity: classifications**
| **Field** | **Type** | **Description** |
|:-:|:-:|:-:|
| classification_id | SERIAL (PK) | Unique identifier for the classification |
| classification_name | VARCHAR(100) | Name of the data classification category |
| category | VARCHAR(50) | Classification category (e.g., PII, PHI) |
| sensitivity_level | INTEGER | Numeric sensitivity level (higher = more sensitive) |
| description | TEXT | Detailed description of the classification |
| regex_patterns | JSONB | Regular expression patterns for detection |
| keywords | TEXT[] | Array of keywords for pattern matching |
| created_at | TIMESTAMP | Record creation timestamp |
| created_by | VARCHAR(255) | User who created the record |
| updated_at | TIMESTAMP | Last modification timestamp |
| updated_by | VARCHAR(255) | User who last modified the record |
| deleted_at | TIMESTAMP | Soft delete timestamp |
| deleted_by | VARCHAR(255) | User who deleted the record |
**Entity: masking_techniques**
| **Field** | **Type** | **Description** |
|:-:|:-:|:-:|
| technique_id | SERIAL (PK) | Unique identifier for the technique |
| technique_name | VARCHAR(100) | Name of the masking technique |
| technique_type | VARCHAR(50) | Type category (e.g., hash, redact, generalize) |
| description | TEXT | Detailed description of the technique |
| parameters | JSONB | Configuration parameters for the technique |
| is_reversible | BOOLEAN | Whether the transformation can be reversed |
| preserves_format | BOOLEAN | Whether the output format matches input |
| created_at | TIMESTAMP | Record creation timestamp |
| created_by | VARCHAR(255) | User who created the record |
| updated_at | TIMESTAMP | Last modification timestamp |
| updated_by | VARCHAR(255) | User who last modified the record |
| deleted_at | TIMESTAMP | Soft delete timestamp |
| deleted_by | VARCHAR(255) | User who deleted the record |
**Entity: policy_rules**
| **Field** | **Type** | **Description** |
|:-:|:-:|:-:|
| rule_id | SERIAL (PK) | Unique identifier for the rule |
| policy_id | INTEGER (FK) | References policies.policy_id |
| classification_id | INTEGER (FK) | References classifications.classification_id |
| technique_id | INTEGER (FK) | References masking_techniques.technique_id |
| priority | INTEGER | Execution priority order |
| is_mandatory | BOOLEAN | Whether rule application is mandatory |
| created_at | TIMESTAMP | Record creation timestamp |
| created_by | VARCHAR(255) | User who created the record |
| updated_at | TIMESTAMP | Last modification timestamp |
| updated_by | VARCHAR(255) | User who last modified the record |
**6.2.2 Operational Tables**
**Entity: users**
| **Field** | **Type** | **Description** |
|:-:|:-:|:-:|
| user_id | VARCHAR(255) (PK) | Unique identifier for the user |
| username | VARCHAR(100) | User's login username |
| email | VARCHAR(255) | User's email address |
| password_hash | VARCHAR(255) | Hashed password for authentication |
| role | VARCHAR(50) | User role (e.g., admin, analyst, viewer) |
| mfa_secret | VARCHAR(100) | Multi-factor authentication secret |
| is_active | BOOLEAN | Whether user account is active |
| created_at | TIMESTAMP | Account creation timestamp |
| created_by | VARCHAR(255) | User who created the account |
| updated_at | TIMESTAMP | Last modification timestamp |
| updated_by | VARCHAR(255) | User who last modified the record |
| deleted_at | TIMESTAMP | Soft delete timestamp |
**Entity: jobs**
| **Field** | **Type** | **Description** |
|:-:|:-:|:-:|
| job_id | UUID (PK) | Unique identifier for the processing job |
| user_id | VARCHAR(255) (FK) | References users.user_id |
| policy_id | INTEGER (FK) | References policies.policy_id |
| filename | VARCHAR(512) | Original uploaded filename |
| file_url | TEXT | Storage URL for the dataset file |
| file_type | VARCHAR(50) | File format (csv, json, parquet, xlsx) |
| file_size | BIGINT | File size in bytes |
| row_count | INTEGER | Number of records in the dataset |
| status | VARCHAR(50) | Overall job status (e.g., pending, complete) |
| state | VARCHAR(50) | Current pipeline state |
| current_service | VARCHAR(100) | Service currently processing the job |
| approved_by | VARCHAR(255) | User who approved the job |
| approved_at | TIMESTAMP | Approval timestamp |
| error_message | TEXT | Error details if job failed |
| created_at | TIMESTAMP | Job creation timestamp |
| created_by | VARCHAR(255) | User who created the job |
| updated_at | TIMESTAMP | Last modification timestamp |
| updated_by | VARCHAR(255) | User who last modified the record |
| deleted_at | TIMESTAMP | Soft delete timestamp |
| deleted_by | VARCHAR(255) | User who deleted the record |
**6.2.3 Result Tables**
**Entity: column_classification_results**
| **Field** | **Type** | **Description** |
|:-:|:-:|:-:|
| result_id | SERIAL (PK) | Unique identifier for the result |
| job_id | UUID (FK) | References jobs.job_id |
| classification_id | INTEGER (FK) | References classifications.classification_id |
| column_index | INTEGER | Zero-based column index in dataset |
| column_name | VARCHAR(255) | Name of the classified column |
| confidence_score | DECIMAL(5,4) | Classification confidence (0.0000-1.0000) |
| detection_signals | JSONB | Signals that triggered classification |
| is_pii | BOOLEAN | Whether column contains PII |
| created_at | TIMESTAMP | Result creation timestamp |
| created_by | VARCHAR(255) | Service that created the result |
| updated_at | TIMESTAMP | Last modification timestamp |
**Entity: nlp_annotations**
| **Field** | **Type** | **Description** |
|:-:|:-:|:-:|
| annotation_id | SERIAL (PK) | Unique identifier for the annotation |
| job_id | UUID (FK) | References jobs.job_id |
| column_name | VARCHAR(255) | Column containing the entity |
| row_index | INTEGER | Row number where entity was found |
| entity_type | VARCHAR(50) | Type of detected entity (e.g., NAME, SSN) |
| original_text | TEXT | Original text that was detected |
| start_position | INTEGER | Character start position in cell |
| end_position | INTEGER | Character end position in cell |
| confidence_score | DECIMAL(5,4) | Detection confidence (0.0000-1.0000) |
| created_at | TIMESTAMP | Annotation creation timestamp |
| created_by | VARCHAR(255) | Service that created the annotation |
**Entity: masking_results**
| **Field** | **Type** | **Description** |
|:-:|:-:|:-:|
| masking_id | SERIAL (PK) | Unique identifier for masking result |
| job_id | UUID (FK, UNIQUE) | References jobs.job_id (one-to-one) |
| original_hash | VARCHAR(64) | SHA-256 hash of original dataset |
| masked_hash | VARCHAR(64) | SHA-256 hash of masked dataset |
| masked_file_url | TEXT | Storage URL for masked file |
| transformations_applied | JSONB | List of masking transformations used |
| columns_suppressed | INTEGER | Count of fully suppressed columns |
| records_processed | INTEGER | Number of records processed |
| processing_time_ms | INTEGER | Processing duration in milliseconds |
| created_at | TIMESTAMP | Result creation timestamp |
| created_by | VARCHAR(255) | Service that created the result |
| updated_at | TIMESTAMP | Last modification timestamp |
| updated_by | VARCHAR(255) | User who last modified the record |
**Entity: validation_results**
| **Field** | **Type** | **Description** |
|:-:|:-:|:-:|
| validation_id | SERIAL (PK) | Unique identifier for validation result |
| job_id | UUID (FK, UNIQUE) | References jobs.job_id (one-to-one) |
| k_anonymity | INTEGER | Calculated k-anonymity value |
| l_diversity | DECIMAL(5,2) | Calculated l-diversity value |
| t_closeness | DECIMAL(5,4) | Calculated t-closeness value |
| validation_passed | BOOLEAN | Whether privacy thresholds were met |
| risk_score | INTEGER | Overall risk assessment score (0-100) |
| quasi_identifiers | TEXT[] | Fields considered quasi-identifying |
| sensitive_attributes | TEXT[] | Fields considered sensitive |
| failure_reasons | JSONB | Details of validation failures |
| created_at | TIMESTAMP | Result creation timestamp |
| created_by | VARCHAR(255) | Service that created the result |
| updated_at | TIMESTAMP | Last modification timestamp |
| updated_by | VARCHAR(255) | User who last modified the record |
| validated_by | VARCHAR(255) | User who validated/approved result |
**Entity: audit_logs**
| **Field** | **Type** | **Description** |
|:-:|:-:|:-:|
| id | BIGSERIAL (PK) | Sequential primary key for ordering |
| event_id | UUID | Unique identifier for the audit event |
| job_id | UUID (FK) | References jobs.job_id |
| event_type | VARCHAR(100) | Type of event (e.g., JOB_CREATED, NLP_COMPLETED) |
| service_name | VARCHAR(100) | Service that produced the event |
| actor_id | VARCHAR(255) | User or service that triggered the event |
| payload | JSONB | Event-specific metadata |
| merkle_hash | VARCHAR(64) | Hash linking to previous event (tamper evidence) |
| previous_hash | VARCHAR(64) | Hash of the preceding audit event |
| timestamp | TIMESTAMP | Event creation timestamp |
| ip_address | INET | IP address of the actor |
**6.2.4 Standard Audit Fields**
All tables include standard audit fields for record lifecycle tracking:
| **Field** | **Type** | **Description** |
|:-:|:-:|:-:|
| created_at | TIMESTAMP | Record creation timestamp |
| created_by | VARCHAR(255) | User or service that created the record |
| updated_at | TIMESTAMP | Last modification timestamp |
| updated_by | VARCHAR(255) | User or service that last modified the record |
| deleted_at | TIMESTAMP | Soft delete timestamp (where applicable) |
| deleted_by | VARCHAR(255) | User who initiated soft delete |
### 6.3 Database Description
The SADN platform uses a centralized relational database to maintain all metadata, processing results, audit trails, and policy configurations required for the anonymization pipeline.
**6.3.1 Database Architecture Overview**
SADN employs a PostgreSQL database to persist structured information generated across the anonymization workflow. The database is fully ACID-compliant, supports JSON-based semi-structured data, and ensures strong consistency guarantees essential for auditability and regulatory compliance.
The database performs five major roles:
* **Configuration Management** – Stores policies, classifications, masking techniques, and rules
* **User Management** – Manages user accounts, roles, and authentication data
* **Job Tracking** – Tracks each dataset's lifecycle, state transitions, and processing timestamps
* **Pipeline Output Storage** – Records classification, NLP, masking, and validation results
* **Audit Logging** – Maintains immutable, Merkle-chained history of all operations

⠀**6.3.2 Entity Overview**
The core database consists of eleven primary tables organized into three logical groups:
**Configuration Tables (4 tables)**
* **policies** – Defines compliance policies and retention rules
* **classifications** – Categorizes data sensitivity types with detection patterns
* **masking_techniques** – Defines available anonymization methods
* **policy_rules** – Maps classifications to techniques within policies

⠀**Operational Tables (2 tables)**
* **users** – Manages user accounts and authentication
* **jobs** – Central hub tracking dataset processing lifecycle

⠀**Result Tables (5 tables)**
* **column_classification_results** – Stores column-level classification outcomes
* **nlp_annotations** – Records cell-level NLP entity detections
* **masking_results** – Documents masking transformations and file hashes
* **validation_results** – Stores privacy metric evaluations
* **audit_logs** – Immutable, ordered audit events with hash chaining

⠀**6.3.3 Data Model and Table Relationships**
The database schema follows a hub-and-spoke structure centered around the jobs table, with configuration tables providing reference data.
**Configuration Relationships:**
* policies → policy_rules (1:N)
* classifications → policy_rules (1:N)
* classifications → column_classification_results (1:N)
* masking_techniques → policy_rules (1:N)

⠀**Operational Relationships:**
* users → jobs (1:N)
* policies → jobs (1:N)

⠀**Result Relationships:**
* jobs → column_classification_results (1:N)
* jobs → nlp_annotations (1:N)
* jobs → masking_results (1:1)
* jobs → validation_results (1:1)
* jobs → audit_logs (1:N)

⠀
**6.3.4 Rationale for Using PostgreSQL**
**Strong Consistency & ACID Guarantees** – Critical for ensuring correct state transitions, reliable audit logs, and consistent policy enforcement.
**Native JSONB Support** – Used extensively for detection signals, masking transformations, validation metrics, and policy definitions.
**Referential Integrity** – Foreign key relationships enforce strict guarantees that every result maps back to an existing job.
**Security Features** – Supports row-level security, SSL/TLS connections, and fine-grained access control.
**Write-Ahead Logging (WAL)** – Provides durability, crash recovery, and compatibility with backup/restore strategies.
**6.3.5 Storage and Indexing Strategy**
**Primary Indexes:**
* jobs(job_id) – primary job lookup
* users(user_id) – user authentication
* policies(policy_id), classifications(classification_id), masking_techniques(technique_id)
* column_classification_results(job_id), nlp_annotations(job_id)
* masking_results(job_id), validation_results(job_id)
* audit_logs(job_id), audit_logs(timestamp) – supports chronological queries

⠀**Secondary Indexes:**
* jobs(status), jobs(state) – efficient job monitoring
* jobs(created_at) – time-based filtering
* users(email), users(username) – authentication lookups
* policies(is_active), classifications(category) – configuration filtering

⠀**6.3.6 Integration with Other System Components**
* **Auth Service:** manages user records and authentication
* **Orchestrator:** creates jobs, updates states, and triggers pipeline progression
* **Classification Service:** inserts column classification results
* **NLP Service:** inserts entity annotation results
* **Masking Service:** inserts masking metadata and dataset hashes
* **Validation Service:** inserts privacy metric evaluations
* **Audit Service:** writes cryptographically chained audit events into append-only tables
* **Storage Service:** updates storage phases and paths in jobs table
* **Dashboard:** reads historical records for monitoring and compliance reporting

⠀**6.3.7 Summary**
The database architecture provides a structured, reliable, and secure foundation for SADN's anonymization pipeline. It maintains all operational state, processing output, compliance artifacts, and configuration rules. Through its relational consistency, JSON flexibility, and strong security features, it ensures that every dataset, transformation, and audit event remains verifiable, traceable, and compliant with institutional and regulatory requirements.

### 6 Component Design

⠀
In this section, we take a closer look at what each component does in a more systematic way. If you gave a functional description in previous sections, provide a summary of your algorithm for each function listed previously in procedural description language (PDL) or pseudocode. If you gave an OO description, summarize each object member function for all the objects in PDL or pseudocode. 

Describe any local data when necessary.

### 7.1 Orchestrator Component
**7.1.1 Overview**
The Orchestrator is the sole external entry point for the Saudi Anonymization and Data Masking Network. It exposes RESTful APIs through which external actors submit datasets, monitor job progress, retrieve results, and make approval decisions. Unlike other SADN microservices that perform data transformation or analysis, the Orchestrator functions primarily as a coordinator-receiving requests, delegating work to specialized services, and tracking job state throughout the pipeline.
The Orchestrator is implemented in Python using the FastAPI framework, maintaining consistency with other Python-based SADN services. It does not process dataset contents directly; instead, it transfers uploaded files to the Storage Service and monitors state changes recorded by downstream services. This architectural decision centralizes authentication, authorization, and request validation at a single controlled point.
The internal modules, external endpoints, and communication patterns are documented in Section 5.3.3. This section specifies the processing logic, data access patterns, error handling strategies, and configuration parameters required for implementation.
**7.1.2 Job Lifecycle Management**
The Orchestrator manages job state throughout the anonymization pipeline. Jobs progress through nine statuses as documented in Section 5.2.5. The Orchestrator is responsible for initial job creation and for processing user decisions that trigger final state transitions.
**Job Creation Logic**
FUNCTION CreateJob(uploadedFile, userId, policyId)
    
    // Validate request
    IF uploadedFile.size > MAX_FILE_SIZE THEN
        RETURN Error(413, "File exceeds maximum size")
    END IF
    
    IF NOT IsValidFormat(uploadedFile.extension) THEN
        RETURN Error(415, "Unsupported file format")
    END IF
    
    // Create job record
    jobId ← GenerateUUID()
    
    INSERT INTO jobs (
        job_id, user_id, filename, file_size, file_format,
        status, storage_phase, policy_id, created_at
    ) VALUES (
        jobId, userId, uploadedFile.name, uploadedFile.size,
        uploadedFile.format, "PENDING", NULL, policyId, NOW()
    )
    
    // Transfer file to Storage Service
    response ← HTTP_POST(
        StorageService + "/internal/files/" + jobId,
        uploadedFile.content
    )
    
    IF response.status ≠ 200 THEN
        UpdateJobStatus(jobId, "FAILED", response.error)
        RETURN Error(500, "File transfer failed")
    END IF
    
    // Publish audit event
    PublishToAuditQueue({
        event_type: "JOB_CREATED",
        job_id: jobId,
        actor_id: userId
    })
    
    RETURN Success(jobId)

END FUNCTION
**Status Query Logic**
FUNCTION GetJobStatus(jobId, requestingUserId)
    
    job ← SELECT * FROM jobs WHERE job_id = jobId
    
    IF job IS NULL THEN
        RETURN Error(404, "Job not found")
    END IF
    
    // Verify access authorization
    IF NOT CanAccessJob(requestingUserId, job) THEN
        RETURN Error(403, "Access denied")
    END IF
    
    RETURN {
        job_id: job.job_id,
        status: job.status,
        storage_phase: job.storage_phase,
        created_at: job.created_at,
        updated_at: job.updated_at,
        error_message: job.error_message
    }

END FUNCTION
**7.1.3 User Approval Workflow**
When privacy validation passes, jobs enter the AWAITING_APPROVAL status. The Data Owner must explicitly approve or reject the anonymization result before the dataset transitions to its final phase.
**Approval Processing**
FUNCTION ApproveJob(jobId, requestingUserId)
    
    job ← SELECT * FROM jobs WHERE job_id = jobId
    
    // Validate job state
    IF job.status ≠ "AWAITING_APPROVAL" THEN
        RETURN Error(409, "Job not awaiting approval")
    END IF
    
    // Verify user is job owner
    IF job.user_id ≠ requestingUserId THEN
        RETURN Error(403, "Only job owner can approve")
    END IF
    
    // Trigger phase transition via Storage Service
    response ← HTTP_POST(
        StorageService + "/internal/files/" + jobId + "/approve"
    )
    
    IF response.status ≠ 200 THEN
        RETURN Error(500, "Phase transition failed")
    END IF
    
    // Publish audit event
    PublishToAuditQueue({
        event_type: "JOB_APPROVED",
        job_id: jobId,
        actor_id: requestingUserId
    })
    
    RETURN Success("Job approved, dataset moved to safe storage")

END FUNCTION
**Rejection Processing**
FUNCTION RejectJob(jobId, requestingUserId, rejectionReason)
    
    job ← SELECT * FROM jobs WHERE job_id = jobId
    
    IF job.status ≠ "AWAITING_APPROVAL" THEN
        RETURN Error(409, "Job not awaiting approval")
    END IF
    
    IF job.user_id ≠ requestingUserId THEN
        RETURN Error(403, "Only job owner can reject")
    END IF
    
    // Trigger quarantine transition
    response ← HTTP_POST(
        StorageService + "/internal/files/" + jobId + "/reject"
    )
    
    // Update job with rejection reason
    UPDATE jobs SET error_message = rejectionReason WHERE job_id = jobId
    
    // Publish audit event
    PublishToAuditQueue({
        event_type: "JOB_REJECTED",
        job_id: jobId,
        actor_id: requestingUserId,
        details: { reason: rejectionReason }
    })
    
    RETURN Success("Job rejected, dataset moved to quarantine")

END FUNCTION
**7.1.4 Result Delivery**
The Orchestrator serves download requests for completed jobs by streaming files from MinIO safe storage.
FUNCTION DownloadResult(jobId, requestingUserId)
    
    job ← SELECT * FROM jobs WHERE job_id = jobId
    
    IF job.status ≠ "COMPLETED" THEN
        RETURN Error(409, "Job not completed")
    END IF
    
    IF NOT CanDownload(requestingUserId, job) THEN
        RETURN Error(403, "Download not authorized")
    END IF
    
    // Stream file from MinIO
    filePath ← "safe/" + jobId + "/masked.csv"
    fileStream ← MinIO.GetObjectStream(filePath)
    
    RETURN StreamResponse(fileStream, job.filename)

END FUNCTION
**7.1.5 Federation Initiation**
The Orchestrator forwards federation requests to the Federation Gateway for processing.
FUNCTION InitiateFederation(jobId, peerId, requestingUserId)
    
    job ← SELECT * FROM jobs WHERE job_id = jobId
    
    IF job.status ≠ "COMPLETED" THEN
        RETURN Error(409, "Only completed jobs can be shared")
    END IF
    
    IF NOT CanInitiateFederation(requestingUserId) THEN
        RETURN Error(403, "Federation not authorized for user")
    END IF
    
    // Delegate to Federation Gateway
    response ← HTTP_POST(
        FederationGateway + "/internal/federation/share/" + jobId,
        { peer_id: peerId, requesting_user_id: requestingUserId }
    )
    
    RETURN response

END FUNCTION
**7.1.6 Interface Specification**
The Orchestrator exposes seven external endpoints as documented in Section 5.3.3.2. Minimal request/response examples are provided below.
**Job Submission**
**POST /api/v1/jobs**
Request: Multipart form with file upload and policy_id parameter.
Response (Success):
{ "job_id": "uuid", "status": "PENDING" }
**Job Status**
**GET /api/v1/jobs/{job_id}**
Response:
{ "job_id": "uuid", "status": "MASKING", "storage_phase": "staging" }
**Approval**
**POST /api/v1/jobs/{job_id}/approve**
Response:
{ "message": "Job approved", "storage_phase": "safe" }
**Download**
**GET /api/v1/jobs/{job_id}/download**
Response: Binary file stream with appropriate content headers.
### 7.1.7 Data Access
**PostgreSQL Operations**
| **Operation** | **Table** | **Purpose** |
|:-:|:-:|:-:|
| INSERT | jobs | Create new job record |
| SELECT | jobs | Query job status and metadata |
| UPDATE | jobs | Record error messages on rejection |
*Table 90.* 
The Orchestrator does not modify job status directly during pipeline processing. Status updates from PENDING through AWAITING_APPROVAL are performed by downstream services (Storage, Validation). The Orchestrator only triggers status changes through its calls to the Storage Service (approve/reject).
**MinIO Operations**
| **Phase** | **Access** | **Purpose** |
|:-:|:-:|:-:|
| safe/ | READ | Stream masked file for download requests |
*Table 91.* 
The Orchestrator does not write to MinIO directly. All file storage operations are delegated to the Storage Service.
**7.1.8 Error Handling**
**HTTP Error Responses**
| **Status Code** | **Condition** | **Response** |
|:-:|:-:|:-:|
| 400 | Invalid request parameters | Validation error details |
| 403 | Authorization failure | Access denied message |
| 404 | Job not found | Job ID not in database |
| 409 | Invalid state transition | Current status prevents action |
| 413 | File too large | Size limit exceeded |
| 415 | Unsupported format | Invalid file type |
| 500 | Internal error | Generic error with correlation ID |
*Table 92.* 
**Internal Call Failures**
When internal HTTP calls to Storage Service or Federation Gateway fail, the Orchestrator:
1 Logs the failure with correlation ID
2 Returns appropriate error to client
3 Does not retry (client can retry the request)

⠀For job creation failures after the database record is created, the job status is updated to FAILED with the error details.
**7.1.9 Configuration**
**Environment Variables**
| **Variable** | **Required** | **Description** |
|:-:|:-:|:-:|
| POSTGRES_HOST | Yes | PostgreSQL server hostname |
| POSTGRES_DATABASE | Yes | Database name |
| RABBITMQ_HOST | Yes | RabbitMQ server hostname |
| MINIO_ENDPOINT | Yes | MinIO server endpoint |
| STORAGE_SERVICE_URL | Yes | Storage Service base URL |
| FEDERATION_GATEWAY_URL | Yes | Federation Gateway base URL |
| MAX_FILE_SIZE_MB | No | Maximum upload size (default: 500) |
| JWT_SECRET | Yes | Token validation secret |
*Table 93.* 
**Tunable Parameters**
| **Parameter** | **Default** | **Description** |
|:-:|:-:|:-:|
| REQUEST_TIMEOUT_SECONDS | 30 | Timeout for internal HTTP calls |
| MAX_UPLOAD_SIZE_MB | 500 | Maximum file upload size |
| TOKEN_EXPIRY_HOURS | 24 | JWT token validity period |
*Table 94.* 
**7.1.10 Security Considerations**
**Authentication**
The Orchestrator validates JWT tokens on all requests. Tokens are verified against the configured secret and checked for expiration. Invalid or expired tokens result in 401 responses.
**Authorization**
Role-based access control is enforced per endpoint as specified in Section 5.3.3.2. The Authorization Handler module verifies that the requesting user's role permits the requested operation. Data Owners can access only their own jobs; DPOs and Administrators have broader access for oversight purposes.
**Input Validation**
All request parameters are validated before processing:
* File uploads are checked for size limits and format
* UUIDs are validated for correct format
* Policy IDs are verified against the policies table

⠀**Audit Trail**
All significant actions (job creation, approval, rejection, download, federation initiation) are published to the audit queue, creating a complete record of user interactions with the system.
 
### 7.2 NLP Component
**7.2.1 Purpose and Scope**
The NLP Component is responsible for automatically identifying, classifying, and annotating Personally Identifiable Information (PII) and Protected Health Information (PHI) within datasets processed by the SADN anonymization pipeline. Its primary purpose is to ensure that all sensitive attributes-whether directly identifying, quasi-identifying, or contextually sensitive-are detected prior to anonymization, enabling the Masking Service and Validation Component to apply the correct transformations and enforce privacy guarantees such as k-anonymity, l-diversity, and t-closeness.
The scope of the NLP Component includes processing both structured and semi-structured data fields, analyzing column names, inspecting sampled cell values, normalizing text inputs, and applying hybrid detection techniques that combine heuristics, pattern matching, dictionary-based recognition, and statistical machine learning. The component outputs a structured “PII Map” that describes the semantic category of each attribute and contributes directly to the privacy, correctness, and governance of the entire system.
This component operates under strict privacy and security constraints. It does not store or log raw values, never persists sensitive data, and communicates only detection metadata to downstream components. Its operation is fully deterministic, traceable through the Audit Trail, and aligned with PDPL-compliant organizational governance requirements.
**7.2.2 Responsibilities**
The responsibilities of the NLP Component are organized into four categories: detection, classification, integration, and governance. These responsibilities ensure that the NLP subsystem not only identifies sensitive fields accurately but also provides structured, explainable outputs required for downstream anonymization, validation, and compliance.
**7.2.2.1 Detection Responsibilities**
The NLP Component is responsible for detecting sensitive elements at both the **column level** and the **cell level**, including:
* **Direct Identifiers**:  Email, phone number, national ID, medical record number (MRN), passport number, IBAN, IP addresses, and other uniquely identifying values.
* **Quasi-Identifiers**:  Birth date, ZIP code, gender, ethnicity, age, district, and combinations that may re-identify individuals when aggregated.
* **Sensitive Attributes**:  Medical conditions, diagnosis codes, clinical procedures, financial values, geospatial positions, and any domain-specific health or personal attributes.
* **Embedded Free-Text PII**:  Names, hospital names, medical terms, or contact info appearing within unstructured fields.
* **Multilingual and Mixed-Script Detection**:  Detecting PII in English, Arabic, and hybrid text (e.g., Arabic names in Latin transliteration, English values inside Arabic text).

⠀These detection tasks rely on a hybrid approach including preprocessing, regex pattern matching, dictionary lookup, and machine learning classification.
**7.2.2.2 Classification Responsibilities**
After detecting potential PII, the NLP Component classifies each field into one of the following semantic categories:
* **Identifier** – A field that directly identifies an individual.
* **Quasi-Identifier** – A field that may re-identify individuals when combined with other data.
* **Sensitive Attribute** – A field containing personal, medical, or financial data requiring strong protection.
* **Non-Sensitive Attribute** – A safe field with no relation to personal identity or sensitive status.

⠀Classification responsibilities include:
* Aggregating evidence from heuristics, pattern hits, dictionary matches, and ML predictions.
* Assigning a **confidence score** for each field classification.
* Producing reasoning metadata (“evidence list”) to support transparency and auditability.
* Identifying ambiguous cases that require DPO review or policy overrides.

⠀Classification results are used by the Masking Service to determine the required anonymization action (masking, generalization, suppression, or encryption).
**7.2.2.3 Integration Responsibilities**
The NLP Component provides structured outputs and integrates seamlessly with downstream components through well-defined interfaces.
Integration responsibilities include:
* Producing the **PII Map**, a JSON-structured representation summarizing all detected sensitive fields and their associated classifications and confidence values.
* Providing Masking Service with attribute-level semantic categories to determine required anonymization transformations.
* Providing Validation Component with identifier and quasi-identifier lists used to compute privacy metrics.
* Emitting standardized events to the Orchestrator and Message Queue to advance job execution stages.
* Ensuring internal data structures are compatible with system-wide configuration and policy frameworks.

⠀Integration ensures consistent anonymization behavior and enforces correctness in the privacy preservation pipeline.
**7.2.2.4 Governance and Audit Responsibilities**
The NLP Component plays a critical role in governance, auditability, and compliance.
Its responsibilities in this domain include:
* Generating standardized audit events for major operations (e.g., NLP.START, NLP.PII.DETECTED, NLP.PII_MAP_READY, NLP.ERROR).
* Ensuring explainability by providing evidence supporting each classification decision, without exposing raw data.
* Supporting organizational governance by allowing DPO overrides and policy-driven adjustments to detection behavior.
* Operating in strict accordance with privacy regulations such as PDPL, ensuring that raw data is never stored in logs, persisted in memory, or exposed outside the subsystem.
* Enabling traceability across the pipeline by contributing to the immutable Audit Trail and allowing reconstruction of the full detection process for any job.

⠀These governance functions ensure that the NLP Component not only detects sensitive data but does so in a secure, compliant, and transparent manner suitable for regulated enterprise environments.
**7.2.3 Position in System Architecture**
The NLP Component occupies a central role in the SADN system architecture, positioned as the first analytical stage following dataset ingestion and schema construction. It serves as the primary entity responsible for detecting and labeling sensitive fields before any anonymization transformations are applied.
Architecturally, the NLP Component forms part of the **Processing Layer** and is integrated into the pipeline flow between the Intake/Orchestrator subsystem and downstream services such as the Masking Engine, Validation Component, and Audit Service. It operates in a stateless, request-driven mode, processing sampled input data and producing structured metadata (PII Map) without persisting raw values.
Its placement ensures that all subsequent anonymization, validation, and compliance processes are informed by deterministic and traceable PII classification outcomes derived from this component.
**7.2.3.1 Role in the Anonymization Pipeline**
The NLP Component plays a foundational role within the anonymization pipeline. Its primary functions include:
* **Initial PII/PHI Detection:**  Acts as the first stage that inspects column names and sampled values to detect identifiers, quasi-identifiers, and sensitive attributes.
* **Semantic Attribute Classification:**  Produces early semantic labels that influence transformation selection in the Masking Service.
* **Pipeline Readiness Provision:**  Ensures that downstream components have accurate metadata to compute privacy models and apply policy-driven transformations.
* **Context Provider:**  Supplies identifier and quasi-identifier definitions used by the Validation Component to evaluate k-anonymity, l-diversity, and t-closeness.
* **Governance Trigger:**  Emits key NLP events that allow the Audit Trail and DPO interfaces to understand classification rationale.

⠀Overall, the NLP Component establishes the semantic foundation required for safe, compliant, and policy-aligned anonymization workflows.
**7.2.3.2 Interactions with Other Components**
The NLP Component interacts with several major subsystems through structured interfaces and event-driven messages:
* **With Intake/Orchestrator:**  Receives job metadata, column schema, and sampled rows.  Returns NLP readiness signals that advance the job to subsequent pipeline steps.
* **With Masking Service:**  Provides a complete PII Map that guides masking strategies (masking, generalization, suppression, FPE).
* **With Validation Component:**  Supplies classification of identifiers and quasi-identifiers used to compute privacy guarantees.
* **With Audit Service:**  Emits structured NLP events and metadata necessary for compliance, reconstruction, and traceability.

⠀The NLP Component therefore forms an interdependent part of the SADN microservices model: it does not execute transformations itself, but it directly influences the decisions, thresholds, and processing paths of all components that follow.
**7.2.4 External Interfaces and Dependencies**
This section specifies all external interfaces between the NLP Component and other services. The interfaces follow SADN’s internal communication standards, using REST or gRPC for synchronous operations and asynchronous event publication for audit and pipeline state signaling.
Dependencies include access to the Pattern Registry, configurable domain dictionaries, and the ML model repository for statistical classification.
**7.2.4.1 Upstream Interface: Intake / Orchestrator  NLP**
**Direction:** Incoming to NLP  **Type:** REST/gRPC  **Payload:**
* job_id
* Dataset schema (column names, inferred types, nullable flags)
* Sampled rows (bounded by configurable sampling size)
* Organization-level policy overrides (optional)

⠀**Function:**  The Intake/Orchestrator subsystem triggers the NLP Component once preliminary parsing is complete. This interface initiates the NLP analysis and provides all necessary context for preprocessing, pattern detection, and classification.
**Error Conditions:**
* Malformed schema
* Missing columns or metadata
* Unreadable sample rows

⠀These errors propagate back to the Orchestrator for DLQ handling.
**7.2.4.2 Downstream Interface: NLP → Masking Service**
**Direction:** Outgoing from NLP  **Type:** REST/gRPC  **Payload:**
* PII Map (entity types, categories, confidence scores)
* Column-level evidence summary
* Policy override flags (if applicable)

⠀**Function:**  The Masking Service uses this metadata to select appropriate anonymization strategies per field. The NLP Component directly influences whether fields are masked, generalized, suppressed, or encrypted.
**Failure Handling:**  Masking Service will reject inconsistent or incomplete PII Maps, causing the job to enter quarantine.
**7.2.4.3 Downstream Interface: NLP → Validation Component**
**Direction:** Outgoing from NLP  **Type:** REST/gRPC or shared job-state structure  **Payload:**
* Identifiers
* Quasi-identifiers
* Sensitive attribute flags
* Risk-profile descriptors

⠀**Function:**  The Validation Component uses this data to compute privacy guarantees such as k-anonymity, l-diversity, and t-closeness.  Accurate NLP output is therefore essential to produce correct privacy metrics and ensure that the anonymization is mathematically valid.
**Dependencies:**  Relies on compatibility with Validation thresholds and organizational policies.
**7.2.4.4 Cross-Cutting Interface: NLP  Audit Component**
**Direction:** Outgoing (asynchronous)  **Type:** Event stream (message queue) or audit REST sink  **Event Types:**
* NLP.START(job_id)
* NLP.PII_MAP_READY(job_id)
* NLP.PII.DETECTED(job_id)
* NLP.ERROR(job_id, error_code)
* Optional classification explanation events

⠀**Function:**  These events ensure pipeline transparency, allow auditors to reconstruct NLP behavior during post-processing evaluations, and support regulatory compliance requirements.
**Security Note:**  Only metadata is emitted-no raw values, no raw text, and no direct identifiers.
**7.2.5 Internal Structure of NLP Component**
The internal structure of the NLP Component is organized into four primary submodules:  (1) the NLP Preprocessing Engine,  (2) the NLP Pattern Engine,  (3) the Statistical Entity Classifier, and  (4) the PII Aggregation and PII Map Builder.
Each submodule contributes a distinct function within the hybrid detection pipeline, enabling robust, multilingual, and explainable identification of sensitive attributes. The design follows a modular, extensible architecture that allows enhancements-such as adding new patterns, expanding dictionaries, or swapping model versions-without impacting the broader anonymization pipeline.
**7.2.5.1 NLP Preprocessing Engine**
The NLP Preprocessing Engine is the foundational unit responsible for transforming raw input text into normalized, structured representations suitable for downstream detection stages. It ensures consistent handling of multilingual data, removes noise, and prepares tokens required for pattern matching, dictionary lookup, and machine learning inference.
**7.2.5.1.1 Objectives of the Preprocessing Engine**
The primary objectives of the Preprocessing Engine are:
**1** **Normalize textual input** to a consistent encoding (UTF-8), standard Unicode form, and unified structural representation.
**2** **Prepare tokens** that can be used by detection engines with minimal ambiguity or formatting variations.
**3** **Enable robust multilingual support**, particularly for English, Arabic, and mixed-script content.
**4** **Reduce noise and variability** (spacing, punctuation, formatting) that may reduce detection accuracy.
**5** **Provide a clean, predictable text pipeline** that guarantees deterministic processing for the NLP Pattern Engine and ML classifier.
**6** **Preserve privacy** by ensuring preprocessing remains stateless and does not persist raw values.

⠀These objectives align preprocessing with the system’s privacy and compliance requirements, ensuring that no sensitive values are exposed outside memory-bound operations.
**7.2.5.1.2 Main Preprocessing Functions**
The Preprocessing Engine performs the following main functions:
**Whitespace and Formatting Cleanup:**  Removing leading/trailing spaces, collapsing multiple spaces, and normalizing line breaks.
**Unicode Normalization:**  Enforcing NFC/NFKC for consistent pattern matching and ML tokenization.
**Case Folding (Language-Aware):**  Lowercasing English text; safely normalizing Arabic text without altering semantic content.
**Punctuation and Symbol Normalization:**  Converting variant symbols into standard forms, removing noise characters.
**Date and Number Standardization:**  Converting common date formats into a unified format (e.g., YYYY-MM-DD); regex-based handling of numeric formats.
**Structural Normalization for Known Identifiers:**  E.g., converting phone numbers to canonical E.164, emails to lowercase, and normalizing ID spacing.
**Language-Aware Tokenization:**  English tokenization using whitespace/punctuation;  Arabic tokenization using rule-based segmentation and normalization of ligatures.
**Mixed-Script Harmonization:**  Handling text containing both Arabic and Latin characters (common in names and emails).
This combined set of functions ensures that downstream detection modules operate on predictable, clean representations.
**7.2.5.1.3 Internal Submodules (Normalization, Tokenization, Language Handling)**
The Preprocessing Engine is divided into three internal submodules:
 **Normalization Submodule**
Responsible for:
* Unicode normalization
* Case folding
* Standardizing punctuation
* Removing invisible and control characters
* Normalizing phone number symbols (+, -, spaces)

⠀This submodule applies deterministic rules to guarantee identical behavior across processing nodes.
 **Tokenization Submodule**
Implements language-sensitive segmentation:
* Splits text into meaningful tokens
* Handles Arabic clitics, diacritics, and ligatures
* Supports multi-token identifiers (e.g., “+966-555-000000”)
* Tokenizes free-text without altering semantic meaning

⠀ **Language Handling Submodule**
Provides:
* Automatic detection of the primary language of each column
* Special normalization rules (Arabic letter unification, English lowercasing)
* Mixed-script reconciliation to ensure tokens are compatible with pattern rules

⠀Together, these submodules create a robust preprocessing layer that elevates detection accuracy while remaining compliant with system privacy constraints.
**7.2.5.1.4 Inputs and Outputs**
**Inputs**
Raw text sampled from dataset columns.
Column metadata (data types, nullability).
Language detection signals.
Policy overrides affecting default normalization behavior.
**Outputs**
Memory-only TokenizedCell structures containing:
{
  column,
  row_index,
  raw_value (not persisted),
  tokens,
  normalized_value,
  detected_language
}
These outputs provide the input to the Pattern Engine, Dictionary Engine, and ML classifier.
**7.2.5.2 NLP Pattern Engine**
The NLP Pattern Engine is a high-performance module responsible for identifying explicit PII through surface pattern detection. It uses precompiled, versioned regular expressions tuned for multilingual data formats.
**7.2.5.2.1 Objectives of the Pattern Engine**
The primary objectives include:
Detecting structured identifiers with high confidence (emails, phones, national IDs).
Providing deterministic, rule-based evidence for PII classification.
Ensuring fast, low-latency detection using precompiled regex libraries.
Supporting customizable pattern sets aligned with organization and regulatory requirements.
Offering DoS-protected regex execution to avoid performance degradation.
The module acts as the first and fastest detector in the hybrid pipeline.
**7.2.5.2.2 Pattern Categories and Coverage**
Patterns are grouped into versioned categories:
* **Email Patterns (EMAIL_PATTERN_V5)**  RFC-compliant + simplified variants.
* **Phone Number Patterns (PHONE_E164_V3)**  International and region-specific formats (including KSA standard).
* **National Identifier Patterns**
  * Saudi National ID
  * Iqama
  * Passport formats
* **Financial Identifier Patterns**
  * IBAN (multi-country)
  * Credit card formats (Luhn-validated)
* **Medical Identifier Patterns**
  * MRN formats (organization-specific)
  * Lab record identifiers
* **Network Address Patterns**
  * IPv4
  * IPv6

⠀Each pattern is:
Precompiled on startup
Versioned for backward compatibility
Guarded with timeouts to prevent catastrophic regex backtracking
**7.2.5.2.3 Pattern Execution Pipeline**
The pipeline consists of:
**Token Intake:**  Receives tokens from Preprocessing Engine.
**Pattern Selection:**  Based on heuristics and column type, selects relevant regex groups.
**Execution with Sandbox Timeout:**  Executes regex engine under strict time constraints.
**Entity Hit Generation:**  Produces PatternHit entries:
{
  column,
  pattern_id,
  entity_type,
  confidence (typically 1.0),
  row_index (if cell-level enabled)
}
**Aggregation:**  Consolidates hits across rows and patterns for final scoring.
This pipeline ensures maximum speed and accuracy for structured identifiers.
**7.2.5.2.4 Pattern Management and Versioning**
Pattern Registry maintains:
* Pattern sets organized by entity type
* Version numbers (e.g., EMAIL_PATTERN_V5)
* Migration control for pattern updates
* Organizational overrides (custom hospital patterns)
* Automatic consistency checks upon system boot

⠀Updated patterns never overwrite existing versions, enabling auditors to reconstruct classification behavior historically.
**7.2.5.3 Statistical Entity Classifier (ML Submodule)**
The ML submodule provides probabilistic entity classification for ambiguous or unstructured fields. It complements rule-based detection with contextual inference.
**Key Functions**
* Named Entity Recognition (NER) for names, places, organizations, diagnoses.
* Probability scoring for classification categories (identifier, sensitive, etc.).
* Handling free-text fields where pattern-based detection is insufficient.
* Supporting multilingual embeddings for English and Arabic.

⠀**Model Characteristics**
* Lightweight transformer or spaCy-like model
* Loaded once per worker
* Operates in batch mode for efficiency
* Configurable to disable in low-resource environments

⠀**Outputs**
MLPrediction objects with:
entity_type
probability
model_version
row and column context
These predictions feed into the PII Map Builder.
**7.2.5.4 PII Aggregation and PII Map Builder**
This submodule consolidates all detection evidence (heuristics, patterns, dictionary matches, ML scores) into a final, structured classification for each column.
**Responsibilities**
* Aggregate all detection signals
* Compute weighted confidence scores
* Apply policy rules and DPO overrides
* Produce final semantic categories:
  * identifier
  * quasi_identifier
  * sensitive
  * non_sensitive

⠀**PII Map Structure**
Example output:
{
  "email": {
	"entity": "EMAIL",
	"category": "identifier",
	"confidence": 0.99,
	"evidence": ["EMAIL_PATTERN_V5"]
  },
  "dob": {
	"entity": "DATE",
	"category": "quasi_identifier",
	"confidence": 0.95
  },
  "diagnosis": {
	"entity": "MEDICAL_CONDITION",
	"category": "sensitive",
	"confidence": 0.87
  }
}
**Downstream Integration**
This structure is sent to:
* Masking Service (for transformation selection)
* Validation Component (for privacy metric computation)
* Audit Component (for governance and traceability)

⠀**7.2.6 Data Inputs and Outputs**
**7.2.6.1 Inputs**
The NLP Component receives structured, semi-structured, and unstructured data originating from the Intake & Metadata Extraction Layer. The following input artifacts are consumed:
* **Raw Cell Values**
  * Free-text strings
  * Numeric values
  * Alphanumeric identifiers
  * Mixed-format fields (e.g., “John – 555-0188 – NY”)
  * Multi-sentence clinical or operational notes
* **Column-Level Metadata**
  * Column name
  * Declared data type
  * Statistical distribution (min, max, entropy, uniqueness)
  * Null density
  * Sample values
  * Histograms (when available)
* **Table-Level Metadata**
  * Schema name
  * Primary key candidate indicators
  * Row count, column count
  * Table semantic profile (if detected)
* **Language & Encoding Metadata**
  * Character encoding (UTF-8 normalized)
  * Detected dominant language per column
  * Tokenization strategy selection flags
* **Orchestrator Control Signals**
  * Job identifiers
  * Processing deadlines
  * Policy thresholds (k, l, t targets)
  * Versioned pattern packs
  * ML model version

⠀**7.2.6.2 Outputs**
The NLP Component emits structured outputs that represent all detected privacy-relevant signals:
* **PII Detection Events**  Each detection is emitted as a normalized record:

⠀{

 column: "email",
  valueSample: "user@example.com",
  piiType: "identifier",
  detectionMethod: "regex",
  confidence: 1.0,
  patternId: "EMAIL_V4",
  modelVersion: "NLP-1.3.2"
}
* **Column Classification Summary**  Defines the final privacy label for the field:
  * Identifier
  * Quasi-Identifier
  * Sensitive Attribute
  * Non-Sensitive
* **PII Map (Primary Downstream Artifact)**  A structured map consumed by Masking and Validation:

⠀{
  "email": { category: "identifier", confidence: 1.0 },
  "zipcode": { category: "quasi_identifier", confidence: 0.92 },
  "diagnosis": { category: "sensitive", confidence: 0.98 }
}
* **Contextual Annotation Events**  Metadata indicating the nature of detected entities:
  * linguistic cues
  * semantic context
  * neighboring column influence
* **Audit Messages**  Cryptographically chained records summarizing:

⠀o   patterns executed
o   ML inference decisions
o   version usage
o   errors, warnings
 **7.2.7 Processing Workflow Overview**
The NLP Component executes a deterministic multi-stage workflow.  This workflow ensures that noisy or inconsistent raw data is transformed into high-quality privacy signals.
**7.2.7.1 Data Normalization**
* Unicode normalization (NFC → UTF-8)
* Removal of zero-width characters
* Whitespace collapsing
* Canonicalization of digits, Arabic/Indic numerals
* Date normalization (e.g., ١٤/٠١/٢٠٢٥ → 2025-01-14)

⠀**Goal:** Ensure consistent input format for all downstream detectors.
**7.2.7.2 Language Detection & Tokenization**
* Detect language per cell or per column
* Arabic-aware tokenization
* English morphological tokenization
* Mixed-script handling (Arabic + Latin)
* Numeric token segmentation

⠀**Goal:** Select correct rule-set and ML model.
**7.2.7.3 Pattern Matching (Deterministic PII Detection)**
Executes the Pattern Engine:
* Email patterns
* Phone number patterns
* National ID / Iqama patterns
* Passport formats
* IBAN
* IP addresses
* Medical record number patterns

⠀**Goal:** Capture high-confidence PII using deterministic logic.
**7.2.7.4 Statistical Entity Recognition (ML Classifier)**
Applies the machine-learning submodule to detect entities such as:
* Person names
* Facility names
* Clinical terms
* Medications
* Diagnoses
* Locations
* Occupations

⠀**Goal:** Capture PII not detectable by fixed patterns.
**7.2.7.5 Contextual Consistency Checks**
* Cross-column correlation (e.g., DOS + Name + Phone → Re-identification risk)
* Entropy-based identifier detection
* Numeric-sequence probability checks

⠀**Goal:** Improve classification reliability by analyzing context.
**7.2.7.6 PII Scoring and Fusion**
Combines signals from:
* heuristic inference
* regex matches
* NER predictions
* distributional statistics

⠀Using weighted confidence formulas such as:
FinalConfidence = 0.45*Regex + 0.35*NER + 0.20*Heuristic
**Goal:** Produce unified, reliable label per field.
**7.2.7.7 PII Map Construction**
Builds the final consolidated artifact consumed by Masking and Validation.  Ensures consistent structure across job runs.
**7.2.7.8 Emission to Downstream Components**
Outputs are dispatched:
* to Masking via REST/gRPC
* to Validation via structured privacy map
* to Audit via tamper-evident logging

⠀7.2.8 Performance Considerations
The NLP Component is designed to operate efficiently within a high-throughput anonymization pipeline, balancing accuracy with computational scalability. The following performance considerations govern its design:
**High-Throughput Batch Processing**  The component processes datasets in columnar batches to minimize overhead and leverage parallelizable operations across columns. Deterministic pattern matching and normalization are vectorized where possible to reduce per-row latency.
**Asynchronous and Parallel Execution**  Normalization, tokenization, and statistical profiling are executed concurrently using a multi-worker pool model. This ensures that large datasets (1M+ rows) can be processed without saturating a single worker.
**Lightweight Deterministic Rules**  Regex-based deterministic detections are optimized using precompiled pattern automata to reduce regex evaluation cost. Patterns are grouped by language and token class to prevent unnecessary evaluations.
**Model Loading Optimization**  Machine-learning (NER) models are loaded once per worker process and cached in memory. Lazy-loading is employed to avoid overhead for columns that do not contain textual or free-form data.
**Memory Efficiency**  Internal structures (NormalizedCell, Token, PatternMatch) are designed to minimize memory footprint by storing normalized values and token arrays only when required.
**Adaptive ML Invocation**  Statistical heuristics determine whether a column requires ML-based detection. Columns with low textual entropy, numeric dominance, or deterministic matches bypass NER inference entirely.
**Streaming Audit Logging**  AuditRecord objects are streamed to the Audit Component rather than buffered in memory. This reduces memory pressure during processing of large datasets.
**Pattern Ordering Heuristics**  Patterns are executed in descending order of expected match rate and computational efficiency to maximize early-term signal extraction.
**Timeout and Budget Controls**  Each stage of the pipeline is assigned an execution budget. Long-running ML steps are terminated if deterministic evidence is already sufficient for classification.
**Performance Telemetry**  The component generates telemetry metrics including processing time (per column and per stage), match density, ML invocation count, and anomaly rate. These metrics support the Validation and Monitoring subsystems.
**7.2.9 Security Considerations**
The NLP Component handles sensitive and potentially identifying information, and therefore adheres to strict security and privacy policies consistent with organizational and regulatory requirements.
**In-Memory Data Protection**  All raw values and normalized values remain in volatile memory. No temporary files are written to disk. Sensitive data is zeroed out in memory after downstream processing completes.
**No Persistent Storage of Raw Data**  The component does not persist unmasked data, preprocessed values, or intermediate tokens. Only classification summaries (PII Map) are forwarded downstream.
**Secure Hashing for Audit Events**  All values included in AuditRecord events are hashed using SHA-256 before transmission. The component never sends raw PII content to the Audit system.
**Strict Access Boundaries**  The NLP subsystem exposes no external API endpoints. It is accessible exclusively through the Orchestration Layer and operates within a sandboxed execution environment.
**Model Integrity Validation**  ML models and pattern packs include embedded version identifiers and signatures. At initialization, the component verifies:
* cryptographic signatures
* version compatibility
* integrity checksum

⠀Unauthorized or tampered models are rejected.
**Pattern Safety Controls**  Patterns are validated to avoid catastrophic backtracking or runtime explosions. Only approved, bounded-regex patterns are deployed.
**Data Minimization Principle**  Only metadata required for classification is propagated to downstream components. No reconstructed row-level information is retained.
**Isolation of Multilingual Models**  Arabic and English models are isolated to prevent cross-language contamination and reduce attack surface.
**Transport Security**  Communication with Masking Service, Validation Component, and Audit Component occurs via secure internal channels using mTLS (mutual TLS) with certificate pinning.
**Protection Against Adversarial Attacks**  The component employs anomaly detectors to identify:
* hostile Unicode inputs
* adversarially perturbed entities
* injection-like patterns

⠀Suspicious values trigger quarantine events logged to the Audit system.
**7.2.10 Error Handling**
The NLP Component implements a structured error-handling strategy to ensure robustness, traceability, and fault isolation.
**Input-Level Errors**  Encoding errors (e.g., invalid UTF-8 sequences) are corrected using fallback normalization rules. If unsuccessful, the cell is marked as corrupted and logged to the ErrorReport structure.
**Pattern Matching Failures**  Regex evaluation errors (e.g., malformed sequences or catastrophic matches) are caught and isolated. Faulty values are skipped while preserving pipeline continuity.
**ML Inference Errors**  Failures such as model unavailability, timeout, or inference exceptions result in:
* fallback to deterministic rules
* degradation to heuristic classification
* logging of the event to the DLQ (Dead-Letter Queue)

⠀**Timeout Management**  Each pipeline stage employs execution budgets. Stages exceeding their timeout threshold are terminated gracefully and marked as degraded processing paths.
**Graceful Degradation**  If contextual fusion or ML-based scoring fails, classification falls back to:
* regex-only evaluation
* heuristic scoring
* statistical profiling

⠀This ensures the system always produces a usable PII Map, even under partial degradation.
**Component-Level Failures**  If a fatal exception occurs:
* processing is halted for the affected dataset
* an ErrorReport is generated
* a DLQ entry is produced
* the Orchestration Layer is notified for retry or escalation
* When retry limits are exceeded, NLP tasks are routed to a Dead-Letter Queue (DLQ) for controlled failure handling, forensic inspection, and potential reprocessing.

⠀**Audit Logging for Errors**  Every error-regardless of severity-is hashed and logged as an AuditRecord event to ensure post-incident traceability.
**Cross-Service Error Propagation**  Errors propagating from downstream systems (Masking, Validation, Storage) are handled through:
structured error codes
retry semantics
circuit-breaker logic
**Recovery Procedures**  The component supports:
automatic retry with exponential backoff
reinitialization of models
clearing of corrupted pattern packs
graceful restoration of processing state
### 7.3 Masking Service Component
**7.3.1 Overview**
The Masking Service is responsible for applying data transformation techniques to anonymize sensitive datasets based on classification configurations provided by the Validation Service. This component represents the core anonymization engine of the Saudi Anonymization and Data Masking Network, implementing five distinct transformation techniques that collectively ensure regulatory compliance while preserving data utility for analytical purposes.
The Masking Service is implemented in C# using the .NET 8 runtime, diverging from the Python-based implementation of other SADN microservices. This technology decision reflects two primary considerations: the computational intensity of transformation operations applied to datasets containing up to 500 megabytes of data, and the availability of mature, audited cryptographic libraries within the .NET ecosystem for pseudonymization operations.
The architectural position of the Masking Service within the processing pipeline is documented in Section 5.3.7. This section provides component-level design specifications including transformation algorithms, interface contracts, data access patterns, error handling strategies, and configuration parameters.
**7.3.1.1 Component Diagram**


*Figure 10.* 
### Masking Service Component Architecture
**7.3.2 Transformation Algorithms**
This section specifies the algorithms implemented by each transformation module within the Masking Service. Each algorithm is presented with its purpose, input/output specifications, pseudocode, and implementation considerations.
**7.3.2.1 Transformation Execution Order**
The Transformation Engine applies techniques in a strictly defined sequence to ensure data consistency and prevent conflicts between transformation operations:
| **Order** | **Transformation** | **Rationale** |
|:-:|:-:|:-:|
| 1 | Suppression | Removes columns before other operations to reduce processing scope |
| 2 | Date Shifting | Modifies temporal values before generalization to preserve shift consistency |
| 3 | Generalization | Applies hierarchical reduction after structural changes are complete |
| 4 | Pseudonymization | Replaces identifiers after generalization to ensure consistent mapping |
| 5 | NLP Redaction | Processes text fields last as redaction depends on finalized column structure |
*Table 95.* 
**Execution Order Pseudocode:**
FUNCTION TransformDataset(dataset, classificationConfig, nlpAnnotations)
    // Phase 1: Structural transformation (column removal)
    columnsToSuppress ← GetColumnsWithTransformation(classificationConfig, "SUPPRESS")
    dataset ← Suppressor.Execute(dataset, columnsToSuppress)
    
    // Phase 2: Temporal transformation
    dateColumns ← GetColumnsWithTransformation(classificationConfig, "DATE_SHIFT")
    dataset ← DateShifter.Execute(dataset, dateColumns)
    
    // Phase 3: Value transformation (categorical/numerical)
    quasiIdentifiers ← GetColumnsWithTransformation(classificationConfig, "GENERALIZE")
    dataset ← Generalizer.Execute(dataset, quasiIdentifiers)
    
    // Phase 4: Identifier replacement
    linkageColumns ← GetColumnsWithTransformation(classificationConfig, "PSEUDONYMIZE")
    dataset ← Pseudonymizer.Execute(dataset, linkageColumns)
    
    // Phase 5: Text transformation
    textColumns ← GetColumnsWithTransformation(classificationConfig, "NLP_REDACT")
    dataset ← TextRedactor.Execute(dataset, textColumns, nlpAnnotations)
    
    RETURN dataset
END FUNCTION
**7.3.2.2 Suppression Algorithm**
**Purpose:** Remove direct identifier columns entirely from the output dataset, ensuring that attributes capable of uniquely identifying individuals are not present in the anonymized output.
**Input:**
* Dataset containing all original columns
* List of column names classified as Direct Identifiers

⠀**Output:**
* Dataset with specified columns removed

⠀**Algorithm Specification:**
FUNCTION Suppressor.Execute(dataset, columnsToSuppress)
    FOR EACH columnName IN columnsToSuppress DO
        IF dataset.HasColumn(columnName) THEN
            dataset.RemoveColumn(columnName)
            Log.Info("Suppressed column: {columnName}")
        ELSE
            Log.Warning("Column not found for suppression: {columnName}")
        END IF
    END FOR
    
    RETURN dataset
END FUNCTION
**Implementation Considerations:**
| **Consideration** | **Specification** |
|:-:|:-:|
| Column validation | Verify column exists before removal; log warning if not found |
| Metadata update | Update column count in dataset metadata after suppression |
| Memory management | Release memory associated with removed columns immediately |
| Audit logging | Record suppressed column names for audit trail |
*Table 96.* 
**Example:**
| **Before Suppression** | **After Suppression** |
|:-:|:-:|
| patient_id, name, phone, age, gender, diagnosis | age, gender, diagnosis |
*Table 97.* 
**7.3.2.3 Generalization Algorithm**
**Purpose:** Replace specific values with broader categorical ranges to reduce the uniqueness of quasi-identifier combinations while preserving analytical utility.
**Input:**
* Dataset with quasi-identifier columns
* Generalization hierarchies for each quasi-identifier
* Target generalization level (determined by k-anonymity requirements)

⠀**Output:**
* Dataset with generalized quasi-identifier values

⠀**7.3.2.3.1 Generalization Hierarchies**
Generalization hierarchies define the categorical structure through which values are progressively generalized. Each hierarchy is a directed acyclic graph where leaf nodes represent original values and parent nodes represent generalized categories.
**Age Hierarchy:**
Level 0 (Original):  0, 1, 2, ... 99, 100+
Level 1 (5-year):    0-4, 5-9, 10-14, ... 95-99, 100+
Level 2 (10-year):   0-9, 10-19, 20-29, ... 90-99, 100+
Level 3 (20-year):   0-19, 20-39, 40-59, 60-79, 80+
Level 4 (Category):  Child (0-17), Adult (18-64), Senior (65+)
Level 5 (Suppressed): *
**Location Hierarchy (Saudi Arabia):**
Level 0 (Original):  Al-Khobar, Dammam, Dhahran, Jubail, ...
Level 1 (City):      Al-Khobar, Dammam, Dhahran, Jubail, Riyadh, Jeddah, ...
Level 2 (Province):  Eastern Province, Riyadh Province, Makkah Province, ...
Level 3 (Region):    Eastern, Central, Western, Northern, Southern
Level 4 (Country):   Saudi Arabia
Level 5 (Suppressed): *
**Date Hierarchy:**
Level 0 (Original):  2024-03-15
Level 1 (Week):      2024-W11
Level 2 (Month):     2024-03
Level 3 (Quarter):   2024-Q1
Level 4 (Year):      2024
Level 5 (Decade):    2020s
Level 6 (Suppressed): *
**Gender Hierarchy:**
Level 0 (Original):  Male, Female
Level 1 (Suppressed): *
**7.3.2.3.2 Generalization Algorithm Pseudocode**
FUNCTION Generalizer.Execute(dataset, quasiIdentifiers)
    FOR EACH column IN quasiIdentifiers DO
        hierarchy ← LoadHierarchy(column.name, column.dataType)
        targetLevel ← column.generalizationLevel  // From classification config
        
        FOR EACH row IN dataset.Rows DO
            originalValue ← row[column.name]
            generalizedValue ← ApplyHierarchy(originalValue, hierarchy, targetLevel)
            row[column.name] ← generalizedValue
        END FOR
        
        Log.Info("Generalized column {column.name} to level {targetLevel}")
    END FOR
    
    RETURN dataset
END FUNCTION

FUNCTION ApplyHierarchy(value, hierarchy, targetLevel)
    currentNode ← hierarchy.FindLeafNode(value)
    
    IF currentNode IS NULL THEN
        Log.Warning("Value not found in hierarchy: {value}")
        RETURN "*"  // Suppress unknown values
    END IF
    
    FOR level FROM 0 TO targetLevel DO
        IF currentNode.Parent IS NOT NULL THEN
            currentNode ← currentNode.Parent
        ELSE
            BREAK  // Already at root
        END IF
    END FOR
    
    RETURN currentNode.Label
END FUNCTION
**7.3.2.3.3 Generalization Information Loss Calculation**
The Masking Service calculates the information loss incurred by generalization for reporting purposes:
FUNCTION CalculateGeneralizationInfoLoss(column, hierarchy, targetLevel)
    maxLevel ← hierarchy.MaxDepth
    infoLoss ← targetLevel / maxLevel
    RETURN infoLoss
END FUNCTION

FUNCTION CalculateAverageGIL(dataset, generalizedColumns)
    totalLoss ← 0
    FOR EACH column IN generalizedColumns DO
        totalLoss ← totalLoss + CalculateGeneralizationInfoLoss(column, ...)
    END FOR
    averageGIL ← totalLoss / COUNT(generalizedColumns)
    RETURN averageGIL
END FUNCTION
**Example:**
| **Original Value** | **Level 1** | **Level 2** | **Level 3** |
|:-:|:-:|:-:|:-:|
| Age: 34 | 30-34 | 30-39 | Adult (18-64) |
| City: Dammam | Dammam | Eastern Province | Eastern |
| Date: 2024-03-15 | 2024-W11 | 2024-03 | 2024-Q1 |
*Table 98.* 
**7.3.2.4 Pseudonymization Algorithm**
**Purpose:** Replace identifying values with consistent, non-reversible pseudonyms that enable longitudinal analysis across records belonging to the same individual while preventing identification without access to the cryptographic key.
**Input:**
* Dataset with linkage columns requiring pseudonymization
* Job-specific salt for HMAC computation

⠀**Output:**
* Dataset with pseudonymized identifiers

⠀**7.3.2.4.1 Salt Generation**
Each anonymization job generates a unique cryptographic salt used for HMAC-SHA256 pseudonymization. The salt ensures that identical input values produce different pseudonyms across different jobs, preventing cross-job re-identification attacks.
FUNCTION GenerateJobSalt(jobId)
    // Combine job ID with cryptographically secure random bytes
    randomBytes ← CryptoRandom.GetBytes(32)  // 256 bits
    saltInput ← Concatenate(jobId.ToBytes(), randomBytes)
    salt ← SHA256.Hash(saltInput)
    
    // Store salt securely for potential authorized re-identification
    SecureKeyStore.Store(jobId, salt, expiryDate: NOW + 7 YEARS)
    
    RETURN salt
END FUNCTION
**7.3.2.4.2 HMAC-SHA256 Pseudonymization**
FUNCTION Pseudonymizer.Execute(dataset, linkageColumns)
    salt ← GetOrGenerateJobSalt(currentJobId)
    pseudonymCache ← new Dictionary<string, string>()
    
    FOR EACH column IN linkageColumns DO
        FOR EACH row IN dataset.Rows DO
            originalValue ← row[column.name]
            
            IF originalValue IS NULL OR originalValue IS EMPTY THEN
                row[column.name] ← NULL
                CONTINUE
            END IF
            
            // Check cache for consistency within same job
            cacheKey ← column.name + ":" + originalValue
            IF pseudonymCache.Contains(cacheKey) THEN
                row[column.name] ← pseudonymCache[cacheKey]
            ELSE
                pseudonym ← GeneratePseudonym(originalValue, salt, column.name)
                pseudonymCache[cacheKey] ← pseudonym
                row[column.name] ← pseudonym
            END IF
        END FOR
        
        Log.Info("Pseudonymized column: {column.name}, unique values: {pseudonymCache.Count}")
    END FOR
    
    RETURN dataset
END FUNCTION

FUNCTION GeneratePseudonym(value, salt, columnName)
    // Include column name to prevent cross-column attacks
    input ← Concatenate(columnName, ":", value)
    
    // Compute HMAC-SHA256
    hmac ← HMAC_SHA256(key: salt, message: input.ToBytes())
    
    // Encode as hexadecimal string (first 24 characters for readability)
    pseudonym ← ToHexString(hmac).Substring(0, 24)
    
    RETURN pseudonym
END FUNCTION
**7.3.2.4.3 Key Storage Specification**
| **Attribute** | **Specification** |
|:-:|:-:|
| Storage location | Secure key vault (Azure Key Vault, HashiCorp Vault, or encrypted PostgreSQL column) |
| Key format | 256-bit (32 bytes) raw binary |
| Retention period | 7 years (aligned with MOH IS0303 requirements) |
| Access control | Restricted to authorized re-identification requests with legal basis |
| Rotation | Not applicable (job-specific salts are not rotated) |
*Table 99.* 
**Example:**
| **Original Value** | **Pseudonym** |
|:-:|:-:|
| P12345 | a7b3c9d2e1f4g5h6i7j8k9l0 |
| P12345 (same patient, different record) | a7b3c9d2e1f4g5h6i7j8k9l0 (consistent) |
| P67890 | m1n2o3p4q5r6s7t8u9v0w1x2 |
*Table 100.* 
**7.3.2.5 Date Shifting Algorithm**
**Purpose:** Apply a random temporal offset to date columns while preserving the relative intervals between dates within the same record or patient group, enabling temporal analysis while preventing identification through date-based attacks.
**Input:**
* Dataset with date columns requiring shifting
* Patient/record identifier for consistent shifting (optional)

⠀**Output:**
* Dataset with shifted date values

⠀**7.3.2.5.1 Offset Calculation**
FUNCTION DateShifter.Execute(dataset, dateColumns)
    offsetCache ← new Dictionary<string, int>()  // patientId → offset
    
    // Determine if dataset has patient identifier for consistent shifting
    patientIdColumn ← FindPatientIdentifierColumn(dataset)
    
    FOR EACH row IN dataset.Rows DO
        // Determine offset for this row
        IF patientIdColumn IS NOT NULL THEN
            patientId ← row[patientIdColumn]
            IF NOT offsetCache.Contains(patientId) THEN
                offsetCache[patientId] ← GenerateOffset(patientId)
            END IF
            offset ← offsetCache[patientId]
        ELSE
            // No patient ID: use row-based deterministic offset
            offset ← GenerateOffset(row.Index.ToString())
        END IF
        
        // Apply offset to all date columns in this row
        FOR EACH column IN dateColumns DO
            originalDate ← row[column.name]
            IF originalDate IS NOT NULL THEN
                shiftedDate ← originalDate.AddDays(offset)
                row[column.name] ← shiftedDate
            END IF
        END FOR
    END FOR
    
    Log.Info("Date shifting complete. Offset range: {MIN_OFFSET} to {MAX_OFFSET} days")
    RETURN dataset
END FUNCTION

FUNCTION GenerateOffset(seed)
    // Deterministic offset based on seed (for consistency across records)
    hash ← SHA256.Hash(Concatenate(currentJobId, ":", seed))
    
    // Convert first 4 bytes to integer
    rawOffset ← BytesToInt32(hash[0..3])
    
    // Map to configured range (default: -365 to +365 days)
    offset ← (rawOffset MOD (MAX_OFFSET - MIN_OFFSET + 1)) + MIN_OFFSET
    
    RETURN offset
END FUNCTION
**7.3.2.5.2 Interval Preservation**
The algorithm ensures that temporal relationships between dates within the same record are preserved:
| **Patient** | **Original admission_date** | **Original surgery_date** | **Original discharge_date** | **Offset** | **Shifted admission_date** | **Shifted surgery_date** | **Shifted discharge_date** |
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| P001 | 2024-01-10 | 2024-01-15 | 2024-01-20 | +64 | 2024-03-15 | 2024-03-20 | 2024-03-25 |
| P001 | 2024-06-01 | 2024-06-03 | 2024-06-10 | +64 | 2024-08-04 | 2024-08-06 | 2024-08-13 |
| P002 | 2024-02-20 | 2024-02-22 | 2024-02-28 | -120 | 2023-10-23 | 2023-10-25 | 2023-10-31 |
*Table 101.* 
**Observation:** The intervals between dates (5 days from admission to surgery, 5 days from surgery to discharge) are preserved, enabling clinical pathway analysis without revealing actual dates.
**7.3.2.5.3 Configuration Parameters**
| **Parameter** | **Default Value** | **Description** |
|:-:|:-:|:-:|
| MIN_OFFSET | -365 | Minimum shift in days |
| MAX_OFFSET | +365 | Maximum shift in days |
| PRESERVE_YEAR | false | If true, offset is constrained to keep dates within same calendar year |
| PRESERVE_SEASON | false | If true, offset is constrained to ±45 days to preserve seasonal patterns |
*Table 102.* 
**7.3.2.6 NLP Redaction Algorithm**
**Purpose:** Replace detected PII entities within free-text columns with placeholder tokens based on annotations provided by the NLP Service, ensuring that sensitive information embedded in narrative content is removed while preserving text structure and readability.
**Input:**
* Dataset with free-text columns
* NLP annotations containing entity positions and types

⠀**Output:**
* Dataset with redacted text values

⠀**7.3.2.6.1 Placeholder Token Format**
| **Entity Type** | **Placeholder Token** | **Example** |
|:-:|:-:|:-:|
| PERSON | [PERSON] | Ahmed Al-Saud → [PERSON] |
| NATIONAL_ID | [NATIONAL_ID] | 1234567890 → [NATIONAL_ID] |
| IQAMA | [IQAMA] | 2123456789 → [IQAMA] |
| IBAN | [IBAN] | SA1234567890123456789012 → [IBAN] |
| PHONE | [PHONE] | +966501234567 → [PHONE] |
| EMAIL | [EMAIL] | user@domain.com → [EMAIL] |
| LOCATION | [LOCATION] | Dammam → [LOCATION] |
| ORGANIZATION | [ORGANIZATION] | ARAMCO → [ORGANIZATION] |
| DATE | [DATE] | 2024-03-15 → [DATE] |
| MEDICAL_RECORD | [MEDICAL_RECORD] | MRN-12345 → [MEDICAL_RECORD] |
| INSURANCE_ID | [INSURANCE_ID] | INS123456 → [INSURANCE_ID] |
*Table 103.* 
**7.3.2.6.2 Redaction Algorithm**
FUNCTION TextRedactor.Execute(dataset, textColumns, nlpAnnotations)
    // Group annotations by row and column for efficient lookup
    annotationIndex ← BuildAnnotationIndex(nlpAnnotations)
    
    FOR EACH column IN textColumns DO
        FOR EACH row IN dataset.Rows DO
            originalText ← row[column.name]
            
            IF originalText IS NULL OR originalText IS EMPTY THEN
                CONTINUE
            END IF
            
            // Get annotations for this cell, sorted by position descending
            cellAnnotations ← annotationIndex.Get(row.Index, column.name)
            cellAnnotations ← SortByPositionDescending(cellAnnotations)
            
            // Apply redactions from end to start (preserves positions)
            redactedText ← originalText
            FOR EACH annotation IN cellAnnotations DO
                placeholder ← GetPlaceholder(annotation.entityType)
                redactedText ← ReplaceRange(
                    redactedText,
                    annotation.startPosition,
                    annotation.endPosition,
                    placeholder
                )
            END FOR
            
            row[column.name] ← redactedText
        END FOR
        
        Log.Info("Redacted column: {column.name}")
    END FOR
    
    RETURN dataset
END FUNCTION

FUNCTION BuildAnnotationIndex(nlpAnnotations)
    index ← new Dictionary<(int, string), List<Annotation>>()
    
    FOR EACH annotation IN nlpAnnotations DO
        key ← (annotation.rowIndex, annotation.columnName)
        IF NOT index.Contains(key) THEN
            index[key] ← new List<Annotation>()
        END IF
        index[key].Add(annotation)
    END FOR
    
    RETURN index
END FUNCTION

FUNCTION ReplaceRange(text, startPos, endPos, replacement)
    prefix ← text.Substring(0, startPos)
    suffix ← text.Substring(endPos)
    RETURN Concatenate(prefix, replacement, suffix)
END FUNCTION
**7.3.2.6.3 Overlapping Entity Handling**
When multiple entities overlap (e.g., a person name containing a location), the algorithm applies the following resolution strategy:
FUNCTION ResolveOverlaps(annotations)
    // Sort by start position, then by length (longer first)
    sorted ← SortBy(annotations, a => (a.startPosition, -a.length))
    
    resolved ← new List<Annotation>()
    lastEndPosition ← -1
    
    FOR EACH annotation IN sorted DO
        IF annotation.startPosition >= lastEndPosition THEN
            // No overlap: include this annotation
            resolved.Add(annotation)
            lastEndPosition ← annotation.endPosition
        ELSE
            // Overlap: skip (previous longer annotation takes precedence)
            Log.Debug("Skipped overlapping annotation: {annotation.entityType}")
        END IF
    END FOR
    
    RETURN resolved
END FUNCTION
**Example:**
| **Original Text** | **After Redaction** |
|:-:|:-:|
| Ahmed Al-Saud visited King Fahd Hospital on 2024-03-15 | [PERSON] visited [ORGANIZATION] on [DATE] |
| Contact: +966501234567, email: ahmed@hospital.sa | Contact: [PHONE], email: [EMAIL] |
| Patient MRN-12345 from Dammam, Eastern Province | Patient [MEDICAL_RECORD] from [LOCATION], [LOCATION] |
*Table 104.* 
**7.3.3 Interface Specification**
This section defines the external interfaces through which the Masking Service communicates with other SADN components.
**7.3.3.1 Queue Input: masking_queue**
The Masking Service consumes messages from the masking_queue to receive transformation requests.
**Message Schema:**
json
{
  "job_id": "UUID",
  "file_path": "string",
  "classification_config": {
    "columns": [
      {
        "name": "string",
        "index": "integer",
        "type": "DIRECT_ID | QUASI_ID | SENSITIVE | FREE_TEXT",
        "transformation": "SUPPRESS | GENERALIZE | PSEUDONYMIZE | DATE_SHIFT | NLP_REDACT | KEEP",
        "generalization_level": "integer (optional)",
        "hierarchy_name": "string (optional)"
      }
    ]
  }
}
**Example Message:**
json
{
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "file_path": "staging/550e8400-e29b-41d4-a716-446655440000/original.csv",
  "classification_config": {
    "columns": [
      {
        "name": "patient_id",
        "index": 0,
        "type": "DIRECT_ID",
        "transformation": "SUPPRESS"
      },
      {
        "name": "national_id",
        "index": 1,
        "type": "DIRECT_ID",
        "transformation": "SUPPRESS"
      },
      {
        "name": "age",
        "index": 2,
        "type": "QUASI_ID",
        "transformation": "GENERALIZE",
        "generalization_level": 2,
        "hierarchy_name": "age_10year"
      },
      {
        "name": "city",
        "index": 3,
        "type": "QUASI_ID",
        "transformation": "GENERALIZE",
        "generalization_level": 1,
        "hierarchy_name": "saudi_location"
      },
      {
        "name": "admission_date",
        "index": 4,
        "type": "QUASI_ID",
        "transformation": "DATE_SHIFT"
      },
      {
        "name": "mrn",
        "index": 5,
        "type": "DIRECT_ID",
        "transformation": "PSEUDONYMIZE"
      },
      {
        "name": "diagnosis",
        "index": 6,
        "type": "SENSITIVE",
        "transformation": "KEEP"
      },
      {
        "name": "clinical_notes",
        "index": 7,
        "type": "FREE_TEXT",
        "transformation": "NLP_REDACT"
      }
    ]
  }
}
**Consumer Configuration:**
| **Parameter** | **Value** |
|:-:|:-:|
| Queue name | masking_queue |
| Prefetch count | 1 (process one job at a time) |
| Auto-acknowledge | false (manual acknowledgment after successful processing) |
| Dead letter exchange | masking_dlx |
| Max retry attempts | 3 |
*Table 105.* 
**7.3.3.2 HTTP Output: Storage Service**
Upon completing transformations, the Masking Service sends the masked file to the Storage Service via HTTP POST.
**Endpoint:** POST /internal/files/{job_id}/masked
**Request:**
http
POST /internal/files/550e8400-e29b-41d4-a716-446655440000/masked HTTP/1.1
Host: storage-service:8080
Content-Type: multipart/form-data; boundary=----FormBoundary
Content-Length: 1048576

------FormBoundary
Content-Disposition: form-data; name="file"; filename="masked.csv"
Content-Type: text/csv

age_range,city,admission_date,mrn_pseudo,diagnosis,clinical_notes
30-39,Eastern Province,2024-05-20,a7b3c9d2e1f4g5h6i7j8k9l0,Diabetes Type 2,[PERSON] presented with symptoms...
...
------FormBoundary--
**Response (Success):**
http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "status": "stored",
  "file_path": "staging/550e8400-e29b-41d4-a716-446655440000/masked.csv",
  "file_size_bytes": 1048576,
  "checksum": "sha256:abc123..."
}
**Response (Error):**
http
HTTP/1.1 500 Internal Server Error
Content-Type: application/json

{
  "error": "storage_error",
  "message": "Failed to write file to MinIO",
  "details": {
    "minio_error": "connection timeout"
  }
}
**7.3.3.3 Queue Output: validation_queue**
After successfully storing the masked file, the Masking Service publishes a message to trigger privacy validation.
**Message Schema:**
json
{
  "job_id": "UUID",
  "action": "VALIDATE_PRIVACY",
  "file_path": "string",
  "masked_file_path": "string",
  "transformation_summary": {
    "suppressed_columns": ["string"],
    "generalized_columns": ["string"],
    "pseudonymized_columns": ["string"],
    "date_shifted_columns": ["string"],
    "redacted_columns": ["string"]
  }
}
**Example Message:**
json
{
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "action": "VALIDATE_PRIVACY",
  "file_path": "staging/550e8400-e29b-41d4-a716-446655440000/original.csv",
  "masked_file_path": "staging/550e8400-e29b-41d4-a716-446655440000/masked.csv",
  "transformation_summary": {
    "suppressed_columns": ["patient_id", "national_id"],
    "generalized_columns": ["age", "city"],
    "pseudonymized_columns": ["mrn"],
    "date_shifted_columns": ["admission_date"],
    "redacted_columns": ["clinical_notes"]
  }
}
**7.3.3.4 Queue Output: audit_queue**
The Masking Service publishes an audit event upon completion of transformation operations.
**Message Schema:**
json
{
  "event_id": "UUID",
  "job_id": "UUID",
  "event_type": "MASKING_COMPLETE",
  "timestamp": "ISO 8601",
  "actor_id": "masking-service",
  "details": {
    "original_row_count": "integer",
    "masked_row_count": "integer",
    "transformations_applied": {
      "suppression": "integer",
      "generalization": "integer",
      "pseudonymization": "integer",
      "date_shifting": "integer",
      "nlp_redaction": "integer"
    },
    "processing_time_ms": "integer"
  }
}
**Example Message:**
json
{
  "event_id": "660e8400-e29b-41d4-a716-446655440001",
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "event_type": "MASKING_COMPLETE",
  "timestamp": "2024-03-15T10:30:45.123Z",
  "actor_id": "masking-service",
  "details": {
    "original_row_count": 10000,
    "masked_row_count": 10000,
    "transformations_applied": {
      "suppression": 2,
      "generalization": 2,
      "pseudonymization": 1,
      "date_shifting": 1,
      "nlp_redaction": 1
    },
    "processing_time_ms": 4532
  }
}
**7.3.4 Data Access**
This section specifies the data access patterns employed by the Masking Service to read input data and configuration.
**7.3.4.1 MinIO Operations**
The Masking Service reads the original dataset from MinIO staging storage.
**Read Operation:**
csharp
*// C# implementation pattern*
public async Task<Dataset> ReadDatasetFromMinIO(string filePath)
{
    var minioClient = new MinioClient()
        .WithEndpoint(_config.MinioEndpoint)
        .WithCredentials(_config.MinioAccessKey, _config.MinioSecretKey)
        .WithSSL(_config.MinioUseSsl)
        .Build();
    
    var bucketName = "sadn-storage";
    var objectName = filePath;  *// e.g., "staging/job-id/original.csv"*
    
    using var memoryStream = new MemoryStream();
    
    await minioClient.GetObjectAsync(new GetObjectArgs()
        .WithBucket(bucketName)
        .WithObject(objectName)
        .WithCallbackStream(stream => stream.CopyTo(memoryStream)));
    
    memoryStream.Position = 0;
    
    *// Parse based on file format*
    var format = DetectFormat(objectName);
    return format switch
    {
        FileFormat.CSV => ParseCsv(memoryStream),
        FileFormat.JSON => ParseJson(memoryStream),
        FileFormat.Parquet => ParseParquet(memoryStream),
        FileFormat.XLSX => ParseExcel(memoryStream),
        _ => throw new UnsupportedFormatException(format)
    };
}
**Access Pattern:**
| **Operation** | **Bucket** | **Path Pattern** | **Frequency** |
|:-:|:-:|:-:|:-:|
| GET | sadn-storage | staging/{job_id}/original.csv | Once per job |
*Table 106.* 
**7.3.4.2 PostgreSQL Queries**
The Masking Service reads classification results and NLP annotations from PostgreSQL.
**Query: Classification Results**
sql
SELECT 
    classification_id,
    column_name,
    column_index,
    column_type,
    transformation,
    confidence_score,
    detection_signals
FROM classification_results
WHERE job_id = @job_id
ORDER BY column_index ASC;
**Query: NLP Annotations**
sql
SELECT 
    annotation_id,
    column_name,
    row_index,
    start_position,
    end_position,
    entity_type,
    entity_text,
    confidence_score
FROM nlp_annotations
WHERE job_id = @job_id
ORDER BY column_name, row_index, start_position ASC;
**Query: Update Job Status**
sql
UPDATE jobs
SET 
    status = 'MASKING',
    updated_at = NOW()
WHERE job_id = @job_id;
**Connection Configuration:**
| **Parameter** | **Value** |
|:-:|:-:|
| Connection pool size | 10 |
| Command timeout | 30 seconds |
| Retry attempts | 3 |
| Retry delay | 1 second (exponential backoff) |
*Table 107.* 
**7.3.5 Error Handling**
This section specifies the error handling strategies implemented by the Masking Service to ensure robust operation and appropriate failure recovery.
**7.3.5.1 Error Categories**
| **Category** | **Examples** | **Severity** | **Recovery Strategy** |
|:-:|:-:|:-:|:-:|
| Transient Infrastructure | MinIO timeout, RabbitMQ disconnect, PostgreSQL connection refused | Medium | Retry with exponential backoff |
| Data Validation | Invalid date format, null in required column, unsupported character encoding | High | Fail job with detailed error message |
| Configuration | Missing hierarchy definition, invalid generalization level | Critical | Fail job; alert operations team |
| Resource Exhaustion | Out of memory, disk full | Critical | Fail job; trigger scaling alert |
| Cryptographic | Salt generation failure, HMAC computation error | Critical | Fail job; security alert |
*Table 108.* 
**7.3.5.2 Retry Strategy**
csharp
public class RetryPolicy
{
    public int MaxRetryAttempts { get; } = 3;
    public TimeSpan InitialDelay { get; } = TimeSpan.FromSeconds(1);
    public double BackoffMultiplier { get; } = 2.0;
    public TimeSpan MaxDelay { get; } = TimeSpan.FromSeconds(30);
    
    public async Task<T> ExecuteWithRetry<T>(Func<Task<T>> operation, string operationName)
    {
        int attempt = 0;
        TimeSpan delay = InitialDelay;
        
        while (true)
        {
            try
            {
                attempt++;
                return await operation();
            }
            catch (TransientException ex)
            {
                if (attempt >= MaxRetryAttempts)
                {
                    Log.Error($"Operation {operationName} failed after {attempt} attempts: {ex.Message}");
                    throw;
                }
                
                Log.Warning($"Retry {attempt}/{MaxRetryAttempts} for {operationName}: {ex.Message}");
                await Task.Delay(delay);
                delay = TimeSpan.FromSeconds(Math.Min(delay.TotalSeconds * BackoffMultiplier, MaxDelay.TotalSeconds));
            }
        }
    }
}
**7.3.5.3 Dead Letter Queue Handling**
Messages that cannot be processed after exhausting retry attempts are routed to the dead letter queue for investigation.
**Dead Letter Message Structure:**
json
{
  "original_message": { ... },
  "failure_info": {
    "error_type": "string",
    "error_message": "string",
    "stack_trace": "string",
    "attempt_count": "integer",
    "first_attempt_at": "ISO 8601",
    "last_attempt_at": "ISO 8601"
  },
  "routing_info": {
    "original_queue": "masking_queue",
    "dead_letter_queue": "masking_dlx",
    "routing_key": "masking.failed"
  }
}
**Monitoring Alert:**
When a message is routed to the dead letter queue, an alert is generated:
| **Alert Level** | **Condition** | **Notification** |
|:-:|:-:|:-:|
| Warning | 1 DLQ message in 1 hour | Log entry |
| Error | 5 DLQ messages in 1 hour | Email to operations team |
| Critical | 20 DLQ messages in 1 hour | PagerDuty alert |
*Table 109.* 
**7.3.5.4 Partial Failure Recovery**
If a transformation fails mid-processing, the Masking Service implements atomic semantics:
FUNCTION ProcessJobAtomically(job)
    checkpoint ← CreateCheckpoint()
    
    TRY
        dataset ← ReadDataset(job.filePath)
        maskedDataset ← TransformDataset(dataset, job.config)
        SendToStorageService(maskedDataset)
        PublishValidationRequest(job)
        PublishAuditEvent(job, SUCCESS)
        AcknowledgeMessage()
    CATCH Exception AS ex
        RollbackToCheckpoint(checkpoint)
        
        IF IsRetryable(ex) AND RetryCount < MAX_RETRIES THEN
            RequeueMessage(job, RetryCount + 1)
        ELSE
            UpdateJobStatus(job.id, FAILED, ex.Message)
            PublishAuditEvent(job, FAILED, ex)
            SendToDeadLetterQueue(job, ex)
            AcknowledgeMessage()  // Remove from main queue
        END IF
    END TRY
END FUNCTION
**Atomicity Guarantees:**
| **Guarantee** | **Implementation** |
|:-:|:-:|
| No partial output | Masked file is sent to Storage Service only after all transformations complete |
| Idempotent processing | Job ID is checked before processing; duplicate messages are acknowledged without reprocessing |
| State consistency | Job status is updated only after successful Storage Service response |
*Table 110.* 
**7.3.6 Configuration**
This section specifies the configuration parameters that control the behavior of the Masking Service.
**7.3.6.1 Environment Variables**
| **Variable** | **Required** | **Default** | **Description** |
|:-:|:-:|:-:|:-:|
| RABBITMQ_HOST | Yes | - | RabbitMQ server hostname |
| RABBITMQ_PORT | No | 5672 | RabbitMQ server port |
| RABBITMQ_USER | Yes | - | RabbitMQ username |
| RABBITMQ_PASSWORD | Yes | - | RabbitMQ password |
| RABBITMQ_VHOST | No | / | RabbitMQ virtual host |
| MINIO_ENDPOINT | Yes | - | MinIO server endpoint |
| MINIO_ACCESS_KEY | Yes | - | MinIO access key |
| MINIO_SECRET_KEY | Yes | - | MinIO secret key |
| MINIO_USE_SSL | No | true | Enable TLS for MinIO connections |
| MINIO_BUCKET | No | sadn-storage | MinIO bucket name |
| POSTGRES_HOST | Yes | - | PostgreSQL server hostname |
| POSTGRES_PORT | No | 5432 | PostgreSQL server port |
| POSTGRES_DATABASE | Yes | - | PostgreSQL database name |
| POSTGRES_USER | Yes | - | PostgreSQL username |
| POSTGRES_PASSWORD | Yes | - | PostgreSQL password |
| STORAGE_SERVICE_URL | Yes | - | Storage Service base URL |
| KEY_VAULT_ENDPOINT | Yes | - | Secure key vault endpoint for salt storage |
| LOG_LEVEL | No | Information | Logging level (Debug, Information, Warning, Error) |
*Table 111.* 
**7.3.6.2 Generalization Hierarchies Configuration**
Hierarchies are defined in JSON configuration files loaded at service startup:
**File:** hierarchies/age.json
json
{
  "hierarchy_name": "age_standard",
  "data_type": "integer",
  "levels": [
    {
      "level": 0,
      "name": "exact",
      "description": "Exact age value"
    },
    {
      "level": 1,
      "name": "5-year",
      "ranges": [
        {"min": 0, "max": 4, "label": "0-4"},
        {"min": 5, "max": 9, "label": "5-9"},
        {"min": 10, "max": 14, "label": "10-14"},
        ...
        {"min": 95, "max": 99, "label": "95-99"},
        {"min": 100, "max": 999, "label": "100+"}
      ]
    },
    {
      "level": 2,
      "name": "10-year",
      "ranges": [
        {"min": 0, "max": 9, "label": "0-9"},
        {"min": 10, "max": 19, "label": "10-19"},
        ...
      ]
    },
    {
      "level": 3,
      "name": "category",
      "ranges": [
        {"min": 0, "max": 17, "label": "Child"},
        {"min": 18, "max": 64, "label": "Adult"},
        {"min": 65, "max": 999, "label": "Senior"}
      ]
    },
    {
      "level": 4,
      "name": "suppressed",
      "value": "*"
    }
  ]
}
**File:** hierarchies/saudi_location.json
json
{
  "hierarchy_name": "saudi_location",
  "data_type": "string",
  "levels": [
    {
      "level": 0,
      "name": "city",
      "description": "Exact city name"
    },
    {
      "level": 1,
      "name": "province",
      "mappings": {
        "Dammam": "Eastern Province",
        "Al-Khobar": "Eastern Province",
        "Dhahran": "Eastern Province",
        "Jubail": "Eastern Province",
        "Riyadh": "Riyadh Province",
        "Jeddah": "Makkah Province",
        "Makkah": "Makkah Province",
        "Madinah": "Madinah Province",
        ...
      }
    },
    {
      "level": 2,
      "name": "region",
      "mappings": {
        "Eastern Province": "Eastern",
        "Riyadh Province": "Central",
        "Makkah Province": "Western",
        "Madinah Province": "Western",
        ...
      }
    },
    {
      "level": 3,
      "name": "country",
      "value": "Saudi Arabia"
    },
    {
      "level": 4,
      "name": "suppressed",
      "value": "*"
    }
  ]
}
**7.3.6.3 Tunable Parameters**
| **Parameter** | **Default** | **Range** | **Description** |
|:-:|:-:|:-:|:-:|
| DATE_SHIFT_MIN_DAYS | -365 | -3650 to 0 | Minimum date shift offset |
| DATE_SHIFT_MAX_DAYS | +365 | 0 to +3650 | Maximum date shift offset |
| PSEUDONYM_LENGTH | 24 | 16 to 64 | Length of generated pseudonym (hex characters) |
| SALT_LENGTH_BYTES | 32 | 16 to 64 | Cryptographic salt length in bytes |
| MAX_FILE_SIZE_MB | 500 | 1 to 1000 | Maximum file size to process |
| PROCESSING_TIMEOUT_MINUTES | 30 | 5 to 120 | Maximum processing time per job |
| RETRY_MAX_ATTEMPTS | 3 | 1 to 10 | Maximum retry attempts for transient failures |
| RETRY_INITIAL_DELAY_SECONDS | 1 | 1 to 60 | Initial retry delay |
| RETRY_BACKOFF_MULTIPLIER | 2.0 | 1.5 to 3.0 | Exponential backoff multiplier |
*Table 112.* 

**7.3.7 Security Considerations**
**7.3.7.1 Cryptographic Standards**
| **Operation** | **Algorithm** | **Key Size** | **Standard** |
|:-:|:-:|:-:|:-:|
| Pseudonymization | HMAC-SHA256 | 256 bits | FIPS 198-1 |
| Salt generation | CSPRNG | 256 bits | NIST SP 800-90A |
| Key derivation | SHA-256 | 256 bits | FIPS 180-4 |
*Table 113.* 
**7.3.7.2 Sensitive Data Handling**
| **Data Type** | **In-Memory Handling** | **Logging Policy** |
|:-:|:-:|:-:|
| Original dataset | Cleared after processing | Never logged |
| Pseudonymization salt | Stored in secure key vault | Key ID logged, value never |
| PII values | Processed in isolated memory | Never logged |
| Masked output | Streamed to Storage Service | Metadata only |
*Table 114.* 
**7.3.7.3 Audit Trail**
All masking operations are recorded in the audit trail with the following information:
| **Field** | **Content** |
|:-:|:-:|
| Timestamp | Millisecond precision |
| Job ID | UUID reference |
| Transformation counts | Number of each transformation type applied |
| Processing duration | Milliseconds |
| Actor | Service identifier |
*Table 115.* 
### 7.4 Validation Component
The Validation Component is responsible for evaluating the privacy guarantees of anonymized datasets by computing statistical privacy metrics, verifying compliance with masking policies, and determining whether the dataset meets the minimum thresholds required for release. This component acts as the final privacy gate before data can transition into the *safe/* storage phase and become available for research or federated sharing.
**7.4.1 Purpose**
The Validation Component ensures that all masked datasets satisfy the configured privacy-preserving properties required under PDPL, NDMO data governance controls, and MOH IS0303 healthcare data requirements. Its primary goal is to prevent re-identification risks by assessing the anonymity level of processed data.
**7.4.2 Responsibilities**
The Validation Component performs the following core responsibilities:
1 Compute Privacy Metrics
	* k-anonymity: minimum equivalence class size
	* l-diversity: diversity of sensitive attributes
	* t-closeness: distributional closeness to the original dataset
	* Risk Score: quantitative re-identification risk evaluation
2 Policy Enforcement
	* Validate dataset against defined thresholds (e.g., k ≥ 5, l ≥ 2, t ≤ 0.1).
	* Load dynamic masking policies from PostgreSQL.
	* Ensure each job adheres to the assigned privacy configuration.
3 Pass/Fail Decision Logic
	* If metrics meet policy requirements → dataset approved → move to *safe/*
	* If metrics fail → dataset rejected → move to *quarantine/*
4 Result Storage
	* Insert detailed validation results into validation_results table.
	* Update job status (VALIDATION_PASSED / VALIDATION_FAILED).
5 Compliance Logging
	* Publish validation events to audit_queue including metrics, thresholds, and risk score.
	* Provide DPO visibility into decision criteria and failure reasons.
6 Integration with Storage Lifecycle
	* Publish actions to storage_queue for phase transitions:
		* PASS → safe/
		* FAIL → quarantine/

⠀**7.4.3 Inputs**
The Validation Component operates based on a structured set of inputs delivered through the validation_queue. These inputs provide all required metadata, file locations, and policy parameters needed to evaluate privacy metrics. The component consumes the following inputs:
**A. Job Identification**
Information necessary to uniquely reference the dataset and its processing context:
* job_id – Unique identifier that ties all processing stages together.
* masking_report_id – Reference to the masking output stored in PostgreSQL.

⠀**B. File References**
Pointers to the dataset versions stored in MinIO:
* masked_file_path – Location of the anonymized dataset to be evaluated.
* original_file_path – Location of the pre-masked dataset (only required to compute t-closeness).

⠀**C. Privacy Model Parameters**
Attributes necessary to calculate k-anonymity, l-diversity, and t-closeness:
* quasi_identifiers – Columns used to form equivalence classes (e.g., age, zipcode, gender).
* sensitive_attributes – Attributes whose diversity or distribution must be preserved (e.g., diagnosis).

⠀**D. Policy Reference**
Configuration governing the required privacy thresholds:
* policy_id – Identifier used to retrieve the applicable k/l/t thresholds from the policies table.

⠀**E. Supporting Metadata**
Additional context delivered with the message:
* timestamp – Event creation time, used for audit chronology.
* processing_context *(optional)* – Any pipeline metadata forwarded by the Masking Service.

⠀**7.4.4 Processing Workflow**
The Validation Component executes the following processing steps:
1 Load Files from MinIO
	* Read masked dataset
	* Optionally read original dataset (for t-closeness)
2 Load Policy Thresholds
	* Retrieve k, l, t thresholds from policies table
	* Validate policy integrity and version
3 Calculate Metrics
	* k-anonymity: minimum group size produced by quasi-identifiers
	* l-diversity: distinct sensitive values per equivalence class
	* t-closeness: Earth Mover’s Distance comparing group vs global distributions
4 Compute Risk Score
	* A 0–100 score characterizing the dataset’s re-identification risk
5 Pass/Fail Decision
	* All thresholds must be satisfied for dataset to pass
	* Failure triggers quarantine path
6 Record Results
	* Store all metric values, decisions, and thresholds in PostgreSQL
	* Publish event to audit_queue
7 Trigger Storage Transition
	* PASS → publish “MOVE_PHASE: staging → safe”
	* FAIL → publish “MOVE_PHASE: staging → quarantine”

⠀**7.4.5 Outputs**
The Validation Component produces:
**1\. Validation Results (Database Entry)**
Inserted into validation_results:
* job_id
* k_anonymity
* l_diversity
* t_closeness
* validation_passed
* risk_score
* failure_reason (if any)
* timestamp

⠀**2. RabbitMQ Event (storage_queue)**
A. PASS Event:
When the dataset satisfies all privacy requirements, the Validation Component issues a phase-transition instruction to the Storage Service.  The message indicates that the job has successfully passed validation and must be moved from the staging phase into the safe phase.
Text Description (PASS):
*“Job <job_id> has passed validation. Move dataset from the staging phase to the safe phase.”*
B. FAIL Event:
When the dataset fails one or more privacy metrics (e.g., k-anonymity, l-diversity, or t-closeness), the Validation Component instructs the Storage Service to quarantine the dataset.
Text Description (FAIL):
**7.4.6 Security Considerations**
Since Validation is the last privacy checkpoint, it enforces:
1 Strict PDPL privacy-by-design enforcement.
2 Mandatory rejection of datasets failing minimum anonymity thresholds.
3 Prevention of unsafe downstream consumption or sharing.
4 Immutable audit logging for all validation decisions.
5 Zero exposure of raw PII during computation (masked files only).

⠀**7.4.7 Failure Handling**
In case of processing errors:
* Job is marked as VALIDATION_FAILED
* File is moved to *quarantine/*
* Error reason is stored in PostgreSQL
* DPO receives detailed failure analytics
* User receives safe error message without internal details

⠀ ***Illustration Example:*** *“Job <job_id> has failed validation. Move dataset from the staging phase to the quarantine phase due to insufficient privacy metrics (example: k-anonymity below required threshold).”*

### 7.5 Storage Component
The Storage Component is responsible for the secure, structured, and compliant management of dataset files across all processing phases of the SADN pipeline. It provides internal-only endpoints for file ingestion and streaming, enforces lifecycle transitions, maintains synchronization with job metadata, and ensures adherence to retention and compliance requirements. While Section 5 describes the system-wide architecture and flow, this section focuses on the **Storage Component’s internal design**, responsibilities, and interfaces.
### 7.5.1 Component Overveiw
The Storage Component orchestrates the internal handling of dataset files throughout their entire lifecycle. This includes receiving uploaded files, conducting intake validation, maintaining both original and masked versions, performing phase transitions, updating metadata, and enforcing long-term archival requirements. Storage plays a critical role in maintaining the integrity of dataset artifacts and ensuring consistency between the physical file system and metadata stored in PostgreSQL.
To summarize its primary capabilities, the table below provides a structured view of the Storage Component’s core functions.

| **Capability** | **Description** |
|---|---|
| Dataset Intake | Receives and persists uploaded files in the intake area |
| File Validation | Ensures structural, format, and integrity checks before processing |
| Phase Transitions | Moves files across lifecycle phases using atomic operations |
| Masked Output Handling | Stores masked results and coordinates approval-based transitions |
| Metadata Synchronization | Updates database records after every storage action |
| Retention Enforcement | Applies quarantine, safe, and archive retention periods |
| Secure Internal Access | Provides restricted streaming endpoints to other services |
*Table 116.* 

**7.5.2 Provided Interfaces**
The Storage Component exposes a controlled set of internal HTTP endpoints. These endpoints are accessible only within the system’s internal network and support all necessary file operations and transitions required by dependent services.
Internal HTTP Endpoints Provided by Storage
| **Endpoint** | **Method** | **Description** | **Access Scope** |
|:-:|:-:|:-:|:-:|
| /api/v1/upload | POST | Receives uploaded dataset from Orchestrator and saves it under intake | Internal-only |
| /internal/storage/write-masked | POST | Accepts masked files from Masking Service and stores them in staging | Internal-only |
| /api/v1/move-to-safe | POST | Executes lifecycle transitions (intake → staging, staging → safe/quarantine) | Internal-only |
| /api/v1/move-to-quarantine | POST | Moves failed/rejected file from staging/ to quarantine/ | Internal-only |
| /api/v1/file/{job_id} | GET | Retrieves file for a specific job | Internal-only |
| /api/v1/file/{job_id} | DELETE | Deletes file for a specific job | Internal-only |
| /internal/storage/write-masked | POST | Accepts masked files from Masking Service and stores them in staging | Internal-only |
| /internal/storage/read | GET | Streams file content for NLP, Masking, and Validation services | Internal-only |
*Table 117.* 
These interfaces ensure that file movement and retrieval are restricted to controlled internal operations, maintaining the same security principles outlined in the system architecture section.
**7.5.3 Required Interfaces**
The Storage Component depends on external services to maintain metadata consistency, support object storage operations, and publish audit events. These dependencies align with the architectural cohesion, where services interact through RabbitMQ and shared metadata layers.
External Dependencies Required by Storage

| **Dependency** | **Purpose** |
|:-:|:-:|
| MinIO | Storage of physical dataset files across lifecycle phases |
| PostgreSQL | Tracking job metadata, file paths, timestamps, and validation results |
| RabbitMQ | Receiving transition commands and publishing audit messages |
| Audit Service | Persisting cryptographically chained audit logs |
*Table 118.* 
**7.5.4 Internal Architecture**
Internally, the Storage Component consists of several modules that collectively manage intake, transitions, metadata, and retention behaviors. Each module is designed to encapsulate its own logic, ensuring reliability and making the system easier to maintain.
Internal Modules of the Storage Component

| **Module** | **Description** |
|:-:|:-:|
| Intake Validator | Performs file structure, format, size, and safety validation before processing |
| Phase Transition Manager | Handles atomic directory transitions between lifecycle phases |
| Metadata Synchronizer | Updates PostgreSQL job metadata after file operations |
| Retention & Cleanup Engine | Applies retention rules and performs scheduled cleanup of outdated phases |
*Table 119.* 
This modular structure supports the internal organization required for predictable and auditable file management.
**7.5.5 Internal Data Structures**
The Storage Component maintains datasets and supplementary metadata files in a structured, phase-based directory hierarchy.
* **Directory Layout**

⠀sadn-bucket/
   intake/{job_id}/
   staging/{job_id}/
   quarantine/{job_id}/
   safe/{job_id}/
   archive/{job_id}/
* **Metadata Files**

⠀Each job directory maintains structured metadata files that record critical information used in later phases.
Metadata Files Within Job Directories

| **File** | **Description** |
|:-:|:-:|
| metadata.json | Contains dataset attributes, job-level metadata, and storage details |
| audit_trail.json | Records storage-related audit events and transitions |
| privacy_metrics.json | Stores computed privacy metrics from validation |
| masking_policy.json | Captures masking configurations applied by Masking Service |
| error.json | Documents validation or processing errors for quarantined jobs |
*Table 120.* 
**Multi-File Job Structure**
The Storage Component supports multi-file jobs containing related artifacts processed as a coherent unit:
| **File Type** | **Description** |
|:-:|:-:|
| dataset.csv | Primary data file |
| dictionary.json | Column definitions and metadata |
| schema.json | Data structure specification |
Directory Layout for Multi-File Jobs:
staging/{job_id}/
  ├── original/
  │   ├── dataset.csv
  │   ├── dictionary.json
  │   └── schema.json
  └── masked/
      └── dataset.csv
**7.5.6 Processing Logic**
The internal processing logic aligns with the overall system flow but focuses only on operations performed within this component. The table below summarizes the main processing stages performed by Storage.
Internal Processing Workflow
| **Stage** | **Description** |
|:-:|:-:|
| File Intake | Accept file from Orchestrator and store under intake directory |
| Intake Validation | Validate structure, size, format, and integrity of uploaded file |
| Promotion to Staging | Move file to staging after validation and update metadata |
| Masked Output Handling | Accept and store masked file variants from Masking Service |
| Approval Transition | Move masked file to safe or quarantine based on approval decision |
| Archival Transition | Compress and store approved masked files in archive after retention period |
| Controlled Rollback | Revert file to earlier phase when triggered by Orchestrator (safe/ → staging/ for re-processing) |
*Table 121.* 

**7.5.7 Error Handling**
The Storage Component applies a structured error-handling strategy to ensure that failures do not compromise file consistency or system behavior.
Storage Error Response Strategy
| **Error Type** | **Response** |
|:-:|:-:|
| Validation Failure | Move file to quarantine and create error metadata |
| Transition Failure | Send failure to DLQ, update metadata, and log audit event |
| Missing File | Update metadata and generate audit notice |
| I/O Errors | Retry operation; escalate to DLQ if persistent |
| Internal Exceptions | Stop processing, record metadata, emit audit event |
| Rollback Request | Revert phase transition to previous state upon Orchestrator trigger |
*Table 122.* 
**7.5.8 Security Considerations**
To maintain compliance and prevent unauthorized access, the Storage Component applies a set of security controls designed to protect sensitive dataset content throughout all storage operations.
Security Controls in Storage
| **Security Area** | **Implementation** |
|:-:|:-:|
| Data-at-Rest Encryption | AES-256-GCM applied across all stored content |
| Data-in-Transit Encryption | TLS 1.3 used for all internal endpoints |
| Access Restriction | All endpoints limited to internal network scope |
| File Separation | Original and masked datasets managed separately |
| Retention Rules | Automated cleanup to comply with regulatory timelines |
*Table 123.* 

**7.5.9 Performance Considerations**
The Storage Component is optimized for large dataset handling and efficient I/O operations.
Performance Characteristics
| **Area** | **Approach** |
|:-:|:-:|
| File Movement | Atomic renames prevent costly file copying |
| Streamed Reads | Supports large file streaming without memory overload |
| Asynchronous Operations | RabbitMQ ensures non-blocking transitions |
| Background Retention Tasks | Scheduled cleanup avoids runtime bottlenecks |
*Table 124.* 
**Storage Capacity Monitoring**
The Storage Service exposes disk utilization metrics via Prometheus:
* storage_disk_usage_percent - Current disk utilization
* storage_disk_free_bytes - Available disk space

⠀Alert threshold: Operations are rejected when disk usage exceeds 90%.
**7.5.10 Component Dependencies**
The following libraries and SDKs are used to implement the Storage Component’s internal behavior.
Software Dependencies
| **Dependency** | **Purpose** |
|---|---|
| MinIO SDK | Object storage read/write and transition operations |
| PostgreSQL Driver | Metadata synchronization and updates |
| RabbitMQ Client | Handling queue-based transition commands |
| Encryption Utilities | AES-256 and hash functions for secure operations |
*Table 125.* 

**7.5.11 Design Rationale**
The design of the Storage Component follows principles that maximize system reliability, minimize complexity, and ensure regulatory compliance.
Key Design Rationale
| **Design Decision** | **Justification** |
|:-:|:-:|
| Atomic Transitions | Guarantees consistency and avoids partial states |
| Internal-Only Endpoints | Reduces risk of data exposure |
| Metadata Files | Enhances auditability and traceability |
| Directory-Based Phases | Simplifies retention enforcement |
| Modular Architecture | Improves maintainability and service clarity |
*Table 126.* 

### 7.6 Audit Component
**7.6.1** Component Overview
The Audit Service is a dedicated compliance and integrity subsystem responsible for capturing, chaining, and preserving all operational events generated throughout the SADN anonymization pipeline. Acting as the system-wide forensic backbone, it ensures that every transformation, decision, and file movement is verifiable, immutable, and traceable under PDPL, NDMO, and MOH regulatory guidelines.
The Audit Service operates as a standalone microservice implemented with an event-driven architecture. It consumes structured audit events from all other SADN components through the audit_queue and persists them in a cryptographically–secured, append-only audit log stored in PostgreSQL. Each event is chained using SHA-256 hashing, creating an integrity-preserving sequence where any modification becomes immediately detectable.
The architectural role of the Audit Service is documented in Section 5.3.8, where it is positioned as a parallel, non-blocking observer of pipeline activity. Unlike validation, masking, or storage operations, the Audit Service does not influence job behavior directly; instead, it provides authoritative compliance evidence, lifecycle reconstruction capabilities, and forensic visibility required for internal audits, external assessments, and incident investigations.
This component specification includes the audit event model, hash-chaining procedures, tunable parameters , interface definitions, and security controls applied to maintain strict integrity guarantees. As with other components in Section 7, the design includes pseudocode for core logging and chaining algorithms to ensure determinism, correctness, and reproducibility across implementations.
**7.6.1.1** Component Diagram
**7.6.2** Audit Event Model
The Audit Event Model defines the canonical structure used to represent all audit records generated across the SADN pipeline. It establishes a unified schema that ensures consistency, verifiability, and compatibility between all producing microservices (Orchestrator, Storage, Masking, Validation, NLP, and Federation Gateway).
Each audit event is encapsulated in a structured envelope containing core identifiers, metadata describing the action, and fields required for cryptographic integrity protection. The model ensures that events from heterogeneous services can be validated, chained together, and stored in an append-only format within PostgreSQL.
The Audit Event Model includes:
* **Event Identification Fields**  Unique identifiers allowing events to be traced, correlated, and grouped by job.
* **Source and Classification Metadata**  Fields describing the producing microservice, actor type, event category, and severity level.
* **Payload Section**  A structured metadata object that varies based on event type (e.g., masking summary, validation results, file movement details, user actions, or error information).
* **Integrity Fields**  Cryptographic hashes and sequencing values used by the Audit Service to construct a tamper-evident hash chain across all events.

⠀This model forms the foundation for the **Hash-Chaining Process** described in Section 7.6.2.1 and the **Event Types** classification described in Section 7.6.2.2.
**7.6.2.1 Hash-Chaining Process**
The Audit Service applies a cryptographically linked hash-chaining mechanism to guarantee that every audit event is tamper-evident and that the full audit trail can be verified end-to-end. This mechanism ensures that any modification, removal, or insertion of events becomes detectable during integrity checks.
Each audit entry includes three core integrity fields:
* **previous_hash** – The chain hash of the immediately preceding event.
* **event_payload_hash** – SHA-256 hash of the serialized payload of the current event.
* **chain_hash** – A SHA-256 hash computed using both previous_hash and event_payload_hash, forming the actual chain link.

⠀Together, these fields create a sequential hash chain comparable to a simplified blockchain structure.
**Hash Construction Logic**
When a new audit event arrives from the audit_queue, the Audit Service performs the following steps:
1 Retrieve the chain_hash of the most recent audit entry for the same chain (global or job-specific).
2 Serialize the event's payload deterministically and compute its SHA-256 hash.
3 Compute the new chain_hash using the concatenation of:
	* the previous event’s chain_hash
	* the current event’s event_payload_hash
4 Assign an incremented sequence_number to maintain deterministic replay order.
5 Persist the event atomically in the append-only audit_logs table.

⠀This chaining process enforces strict immutability: changing any past event would alter its hash, break all downstream hashes, and invalidate the entire chain.
**Hash-Chaining Pseudocode**
The following pseudocode outlines the deterministic procedure used to generate and append audit events to the chain:
FUNCTION AppendAuditEvent(event):

    // Step 1: Load Previous Chain State
    previous_event ← GetLastAuditEntry()
    IF previous_event EXISTS THEN
        event.previous_hash ← previous_event.chain_hash
        event.sequence_number ← previous_event.sequence_number + 1
    ELSE
        event.previous_hash ← GENESIS_HASH
        event.sequence_number ← 1
    END IF

    // Step 2: Compute Payload Integrity
    serialized_payload ← Serialize(event.payload)
    event.event_payload_hash ← SHA256(serialized_payload)

    // Step 3: Compute Chain Hash
    buffer ← event.previous_hash + event.event_payload_hash
    event.chain_hash ← SHA256(buffer)

    // Step 4: Persist Event Atomically
    InsertIntoAuditLog(event)

END FUNCTION
**Verification Logic**
To verify the entire audit chain, a verification engine can perform:
1 Ensure that each event’s previous_hash matches the computed hash of the event before it.
2 Recompute event_payload_hash from the stored payload.
3 Recompute chain_hash and validate against the stored value.
4 Confirm strict monotonicity of sequence_number.

⠀Any mismatch indicates tampering or corruption, ensuring strong forensic guarantees.
**7.6.2.1 Event Types**
The Audit Service organizes all logged actions into a fixed set of event types to support consistent querying, filtering, and compliance reporting. Each event_type value represents a specific category of behavior within the SADN pipeline and follows a stable naming convention (DOMAIN_ACTION).
The main event type groups are:
**7.6.2.1.1** Job & Orchestrator Events
These events describe high-level job lifecycle and user-facing actions managed by the Orchestrator:
* **JOB_CREATED** – A new anonymization job has been registered.  
* **JOB_STATUS_CHANGED** – Job state transitioned (e.g., PENDING → MASKING).  
* **JOB_CANCELLED** – Job was cancelled by a user or administrator.  
* **USER_APPROVED** – Data Owner approved anonymization results.  
* **USER_REJECTED** – Data Owner rejected anonymization results.  
* **USER_DOWNLOADED_RESULT** – An anonymized dataset or report was downloaded.  

⠀**7.6.2.1.2** Storage & Lifecycle Events
These events capture file movements and lifecycle operations handled by the Storage Service:
* **FILE_UPLOADED** – Initial dataset file accepted into intake/.
* **PHASE_MOVED** – File moved between phases (e.g., intake → staging, staging → safe).
* **FILE_QUARANTINED** – Dataset moved into quarantine/ due to failure or rejection.
* **FILE_ARCHIVED** – Approved masked dataset moved into archive/.
* **RETENTION_CLEANUP_EXECUTED** – Scheduled retention/cleanup job removed expired data.

⠀**7.6.2.1.3** Masking Events
These events summarize anonymization operations performed by the Masking Service:
* **MASKING_STARTED** – Masking process initiated for a job.
* **MASKING_COMPLETED** – Masking finished successfully; masked output produced.
* **MASKING_PARTIAL** – Masking completed with warnings (non-fatal issues).
* **MASKING_FAILED** – Masking process failed and could not produce a valid output.

⠀**7.6.2.1.4** Validation & Privacy Events
These events describe privacy checks and decisions made by the Validation Service:
* **VALIDATION_STARTED** – Privacy metric computation started.
* **VALIDATION_PASSED** – Dataset satisfied configured k, l, t thresholds.
* **VALIDATION_FAILED** – Dataset failed one or more privacy requirements.
* **RISK_SCORE_COMPUTED** – Risk score computed and stored for a job.

⠀**7.6.2.1.5** NLP & Detection Events
These events document NLP operations related to PII/PHI detection:
* **NLP_SCAN_STARTED** – Free-text PII scan initiated.
* **NLP_SCAN_COMPLETED** – Scan completed with aggregated detection counts.
* **NLP_MODEL_VERSION_USED** – Explicit record of model/version used for the job.

⠀**7.6.2.1.6** Federation Events
These events track cross-institutional data sharing via the Federation Gateway:
* **FEDERATION_SHARE_REQUESTED** – Outgoing sharing request created.
* **FEDERATION_SHARE_COMPLETED** – Anonymized dataset successfully shared with a peer node.
* **FEDERATION_SHARE_FAILED** – Sharing attempt failed (e.g., TLS, signature, or policy issues).
* **FEDERATION_REQUEST_RECEIVED** – Incoming request received from a peer node.

⠀**7.6.2.1.7** Error, DLQ & Security Events
These events capture exceptional and security-relevant conditions across the pipeline:
* **ERROR_OCCURRED** – Generic component error with categorized error_code.
* **DLQ_REDIRECTED** – Message routed to a Dead Letter Queue after repeated failures.
* **SECURITY_EVENT** – Security-relevant incident (e.g., invalid token, unauthorized access attempt).
* **CONFIG_CHANGE_APPLIED** – Sensitive configuration or policy change (e.g., new masking policy, updated thresholds).

⠀Each event type is mapped to a structured payload schema within the Audit Event Model (Section 7.6.2) and is stored with a clearly defined severity level, enabling fine-grained filtering for operational monitoring, compliance audits, and forensic investigations.
**7.6.3 Tunable Parameters**
The Audit Service exposes a set of configurable parameters that control how events are chained, stored, and retained. These parameters allow institutions to adapt audit behavior to their compliance requirements, performance constraints, and operational environments. All tunable parameters are loaded from environment variables or configuration files at startup to ensure deterministic behavior and easy deployment across nodes.
The parameters fall into four main categories: **hashing behavior**, **retention and cleanup**, **batching/performance**, and **message ingestion controls**.
* Hashing & Integrity Parameters

⠀**Parameter** **Default** | **Range** | **Description** |
|:-:|:-:|:-:|:-:|
| **CHAIN_HASH_ALGORITHM** | SHA-256 | SHA-256 / SHA-512 | Hash algorithm used to compute the chain link (chain_hash). |
| **GENESIS_HASH** | Fixed 64-hex seed | Any 32–128 hex chars | The initial hash used when no previous event exists. |
| **PAYLOAD_SERIALIZATION_MODE** | canonical-json | canonical-json / compact-json | Controls deterministic serialization for event_payload_hash. |
*Table 127.* 

* Retention & Cleanup Parameters

⠀**Parameter** **Default** | **Range** | **Description** |
|:-:|:-:|:-:|:-:|
| **AUDIT_RETENTION_DAYS** | 2555 (7 years) | 1–3650 | Maximum retention period before cleanup tasks archive or purge audit logs. |
| **CLEANUP_INTERVAL_HOURS** | 24 | 1–168 | How frequently the retention engine scans for expired audit entries. |
| **ARCHIVE_ENABLED** | true | true / false | Determines whether old audit entries are moved to an archive table instead of deletion. |
*Table 128.* 

* Performance & Batching Parameters

⠀**Parameter** **Default** | **Range** | **Description** |
|:-:|:-:|:-:|:-:|
| **BATCH_INSERT_SIZE** | 1 | 1–500 | Number of audit events appended to the database in a single transaction. |
| **MAX_QUEUE_PREFETCH** | 50 | 1–1000 | Number of messages pre-fetched from audit_queue for faster ingestion. |
| **DB_WRITE_TIMEOUT_MS** | 5000 | 1000–30000 | Maximum allowed write time before retry or failure. |
*Table 129.* 

* Message Ingestion & Reliability Parameters

⠀**Parameter** **Default** | **Range** | **Description** |
|:-:|:-:|:-:|:-:|
| **RETRY_MAX_ATTEMPTS** | 5 | 1–20 | Number of retry attempts for transient write failures. |
| **RETRY_BACKOFF_MULTIPLIER** | 2.0 | 1.2–3.0 | Exponential backoff applied between retries. |
| **DLQ_REDIRECT_THRESHOLD** | 3 | 1–10 | Number of repeated failures before redirecting the event to audit_dlq. |
*Table 130.* 

* Validation & Verification Parameters

⠀
| **Parameter** | **Default** | **Range** | **Description** |
|:-:|:-:|:-:|:-:|
| **CHAIN_VERIFICATION_ON_STARTUP** | true | true / false | Whether the Audit Service verifies the integrity of the entire chain at startup. |
| **VERIFICATION_BATCH_SIZE** | 1000 | 100–10000 | Controls how many events are verified per iteration during integrity scans. |
| **INTEGRITY_ALERT_THRESHOLD** | 1 | 1–100 | Number of detected hash mismatches allowed before triggering a security alert. |
*Table 131.* 

**7.6.4 Security Considerations**
The Audit Service implements strict security controls to ensure the confidentiality, integrity, and compliance readiness of all recorded events. Because the audit log functions as the authoritative forensic record for the entire SADN pipeline, this component applies hardened mechanisms to prevent tampering, unauthorized access, or leakage of sensitive operational details. The following subsections describe the integrity controls and sensitive metadata protections applied within the Audit Service.
**7.6.4.1 Integrity Controls**
The Audit Service applies multiple layers of integrity protections to ensure that every recorded event remains tamper-evident, verifiable, and resistant to unauthorized modification. These controls preserve the legal and forensic reliability of the audit trail under PDPL, NDMO, and MOH IS0303 compliance standards.
**7.6.4.1.1 Cryptographic Hash Chaining**
* Every audit event includes:
  * previous_hash
  * event_payload_hash
  * chain_hash
* The Audit Service computes a new chain_hash using SHA-256 over the concatenation of the current event payload and the previous event’s hash.
* Any change to a past event breaks all downstream hashes, making tampering immediately detectable.

⠀**7.6.4.1.2 Append-Only Persistence Model**
* The audit_logs table is configured as **append-only**, enforcing:  
  * No updates
  * No deletions
  * No overwrites
* Database roles are separated such that the Audit Service is the only component allowed to write new events, and no component has permission to modify existing records.

⠀**7.6.4.1.3 Atomic Event Insertion**
* Each audit entry is written in a single ACID transaction, ensuring that:  
  * A chain update cannot partially complete.
  * No event is recorded with missing integrity fields.
  * Sequence numbers cannot become inconsistent.

⠀**7.6.4.1.4 Deterministic Payload Serialization**
* All event payloads are serialized using **canonical JSON**, ensuring:  
  * Consistent hash results across environments
  * Accurate verification during integrity scans
  * Elimination of serialization ambiguity (e.g., whitespace or field-order differences)

⠀**7.6.4.1.5 Chain Verification Procedures**
* Optional startup verification replays the entire chain and validates:  
  * event_payload_hash integrity
  * Correct previous_hash linkage
  * Consistent chain_hash recomputation
  * Monotonic ordering of sequence_number
* Failed verification triggers a SECURITY_EVENT audit entry and halts ingestion.

⠀**7.6.4.1.6 Fail-Safe Tamper Detection**
* Any detected mismatch in:  
  * payload hashes
  * chain linkage
  * sequence numbering
  * invalid event structure
* Results in immediate rejection of the event and routing to audit_dlq for investigation.

⠀**7.6.4.1.7 Separation of Chain Contexts**
* Global and per-job chains can be maintained to:
  * Reduce verification load
  * Improve audit granularity
  * Prevent cross-chain contamination

⠀These mechanisms collectively ensure that the audit trail remains a trustworthy, immutable, and verifiable record of all SADN processing activities.
**7.6.4.2 Sensitive Metadata Handling**
The Audit Service is designed to ensure that no personally identifiable information (PII), protected health information (PHI), or sensitive dataset content is ever recorded in the audit trail. Because the audit log serves as a long-term compliance artifact and may be reviewed by auditors, administrators, or external regulatory bodies, strict rules govern what can and cannot appear in audit payloads.
**7.6.4.2.1** Zero-PII Storage Policy
* No raw dataset values, identifiers, or any fields classified as PII/PHI may be included in an audit event.
* Microservices are required to publish **only metadata summaries**, not raw content.
* Allowed examples: counts, flags, anonymized IDs, timestamps.
* Prohibited examples: names, phone numbers, medical details, original text fields.

⠀**7.6.4.2.2** Summarized Masking & Validation Metadata
* Masking events record only **aggregate transformation information**, such as:
  * number of columns suppressed
  * number of rows generalized
  * pseudonymized field count
* Validation events record **metric values** (k, l, t, risk score), not raw attribute distributions.

⠀**7.6.4.2.3** Sanitized Error Information
* Error events avoid including stack traces, internal file paths, or system-level debug messages.
* Instead, they include:
  * an error_code
  * a short classification message
  * a log correlation ID (not the raw trace itself)
* This prevents accidental exposure of sensitive operational data.

⠀**7.6.4.2.4** No Cryptographic Material Logging
To prevent leakage of sensitive security details:
* The audit log never stores salts, keys, encryption materials, or cryptographic parameters used by the Masking or Federation systems.
* References such as key IDs or policy IDs **may** be logged, but the values themselves must not.

⠀**7.6.4.2.5** Controlled Logging of User Actions
* When a user performs an action (approve, reject, download), only:
  * anonymized actor_id
  * logical user type (ADMIN, END_USER)
  * timestamp
* Are logged.
* No usernames, emails, tokens, or identifying credentials are included.

⠀**7.6.4.2.6** NLP and Text Handling Restrictions
* NLP events must record **counts and categories only** (e.g., “Detected 4 PERSON entities”).
* No extracted text, spans, tokens, or sensitive content from the original dataset may appear in audit payloads.

⠀**7.6.4.2.7** Compliance-Driven Payload Filtering
* Prior to persistence, the Audit Service performs schema validation to ensure:
  * No disallowed fields exist
  * No nested PII structures remain
  * All metadata conforms to zero-content-storage rules
* Invalid or non-compliant events are redirected to audit_dlq.

⠀


This handling strategy ensures that the audit system maintains comprehensive traceability **without ever exposing sensitive data**, preserving both privacy and regulatory compliance.
**7.6.5 Audit Trail Structure**
The Audit Service persists all events in a single, append-only audit trail stored in PostgreSQL. This trail is organized to support chronological reconstruction of system activity, efficient filtering by job or event type, and reliable integrity verification.
The audit trail is represented primarily by the audit_logs table, with optional archive tables for long-term retention.
**7.6.5.1** Logical Table Layout
The core audit table stores a normalized envelope plus a JSON payload:
| **Column Name** | **Type** | **Description** |
|:-:|:-:|:-:|
| id | BIGSERIAL (PK) | Internal surrogate key used for physical ordering. |
| event_id | UUID | Globally unique identifier for the audit event. |
| job_id | UUID (nullable) | Identifier of the associated job, if applicable. |
| event_type | VARCHAR | Categorical label of the event (e.g., VALIDATION_PASSED). |
| source_service | VARCHAR | Originating microservice (e.g., storage, masking, audit). |
| actor_type | VARCHAR | Logical actor (SYSTEM_SERVICE, END_USER, ADMIN). |
| actor_id | VARCHAR (nullable) | Anonymized identifier of the user/actor, if present. |
| timestamp | TIMESTAMPTZ | Event creation time in UTC with millisecond precision. |
| severity | VARCHAR | Event importance (INFO, WARNING, ERROR, SECURITY). |
| sequence_number | BIGINT | Monotonic chain position for deterministic replay. |
| previous_hash | VARCHAR | Hash of the preceding event in the chain. |
| event_payload_hash | VARCHAR | Hash of the serialized payload for this event. |
| chain_hash | VARCHAR | Final chain link hash used for integrity verification. |
| payload | JSONB | Structured metadata specific to the event type. |
*Table 132.* 
Archive tables (e.g., audit_logs_archive_YYYY) may mirror this schema for older records moved beyond primary retention windows.
**7.6.5.2** Indexing & Partitioning Strategy
To support efficient queries while maintaining simplicity:
* **Primary Key:**  PRIMARY KEY (id) – ensures fast insertion and deterministic physical ordering.
* **Core Indexes:**
  * INDEX audit_logs_job_id_timestamp (job_id, timestamp) – fast reconstruction of job history.
  * INDEX audit_logs_event_type (event_type) – filter by event type for reports.
  * INDEX audit_logs_timestamp (timestamp) – time-range queries for audits.
* **Optional Partitioning:**  Time-based partitions (e.g., monthly or quarterly) may be used for:
  * faster pruning/archiving of old data
  * smaller index sizes per partition
  * improved query performance for recent time windows

⠀**7.6.5.3** Canonical Event Flow in the Trail
Conceptually, the audit trail maintains a globally ordered record of all events across the system:
**1** **Event Produced** – A microservice publishes a structured event to audit_queue.
**2** **Event Consumed** – The Audit Service reads the message, validates its schema, and enriches it with integrity metadata.
**3** **Chain Update** – sequence_number, previous_hash, event_payload_hash, and chain_hash are computed.
**4** **Persist Entry** – The event is inserted into audit_logs in an atomic transaction.
**5** **(Optional) Archive** – After exceeding AUDIT_RETENTION_DAYS, records are moved to an archive table or exported.

⠀**7.6.5.4** Pseudocode – Writing to the Audit Trail
The following pseudocode illustrates how finalized events are persisted into the audit trail after hash-chaining is applied:
// Assumes AppendAuditEvent(event) has already set sequence_number and hashes

FUNCTION PersistAuditEvent(event):

    BEGIN TRANSACTION

        INSERT INTO audit_logs (
            event_id,
            job_id,
            event_type,
            source_service,
            actor_type,
            actor_id,
            timestamp,
            severity,
            sequence_number,
            previous_hash,
            event_payload_hash,
            chain_hash,
            payload
        ) VALUES (
            event.event_id,
            event.job_id,
            event.event_type,
            event.source_service,
            event.actor_type,
            event.actor_id,
            event.timestamp,
            event.severity,
            event.sequence_number,
            event.previous_hash,
            event.event_payload_hash,
            event.chain_hash,
            event.payload
        );

    COMMIT TRANSACTION

END FUNCTION
**7.6.5.5** Pseudocode – Reconstructing a Job’s Audit Trail
To support investigations and compliance reviews, the Audit Service (or a reporting tool) can load a complete chronological history for a specific job:
FUNCTION GetJobAuditTrail(job_id):

    entries ← QUERY
        SELECT *
        FROM audit_logs
        WHERE job_id = job_id
        ORDER BY timestamp ASC, sequence_number ASC;

    RETURN entries

END FUNCTION

This function is used by internal dashboards or reporting modules to display a human-readable timeline of events for a given job.
**7.6.5.6** Pseudocode – Global Integrity Scan
For periodic verification of the trail’s integrity:
FUNCTION VerifyAuditChain():

    previous_chain_hash ← GENESIS_HASH

    entries ← QUERY
        SELECT sequence_number, previous_hash,
               event_payload_hash, chain_hash, payload
        FROM audit_logs
        ORDER BY sequence_number ASC;

    FOR EACH entry IN entries DO

        serialized_payload ← Serialize(entry.payload)
        recomputed_payload_hash ← SHA256(serialized_payload)

        IF recomputed_payload_hash != entry.event_payload_hash THEN
            RAISE IntegrityViolation("Payload hash mismatch at sequence " + entry.sequence_number)
        END IF

        buffer ← previous_chain_hash + entry.event_payload_hash
        recomputed_chain_hash ← SHA256(buffer)

        IF recomputed_chain_hash != entry.chain_hash THEN
            RAISE IntegrityViolation("Chain hash mismatch at sequence " + entry.sequence_number)
        END IF

        IF entry.previous_hash != previous_chain_hash THEN
            RAISE IntegrityViolation("Previous hash mismatch at sequence " + entry.sequence_number)
        END IF

        previous_chain_hash ← entry.chain_hash

    END FOR

END FUNCTION
This structure and behavior ensure that the audit trail is not only **complete and queryable**, but also **cryptographically verifiable** as a single, coherent history of all SADN operations.
## 7.7 Federation Gateway Component
### 7.7.1 Overview
The Federation Gateway is responsible for enabling secure data sharing between peer Saudi Anonymization and Data Masking Network instances operated by partner institutions. This component implements mutual TLS authentication, Data Use Agreement enforcement, and encrypted dataset transmission to authorized external parties.
The Federation Gateway operates exclusively on datasets that have completed the full anonymization pipeline and reside in the safe storage phase. This architectural constraint ensures that only validated, privacy-compliant data can be transmitted externally. For the capstone deployment, the gateway operates in outbound-only mode-the local SADN instance can transmit datasets to peers but does not accept inbound transfers.
The gateway is implemented in Python using the FastAPI framework, maintaining consistency with other SADN microservices. The architectural position of the Federation Gateway within the processing pipeline is documented in Section 5.3.9.
**7.7.1.1 Component Diagram**

*Figure 11.* 

### Federation Gateway Component Architecture
**7.7.1.2 Two-Process Model**
The Federation Gateway supports two distinct operational processes:

*Figure 12.* 
### Federation Two-Process Model

| **Process** | **Actor** | **Frequency** | **Purpose** |
|:-:|:-:|:-:|:-:|
| Peer Registration | Federation Administrator | One-time per institution | Establish trust via certificate exchange |
| Data Transfer | Data Owner / DPO | Per dataset | Transmit anonymized dataset to registered peer |
*Table 133.* 
Peer Registration is an administrative task involving offline certificate exchange and legal agreement execution. Data Transfer is an operational task initiated by Data Owners to share specific datasets with pre-registered peers.
### 7.7.2 Internal Modules
The Federation Gateway comprises four modules:
| **Module** | **Responsibility** |
|:-:|:-:|
| Certificate Manager | Manages X.509 certificate lifecycle, mTLS handshake execution, revocation checking, and rotation handling |
| Peer Registry | Maintains authorized peer institutions, endpoints, connection status, and periodic health checks |
| DUA Validator | Enforces Data Use Agreement requirements including expiration, permitted categories, and purpose alignment |
| Transfer Handler | Executes secure transmission including packaging, hybrid encryption, mTLS transmission, and acknowledgment verification |
*Table 134.* 
### 7.7.3 Federation Protocol
The Federation Gateway implements a twelve-step protocol for secure dataset transmission.
**7.7.3.1 Protocol Steps**
| **Step** | **Action** | **Responsible Module** |
|:-:|:-:|:-:|
| 1 | Receive share request from Orchestrator | Transfer Handler |
| 2 | Validate job is COMPLETED in safe/ | Transfer Handler |
| 3 | Verify privacy metrics meet thresholds | Transfer Handler |
| 4 | Check active DUA exists for peer | DUA Validator |
| 5 | Retrieve peer endpoint and certificate | Peer Registry |
| 6 | Retrieve dataset from MinIO safe/ | Transfer Handler |
| 7 | Generate dataset hash and digital signature | Transfer Handler |
| 8 | Encrypt dataset with hybrid scheme | Transfer Handler |
| 9 | Package into secure container | Transfer Handler |
| 10 | Establish mTLS connection with peer | Certificate Manager |
| 11 | Transmit to peer federation endpoint | Transfer Handler |
| 12 | Process acknowledgment and log audit | Transfer Handler |
*Table 135.* 

*Figure 13.* 
### Federation Protocol Flow
**7.7.3.2 Protocol Pseudocode**
FUNCTION ExecuteFederationTransfer(jobId, peerId, requestingUserId)

    // Step 1-2: Validate job eligibility
    transferId ← GenerateUUID()
    job ← GetJobFromDatabase(jobId)
    
    IF job.status ≠ "COMPLETED" OR job.storage_phase ≠ "safe" THEN
        RAISE FederationError("Job not eligible for federation")
    END IF
    
    // Step 3: Verify privacy metrics
    metrics ← GetPrivacyMetrics(jobId)
    
    IF metrics.k_anonymity < K_THRESHOLD OR 
       metrics.l_diversity < L_THRESHOLD OR 
       metrics.t_closeness > T_THRESHOLD THEN
        RAISE FederationError("Privacy metrics below federation threshold")
    END IF
    
    // Step 4: Validate DUA
    peer ← GetPeerFromRegistry(peerId)
    dua ← DUAValidator.FindActiveDUA(LOCAL_INSTITUTION, peer.institution_name)
    
    IF dua IS NULL OR dua.expiration_date < NOW() THEN
        RAISE FederationError("No active DUA with peer")
    END IF
    
    // Step 5-6: Retrieve data
    peerEndpoint ← peer.endpoint_url
    datasetBytes ← MinIO.GetObject("safe/" + jobId + "/masked.csv")
    
    // Step 7: Generate hash and signature
    datasetHash ← SHA256(datasetBytes)
    privateKey ← Vault.GetPrivateKey(INSTITUTIONAL_KEY_ID)
    signature ← RSA_PSS_Sign(privateKey, datasetHash)
    
    // Step 8: Hybrid encryption
    sessionKey ← CryptoRandom.GetBytes(32)
    compressedData ← GzipCompress(datasetBytes)
    encryptedDataset ← AES_256_GCM_Encrypt(sessionKey, compressedData)
    encryptedSessionKey ← RSA_OAEP_Encrypt(peer.public_key, sessionKey)
    
    // Step 9: Package container
    container ← {
        encrypted_dataset: Base64Encode(encryptedDataset),
        encrypted_session_key: Base64Encode(encryptedSessionKey),
        digital_signature: Base64Encode(signature),
        dataset_hash: datasetHash,
        metadata: {
            source_institution: LOCAL_INSTITUTION,
            dataset_id: jobId,
            timestamp: NOW(),
            dua_reference: dua.dua_id,
            privacy_metrics: metrics
        }
    }
    
    // Step 10-11: Transmit via mTLS
    tlsContext ← CertificateManager.CreateMTLSContext(peer.certificate_fingerprint)
    response ← HTTP_POST(peerEndpoint + "/api/v1/federation/receive", 
                         container, tlsContext, port: 8443)
    
    // Step 12: Process acknowledgment
    IF response.status_code ≠ 200 OR NOT response.body.signature_valid THEN
        UpdateTransferRecord(transferId, "FAILED")
        RAISE FederationError("Peer rejected transfer")
    END IF
    
    UpdateTransferRecord(transferId, "COMPLETED")
    InsertProvenanceRecord(jobId, peer.institution_name, datasetHash)
    
    PublishToAuditQueue({
        event_type: "FEDERATION_TRANSFER_COMPLETE",
        job_id: jobId,
        transfer_id: transferId,
        peer_institution: peer.institution_name
    })
    
    RETURN {transfer_id: transferId, status: "COMPLETED"}

END FUNCTION

**7.7.3.3 mTLS Handshake**
The gateway uses mutual TLS authentication on port 8443:

*Figure 14.* 
### mTLS Handshake Sequence
**7.7.3.4 Secure Container Format**
{
  "encrypted_dataset": "base64...",
  "encrypted_session_key": "base64...",
  "digital_signature": "base64...",
  "dataset_hash": "sha256:a1b2c3...",
  "metadata": {
    "source_institution": "Al-Habib Medical Group",
    "dataset_id": "uuid",
    "timestamp": "2025-03-15T10:30:45Z",
    "dua_reference": "uuid",
    "privacy_metrics": { "k": 7, "l": 3, "t": 0.15 }
  }
}
### Secure Container Format
*Figure 15.* 
### 7.7.4 Interface Specification
**7.7.4.1 HTTP Input**
**Endpoint:** POST /internal/federation/share/{job_id}
**Request:**
{
  "peer_id": "880e8400-e29b-41d4-a716-446655440003",
  "requesting_user_id": "user-456"
}

**Response (Success):**
{
  "transfer_id": "660e8400-e29b-41d4-a716-446655440001",
  "status": "COMPLETED",
  "peer_institution": "Imam Abdulrahman Bin Faisal University",
  "completed_at": "2025-03-15T10:31:05Z"
}

**Response (Error):**
{
  "error": "DUA_VALIDATION_FAILED",
  "code": "DUA_EXPIRED",
  "message": "DUA with IAU expired on 2025-01-01"
}

**7.7.4.2 Queue Publications**
**Queue:** audit_queue
| **Event Type** | **Trigger** |
|:-:|:-:|
| FEDERATION_TRANSFER_COMPLETE | Peer acknowledged successful receipt |
| FEDERATION_TRANSFER_FAILED | Transfer failed at any stage |
*Table 136.* 
**Message Schema:**
{
  "event_id": "uuid",
  "event_type": "FEDERATION_TRANSFER_COMPLETE",
  "job_id": "uuid",
  "timestamp": "ISO8601",
  "actor_id": "federation-gateway",
  "details": {
    "transfer_id": "uuid",
    "peer_institution": "IAU",
    "dataset_hash": "sha256:...",
    "file_size_bytes": 15728640
  }
}

**7.7.4.3 Peer Acknowledgment Format**
{
  "status": "SUCCESS",
  "received_at": "2025-03-15T10:31:02Z",
  "signature_valid": true,
  "decryption_successful": true
}

### 7.7.5 Data Access
**7.7.5.1 MinIO Operations**
| **Phase** | **Access** | **Purpose** |
|:-:|:-:|:-:|
| safe/ | READ | Retrieve masked.csv for transmission |
*Table 137.* 
**7.7.5.2 PostgreSQL Queries**
**Query: Verify Job Eligibility**
SELECT job_id, status, storage_phase
FROM jobs 
WHERE job_id = @job_id AND status = 'COMPLETED';

**Query: Get Peer Details**
SELECT peer_id, institution_name, endpoint_url, certificate_fingerprint
FROM federation_peers
WHERE peer_id = @peer_id AND authorized = TRUE AND status = 'ACTIVE';

**Query: Validate DUA**
SELECT dua_id, expiration_date, data_categories
FROM data_use_agreements
WHERE sending_institution = @sending AND receiving_institution = @receiving
AND status = 'active' AND expiration_date > NOW();

**Query: Insert Transfer Record**
INSERT INTO federation_transfers 
    (transfer_id, job_id, peer_id, dua_id, status, file_hash, file_size_bytes)
VALUES (@transfer_id, @job_id, @peer_id, @dua_id, 'COMPLETED', @hash, @size);

### 7.7.6 Error Handling
**7.7.6.1 Error Categories**
| **Category** | **Examples** | **Recovery Strategy** |
|:-:|:-:|:-:|
| Validation Error | Job not completed, DUA expired | Reject with detailed error |
| Certificate Error | Expired cert, fingerprint mismatch | Abort, log security event |
| Network Error | Timeout, peer unreachable | Retry with exponential backoff |
| Peer Rejection | Signature invalid, decryption failed | Mark failed, alert admin |
*Table 138.* 
**7.7.6.2 Retry Strategy**
FUNCTION ExecuteWithRetry(operation)
    FOR attempt FROM 1 TO MAX_RETRY_ATTEMPTS DO
        TRY
            RETURN operation()
        CATCH RetryableError AS error
            IF attempt < MAX_RETRY_ATTEMPTS THEN
                delay ← INITIAL_DELAY * (BACKOFF_MULTIPLIER ^ attempt)
                Sleep(delay)
            ELSE
                RAISE error
            END IF
        END TRY
    END FOR
END FUNCTION

| **Parameter** | **Value** |
|:-:|:-:|
| MAX_RETRY_ATTEMPTS | 3 |
| INITIAL_DELAY | 2 seconds |
| BACKOFF_MULTIPLIER | 2.0 |
*Table 139.* 
### 7.7.7 Configuration
**7.7.7.1 Environment Variables**
| **Variable** | **Required** | **Default** | **Description** |
|:-:|:-:|:-:|:-:|
| FEDERATION_PORT | No | 8443 | mTLS port |
| INSTITUTIONAL_CERT_PATH | Yes | - | Path to X.509 certificate |
| INSTITUTIONAL_KEY_PATH | Yes | - | Path to private key |
| VAULT_ENDPOINT | Yes | - | HashiCorp Vault endpoint |
| MINIO_ENDPOINT | Yes | - | MinIO server endpoint |
| POSTGRES_HOST | Yes | - | PostgreSQL hostname |
| RABBITMQ_HOST | Yes | - | RabbitMQ hostname |
*Table 140.* 
**7.7.7.2 Tunable Parameters**
| **Parameter** | **Default** | **Description** |
|:-:|:-:|:-:|
| TRANSFER_TIMEOUT_SECONDS | 300 | Maximum transfer time |
| PEER_HEALTH_CHECK_INTERVAL | 300 | Seconds between health checks |
| FEDERATION_K_THRESHOLD | 5 | Minimum k-anonymity for federation |
| FEDERATION_L_THRESHOLD | 2 | Minimum l-diversity for federation |
| FEDERATION_T_THRESHOLD | 0.2 | Maximum t-closeness for federation |
| DUA_EXPIRY_WARNING_DAYS | 30,14,7 | Notification thresholds |
*Table 141.* 
### 7.7.8 Security Considerations
**7.7.8.1 Cryptographic Standards**
| **Operation** | **Algorithm** | **Key Size** | **Standard** |
|:-:|:-:|:-:|:-:|
| Dataset Encryption | AES-256-GCM | 256 bits | NIST SP 800-38D |
| Key Exchange | RSA-OAEP | 4096 bits | PKCS#1 v2.2 |
| Digital Signature | RSA-PSS | 4096 bits | PKCS#1 v2.2 |
| Hash | SHA-256 | 256 bits | FIPS 180-4 |
| TLS | TLS 1.3 | - | RFC 8446 |
*Table 142.* 
**7.7.8.2 Sensitive Data Handling**
| **Data Type** | **Handling** | **Logging Policy** |
|:-:|:-:|:-:|
| Private keys | Retrieved from Vault, cleared after use | Never logged |
| Session keys | Memory only, single use | Never logged |
| Dataset content | Streamed when possible | Never logged |
| Peer certificates | Cached in memory | Fingerprint only |
*Table 143.* 
**7.7.8.3 Federation Rules**
| **Rule** | **Description** |
|:-:|:-:|
| Outbound only | For capstone, only SEND to peers (no inbound) |
| Only safe/ files | Can only share COMPLETED jobs |
| DUA required | Must have active Data Use Agreement |
| mTLS required | Port 8443 with mutual TLS authentication |
*Table 144.* 



### 7 Detailed System Design

⠀
Most components described in the System Architecture section will require a more detailed discussion. Other lower-level components and subcomponents may need to be described as well. Each subsection of this section will refer to or contain a detailed description of a system software component. The discussion provided should cover the following software component attributes:

### 8.1 Orchestrator Service
**8.1.1 Classification**
The Orchestrator is classified as an independent microservice serving as the API Gateway and Job Coordinator for the SADN platform. It is implemented in Python using the FastAPI framework and operates as a synchronous request handler for external clients while coordinating asynchronously with internal services. Unlike other SADN microservices that consume from message queues, the Orchestrator exposes RESTful HTTP endpoints and acts exclusively as a publisher to the audit queue.
**8.1.2 Definition**
The Orchestrator serves as the sole external entry point for all interactions with the Saudi Anonymization and Data Masking Network. Its primary purpose is to receive dataset submissions from Data Owners, track job progress through the anonymization pipeline, deliver results upon completion, and process user approval decisions that determine whether anonymized datasets are released or quarantined.
The Orchestrator does not perform data transformation, classification, or validation. Instead, it delegates all processing to specialized downstream services while maintaining job state visibility and enforcing access controls. This centralized entry point simplifies security enforcement by providing a single location for authentication, authorization, and request validation.
**8.1.3 Responsibilities**
The Orchestrator is responsible for receiving dataset uploads and creating corresponding job records in the database. Upon receiving an upload, it transfers the file to the Storage Service and publishes an audit event recording the submission.
It provides job status visibility by responding to status queries with current pipeline phase, timestamps, and any error information. Data Owners can monitor their jobs from submission through completion.
The service delivers anonymization results by streaming masked datasets from safe storage to authorized requesters. It also serves validation reports containing privacy metrics and risk scores for Data Owner review.
Processing user decisions is a critical responsibility. When Data Owners approve results, the Orchestrator instructs the Storage Service to transition the masked dataset to safe storage and delete the original. When Data Owners reject results, it triggers quarantine transition instead.
The Orchestrator initiates federation by forwarding share requests to the Federation Gateway when Data Owners wish to transmit approved datasets to peer institutions.
Finally, it publishes audit events for all user-facing actions including job creation, approval, rejection, and download requests, ensuring complete traceability of external interactions.
**8.1.4 Constraints**
The Orchestrator operates under functional constraints that limit its scope. It accepts only supported file formats (CSV, JSON, Parquet, Excel) and enforces a maximum file size of 500 MB per upload. It cannot modify job status during pipeline processing-only downstream services update status as they complete their work.
Security constraints require all requests to include valid authentication tokens. Role-based access control restricts operations based on user roles, with Data Owners limited to their own jobs while DPOs and Administrators have broader visibility. No sensitive data from datasets may appear in logs or error responses.
Architectural constraints define the Orchestrator's communication patterns. It makes synchronous HTTP calls to internal services (Storage, Federation Gateway) but does not consume from any message queue. It publishes only to the audit queue and never directly to processing queues. All file storage operations are delegated to the Storage Service.
Performance constraints include request timeout limits for internal calls and concurrent connection limits based on deployment configuration. The service must remain responsive to client requests even when downstream services experience delays.
**8.1.5 Composition**
The Orchestrator comprises five internal modules that collectively handle request processing and coordination.
The API Controller module exposes all RESTful endpoints, validates request payloads, and formats responses. It implements the seven external endpoints documented in Section ~[5.3.3.2](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.7j55jn6ywfbh)~.
The Job Manager module creates and queries job records in PostgreSQL. It generates unique job identifiers, records initial metadata, and retrieves current state for status queries.
The File Transfer Handler module manages large file uploads by streaming content to the Storage Service via internal HTTP. It handles multipart form data and monitors transfer completion.
The Queue Publisher module publishes audit events to RabbitMQ. It manages connection pooling and ensures reliable delivery of audit messages.
The Authentication Handler module validates JWT tokens, extracts user identity, and enforces role-based access policies for each endpoint.
**8.1.6 Uses/Interactions**
The Orchestrator interacts with the Storage Service through four internal HTTP endpoints: uploading files for intake, triggering approval transitions, triggering rejection transitions, and delegating federation file retrieval. These calls are synchronous and blocking.
It interacts with the Federation Gateway through a single internal endpoint to initiate cross-institutional transfers. The Gateway handles all federation protocol details independently.
For data persistence, the Orchestrator reads and writes job records in PostgreSQL. It creates records on submission, queries them for status requests, and updates error messages on rejection. It does not access tables owned by other services.
MinIO access is limited to reading from the safe storage phase when serving download requests. The Orchestrator streams file content directly to clients without intermediate storage.
RabbitMQ interaction is outbound only. The Orchestrator publishes audit events for job creation, approval, and rejection but does not consume from any queue.
HashiCorp Vault provides database credentials and JWT secrets at startup. The Orchestrator does not store credentials in configuration files.
**8.1.7 Resources**
The Orchestrator requires network connectivity to PostgreSQL for job state management, MinIO for result delivery, RabbitMQ for audit publishing, and internal services for delegation. It must reach the Storage Service and Federation Gateway via HTTP.
Compute requirements are modest compared to processing services. Memory usage scales with concurrent request volume and file streaming buffers. CPU usage is primarily I/O-bound rather than computation-intensive.
The service requires access to the audit queue for publishing events. Unlike processing services, it does not require dedicated input queues or dead letter queue configurations.
**8.1.8 Processing**
Request processing begins with authentication. The Authentication Handler validates the JWT token, extracts the user identity and role, and rejects unauthorized requests before further processing.
For job submissions, the Orchestrator validates the uploaded file, creates a database record with PENDING status, streams the file to the Storage Service, and publishes a JOB_CREATED audit event. If file transfer fails, the job status is updated to FAILED.
Status queries retrieve the current job record and verify the requester has access to view it. The response includes current status, storage phase, and timestamps.
Approval requests verify the job is in AWAITING_APPROVAL status and the requester is the job owner. Upon validation, the Orchestrator calls the Storage Service approval endpoint, which triggers the phase transition to safe storage. A JOB_APPROVED audit event is published.
Rejection requests follow similar validation. The Storage Service rejection endpoint triggers quarantine transition. The rejection reason is recorded in the job record, and a JOB_REJECTED audit event is published.
Download requests verify the job is COMPLETED and the requester has download authorization. The Orchestrator streams the masked file from MinIO safe storage to the client.
Federation requests verify completion status and federation authorization before delegating to the Federation Gateway.
Complete processing logic and pseudocode are documented in Section ~[7.1](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.3cu3n7c3mwep)~.
**8.1.9 Interface/Exports**
The Orchestrator exports seven RESTful endpoints for external consumption: job submission, status query, result download, validation report retrieval, approval, rejection, and federation initiation. Each endpoint enforces role-based authorization as specified in Section ~[5.3.3.2](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.7j55jn6ywfbh)~.
Internal communication occurs through HTTP calls to the Storage Service and Federation Gateway. The Orchestrator does not expose internal endpoints-it only consumes them from other services.
Audit events are published to the audit queue for three event types: JOB_CREATED when submissions are accepted, JOB_APPROVED when Data Owners approve results, and JOB_REJECTED when Data Owners reject results.
Database operations include INSERT for job creation, SELECT for status queries, and UPDATE for recording rejection reasons. The Orchestrator owns the jobs table but respects that downstream services update status during processing.
Interface specifications and message formats are detailed in Section ~[7.1.5](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.l8ftniq75bvu)~.
### 8.2 NLP Detailed System Design
 **8.2.1 Classification**
The NLP Component is classified as a **core subsystem** within the anonymization pipeline. It is a composite processing module consisting of several internal engines, including:
* Text Normalization Engine
* Language Detection Module
* Tokenization Engine
* Pattern Matching Engine
* Statistical Entity Classifier (ML)
* Evidence Fusion Engine
* PII Aggregation and Map Builder
* Audit Logging Submodule

⠀This subsystem operates as a **non-user-facing processing module**, invoked exclusively by the Orchestration and Intake layers, and provides structured privacy intelligence to downstream components.
 **8.2.2 Definition**
The NLP Component is responsible for **identifying, classifying, and contextualizing personally identifiable information (PII)** across structured and unstructured dataset fields. The component translates raw values into standardized representations and determines which attributes constitute identifiers, quasi-identifiers, or sensitive attributes.
This subsystem aligns directly with requirements specified in the SRS:
* **REQ-NLP-01:** Detect PII across multiple languages (Arabic, English).
* **REQ-NLP-02:** Support deterministic and statistical detection methods.
* **REQ-NLP-03:** Produce structured PII Maps for downstream masking.
* **REQ-NLP-04:** Provide audit logs for all detection events.
* **REQ-NLP-05:** Handle malformed, corrupted, or adversarial input text safely.

⠀The NLP Component is semantically defined as the **privacy intelligence engine** of the SADN platform.
**8.2.3 Responsibilities**
The responsibilities of the NLP Component span detection, classification, contextualization, and reporting. These include:
**Detection Responsibilities**
* Identify direct identifiers using deterministic patterns (e.g., email, phone number, national ID).
* Detect unstructured entities using machine-learning models (names, diagnoses, locations).
* Assign confidence scores for each detection.

⠀**Classification Responsibilities**
* Label each column as:  **identifier**, **quasi-identifier**, **sensitive attribute**, or **non-sensitive**.
* Derive classification decisions using fused evidence from patterns, ML, statistical metrics, and heuristics.

⠀**Integration Responsibilities**
* Provide PII Map outputs to the Masking Service.
* Supply summaries to the Validation Component for privacy rule verification (k, l, t).
* Forward detection records to the Audit Component.
* Report processing metadata to the Orchestrator.

⠀**Governance & Audit Responsibilities**
* Emit hash-chained audit events documenting all NLP outcomes.
* Record model version, pattern pack ID, and detection rationale for transparency.
* Support reproducibility of past anonymization jobs.

⠀**8.2.4 Constraints**
The NLP Component operates under several architectural, computational, and security constraints:
* Timing Constraints:  Must complete processing of large datasets (1M+ rows) within bounded execution windows.
* State Constraints:  No storing of raw PII, no disk persistence of unmasked data.  Only metadata and hashed values may be externalized.
* Input Constraints:  Input must conform to UTF-8; non-UTF-8 sequences are corrected or quarantined.  Very long tokens (>512 chars) are truncated with warnings.
* Output Constraints:  The component must always return a complete PII Map, even under degraded ML functionality.
* Synchronization Constraints:  Parallel execution must avoid race conditions on shared ML model resources.
* Security Constraints:  Forbidden to expose raw or normalized PII to any component except the Masking Service.
* Exception Constraints:  All failures must be exception-safe and logged without terminating the pipeline.
* Streaming-based NLP processing is considered a future extension and is not within the scope of the current detailed system design.
* The present architecture assumes batch-oriented dataset processing.

⠀**8.2.5 Composition**
The NLP Component is composed of the following internal subcomponents, each contributing to a specific function:
* Preprocessing Engine:  Unicode normalization, language detection, tokenization.
* Pattern Engine:  Regex-based detection for structured identifiers.
* Statistical Classifier (ML):  NER model for free-text fields.
* Heuristic Analyzer:  Detects quasi-identifiers using statistical patterns (entropy, uniqueness).
* Evidence Fusion Engine:  Consolidates regex, ML, and heuristics into unified classification.
* PII Map Builder:  Produces the final PII Map consumed by downstream services.
* Audit Logging Submodule:  Hash-linked record generator for compliance.

⠀Each subcomponent operates independently but contributes to a shared internal state.
**8.2.6 Uses / Interactions**
The NLP Component interacts with the system as follows:
Uses
* Intake Layer: Provides raw dataset values and metadata.
* ML Model Repository: Supplies pre-trained detection models.
* Pattern Pack Registry: Provides updated regex definitions.
* Orchestration Layer: Initiates execution and passes configuration.

⠀Used By
* Masking Service: Consumes PII Map for field-level transformations.
* Validation Component: Uses NLP outputs to compute anonymity metrics.
* Audit Component: Receives detection events for compliance tracking.
* Federation Gateway: Indirectly depends on validated outputs.

⠀Interactions occur over secure internal channels and are mediated by REST/gRPC calls.
**8.2.7 Resources**
The NLP Component manages several resource types:
* CPU Resources:  Used extensively for regex processing and ML inference.  Internal worker pools are load-balanced to prevent starvation.
* Memory Resources:  Temporary storage for normalized tokens, pattern matches, and ML inference buffers.  Memory is explicitly cleared after each batch.
* Model Resources:  Loaded ML models (Arabic NER, English NER) stored in memory.  Shared read-only configuration ensures race-free usage.
* Audit Logging Resources:  Requires communication with the Audit Trail subsystem.  Hashing demands cryptographic CPU operations.
* Concurrency Considerations:  Thread-safe queues prevent deadlocks during parallel execution.

⠀**8.2.8 Processing**
The NLP Component processes data through a deterministic 8-stage workflow:
* Stage 1: Normalization (NFC → UTF-8)  Repair encoding, remove anomalies, standardize formats.
* Stage 2: Tokenization & Language Detection  Generate tokens, infer language, and apply appropriate analyzers.
* Stage 3: Pattern Execution  Apply deterministic rules for structured PII.
* Stage 4: ML-Based Entity Detection  Run NER for unstructured text (names, diagnoses).
* Stage 5: Statistical & Heuristic Analysis  Compute uniqueness, entropy, and quasi-identifier likelihood.
* Stage 6: Evidence Fusion  Combine regex, ML, heuristics into unified label per column.
* Stage 7: PII Map Construction  Generate final classification output for all columns.
* Stage 8: Output & Audit Logging  Produce PII Map, emit audit events, and notify downstream components.

⠀The component is exception-safe; any failure in ML triggers fallback strategies.
 **8.2.9 Interface / Exports**
The NLP Component exports structured outputs through internal APIs:
* Export 1: PII Map  Comprehensive classification of all dataset fields.
* Export 2: Detection Events  List of PatternMatch and NEREntity records.
* Export 3: Processing Metadata  Timing, errors, anomalies, languages detected.
* Export 4: Audit Records  Hashed entries ensuring integrity and traceability.
* Export 5: Error Reports  Structured objects for DLQ routing and failure analysis.
* All NLP exports are metadata-only artifacts. Raw or normalized PII values are never exposed through component interfaces or externalized outside secure memory boundaries.

⠀These exports follow strict formatting rules and version-controlled schemas.
**8.2.10 Detailed Subsystem Design**
The NLP subsystem is designed as a multi-stage processing architecture.  Key design elements include:
* Pipelines:  Each dataset column flows through multiple specialized submodules.
* Dataflow Model:  NormalizedCell → PatternMatch / NEREntity → Evidence Fusion → ColumnSummary → PIIMap
* Parallel Execution:  Column-level parallelism maximizes throughput.
* Model Isolation:  Arabic and English NER models operate in separate inference paths.
* Audit Integration:  Every detection event generates a hash-linked AuditRecord.
* Failure Handling:  Fallback algorithms ensure pipeline completion.

⠀A full subsystem diagram may be referenced in Section 5 (System Architecture).
### 8.3 Masking Service
**8.3.1 Classification**
The Masking Service is an independent microservice implemented in C# using the .NET 8 runtime. It operates as a stateless, event-driven worker within the Data Transformation Subsystem, consuming transformation requests from RabbitMQ and applying privacy-preserving modifications to datasets.
**8.3.2 Definition**
The Masking Service transforms sensitive datasets into anonymized outputs by applying five transformation techniques: suppression, generalization, pseudonymization, date shifting, and NLP-based text redaction. It serves as the core anonymization engine of the SADN pipeline, ensuring that all personal identifiers are removed or obscured before privacy validation occurs.
**8.3.3 Responsibilities**
The Masking Service receives classification configurations from the Validation Service and applies the specified transformation to each column. It retrieves the original dataset from staging storage, executes all transformations in a strict sequence, and delivers the masked output to the Storage Service. Upon completion, it triggers privacy validation and emits audit events for compliance tracking. The service must ensure transformation consistency, meaning identical input values produce identical outputs within the same job.
**8.3.4 Constraints**
The service operates under several constraints. It processes only datasets that have passed intake validation and requires complete classification configurations. Processing must complete within 30 minutes for files up to 500 MB. Security constraints prohibit logging raw PII values, and pseudonymization salts must be stored exclusively in HashiCorp Vault. Architecturally, the service communicates only through message queues and internal HTTP endpoints, never making synchronous calls to other services.
**8.3.5 Composition**
Internally, the service comprises a Queue Consumer module for message handling, a Transformation Engine that orchestrates execution order, and five transformation modules: Suppressor, Generalizer, Pseudonymizer, Date Shifter, and Text Redactor. Each module encapsulates a single transformation technique, enabling independent testing and maintenance. The algorithmic details for each module are specified in Section ~[7.3.2](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.pq6rkhwzms2m)~.
**8.3.6 Uses/Interactions**
The Masking Service consumes messages from masking_queue and reads original datasets from MinIO staging storage. It retrieves NLP annotations and classification results from PostgreSQL. After transformation, it sends the masked file to the Storage Service via internal HTTP and publishes messages to validation_queue and audit_queue. The service retrieves credentials and pseudonymization salts from HashiCorp Vault. It has no direct interaction with the Orchestrator, NLP Service, or end users.
**8.3.7 Resources**
The service requires access to RabbitMQ for queue operations, MinIO for dataset retrieval, PostgreSQL for metadata operations, and Vault for secret management. Compute requirements include sufficient memory to load datasets (4-8 GB recommended) and multi-core CPU for efficient processing. Network connectivity to the Storage Service internal endpoint is required for masked file delivery.
**8.3.8 Processing**
The processing workflow begins with message consumption and validation, followed by dataset loading from MinIO. Transformations execute in strict order: suppression first to reduce scope, then date shifting, generalization, pseudonymization, and finally text redaction. The masked dataset is sent to the Storage Service, and upon confirmation, validation is triggered and audit events are published. Error handling includes retry logic with exponential backoff for transient failures and dead letter queue routing for unrecoverable errors. Complete processing logic and pseudocode are documented in Section ~[7.3](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.bit4obaxxyww)~.
**8.3.9 Interface/Exports**
The service consumes transformation requests from masking_queue containing job identifiers, file paths, and per-column classification configurations. It exports masked datasets to the Storage Service via HTTP and publishes validation trigger messages and audit events to their respective queues. Database operations include reading annotations and writing masking results. Interface specifications and message schemas are detailed in Section ~[7.3.3](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.fq49ch8jtedw)~.
### 8.4 Validation Service
**8.4.1 Classification** 
The Validation Service is classified as:
| **Category** | **Description** |
|---|---|
| **Component Type** | Microservice (stateless, event-driven worker) |
| **Subsystem** | Privacy Assurance Subsystem |
| **Execution Model** | Asynchronous consumer of RabbitMQ (validation_queue) |
| **Operational Role** | Privacy Compliance Engine & Gatekeeper |
| **Tech Stack** | Python 3.11 (FastAPI Worker) / Pandas / SciPy / PostgreSQL / MinIO-S3 |
*Table 145.* 
Validation Service Classification
This service is **security-critical** and enforces all privacy validation guarantees before any dataset becomes eligible for release.
**8.4.2 Definition** 
The Validation Service ensures that **masked datasets** produced by the Masking Service comply with the mandatory privacy metrics required by:
* PDPL (Saudi Personal Data Protection Law)
* NDMO National Data Governance Regulations
* NCA Essential Cybersecurity Controls (ECC-2)
* MOH IS0303 (Health Data Security)

⠀Its primary purpose is to:
**1** **Evaluate the anonymization correctness and strength**
**2** **Calculate privacy metrics (k-anonymity, l-diversity, t-closeness)**
**3** **Generate an objective privacy risk score**
**4** **Decide PASS / FAIL** for dataset release
**5** **Instruct the Storage Service** to place the dataset in *safe* or *quarantine*
**6** **Record an immutable audit trail**

⠀It acts as the **final privacy checkpoint** before dataset exposure to researchers or federation partners.
**8.4.3Responsibilities**
The Validation Service SHALL:
**R1 : Load Masked Dataset and Metadata**
* Retrieve masked dataset from staging/ on MinIO
* Load quasi-identifiers, sensitive attributes, masking policy, and metadata from PostgreSQL

⠀**R2 : Compute Privacy Metrics**
* **k-Anonymity**: Identify minimum group sizes
* **l-Diversity**: Identify sensitive attribute richness
* **t-Closeness**: Compare distribution to global dataset

⠀**R3 : Evaluate Policy Thresholds**
Compare computed metrics against:
* System default thresholds
* Institution-specific thresholds
* Dataset category thresholds (healthcare, education)

⠀**R4 : Compute Privacy Risk Score**
Generate a normalized 0–100 risk score using weighted model:
* Low k → high risk
* Low l → high risk
* High t → high risk

⠀**R5 : Determine Final Status**
* PASS → Dataset safe to release
* FAIL → Dataset quarantined
* WARNING → Edge case requiring manual review

⠀**R6 : Generate Validation Report**
Include:
* Metrics
* Risk score
* Thresholds
* Decision
* Failure reasons
* Processing duration

⠀Stored in PostgreSQL and optionally in MinIO.
**R7 : Emit System Events**
* Publish result event to storage_queue
* Publish audit event to audit_queue

⠀**R8 : Maintain Integrity**
Never modify dataset contents.  Never access raw (unmasked) files.
**8.4.4 Constraints**
 **1. Functional Constraints**
* Validation only works on **masked datasets**
* Quasi-identifiers and sensitive attributes must be known
* Dataset must be readable and structurally valid
* All thresholds come from active masking policy

⠀**2. Security Constraints**
* No output logs contain raw or sensitive data
* Only masked dataset is processed
* All interactions must use mTLS/TLS 1.3
* All keys retrieved from Vault

⠀**3. Architectural Constraints**
* No synchronous calls; event-driven only
* No direct calls to Masking, NLP, or Orchestrator
* File access restricted to MinIO
* State stored exclusively in PostgreSQL

⠀**4. Performance Constraints**
* Maximum dataset size: **100MB**
* Maximum processing time: **≤ 35 seconds**
* Must remain stateless to allow horizontal scaling

⠀**5. Compliance Constraints**
Must satisfy:
* PDPL Articles: Data Minimization, Lawful Use, Security Controls
* NDMO: Data Sharing & Privacy Standards
* NCA ECC-2: Logging, Access Control, Encryption
* MOH IS0303: Handling of PHI

⠀**8.4.5** **. Composition**
The service is composed of the following internal modules:
| **Module** | **Purpose** |
|---|---|
| **Queue Consumer** | Receives validation jobs from RabbitMQ |
| **Metadata Loader** | Loads thresholds, QIs, SAs, job metadata |
| **Dataset Reader** | Reads masked dataset from MinIO |
| **k-Anonymity Engine** | Computes equivalence class sizes |
| **l-Diversity Engine** | Computes diversity of sensitive attributes |
| **t-Closeness Engine** | Computes distribution distance (EMD) |
| **Risk Scoring Module** | Normalizes privacy metrics |
| **Decision Engine** | Determines PASS/FAIL/WARNING |
| **Report Generator** | Writes validation results to DB + file |
| **Audit Logger** | Generates audit-chain events |
| **Publisher** | Sends instructions to Storage Service |
*Table 146.* 
                                            Composition Internal Module
The design is fully modular to isolate privacy computation from storage, orchestration, and audit logic.
**8.4.6 Interactions**

| **Service** | **Interaction Type** | **Purpose** |
|---|---|---|
| **Orchestrator** | Indirect / via queue | Receives validation request |
| **Masking Service** | No direct interaction | Only uses masked output |
| **Storage Service** | Outbound queue event | Move dataset to safe/quarantine |
| **MinIO** | S3 File Read | Load masked dataset |
| **PostgreSQL** | Read/Write | Load metadata + save validation results |
| **Audit Service** | Outbound message | Log validation outcomes |
| **Vault** | Secret fetch | DB creds, MinIO creds |
*Table 147.* 
Validation Interactions
The subsystem is fully decoupled and adheres to SADN’s event-driven choreography.
**8.4.7 Resources**
**CPU / Memory**
* Multi-threaded calculation for grouping and distribution
* Optimized for Pandas/SciPy operations

⠀**Network**
* S3 traffic for dataset retrieval
* DB calls for result persistence

⠀**Storage**
* Temporary in-memory buffers only
* Optional report storage in MinIO

⠀**Queues**
* validation_queue
* storage_queue
* audit_queue

⠀All resources are isolated within the SADN runtime environment.
**8.4.8 Processing Logic**
**Step 1 : Job Initialization**
* Read job metadata
* Retrieve masked dataset from MinIO
* Prepare dataset (type normalization, missing value resolution)

⠀**Step 2 : k-Anonymity**
* Group dataset by quasi-identifiers
* Compute minimum group size
* Compare to threshold (e.g., k ≥ 5)

⠀**Step 3 : l-Diversity**
* For each group, compute distinct sensitive values
* Ensure diversity ≥ threshold (e.g., l ≥ 2)

⠀**Step 4 : t-Closeness**
* Compute global distribution
* Compute group distribution
* Compute EMD distance
* Ensure t ≤ threshold (e.g., 0.1)

⠀**Step 5 : Risk Score**
Weighted formula (experts model):
kScore = (k_threshold / k_actual) * 100
lScore = (l_threshold / l_actual) * 100
tScore = (t_actual / t_threshold) * 100
 
Risk = average(kScore, lScore, tScore)
**Step 6 : Decision**
* All metrics pass → PASS
* One or more fails → FAIL
* Borderline edge → WARNING

⠀**Step 7 : Generate Validation Report**
Includes:
* Metrics
* Thresholds
* Risk score
* Processing time
* Decision
* Failure reason

⠀**Step 8 : Publish Outcome**
* Send PASS/FAIL to Storage Service
* Write validation row in PostgreSQL
* Emit audit event
* ACK queue message

⠀**9. Interface / Exports**
**Inbound Queue: validation_queue**
Contains:
* job_id
* masked_file_path
* quasi_identifiers
* sensitive_attributes
* policy thresholds

⠀**Outbound Queue: storage_queue**
* On PASS → MOVE_PHASE (staging → safe)
* On FAIL → MOVE_PHASE (staging → quarantine)

⠀**Outbound Queue: audit_queue**
Contains:
* metrics
* risk score
* decision
* timestamp
* job reference
* service identifier

⠀**Optional Internal API**
* GET /validation/{job_id}/report
* GET /validation/health

⠀8.5 Storage Service
**8.5.1 Classification**
The **Storage Service** is classified as a **core infrastructure microservice** responsible for enforcing the five-phase dataset lifecycle and guaranteeing the confidentiality, integrity, durability, and regulatory compliance of all data stored within the SADN platform.
Its classification profile is as follows:
**Microservice Category**
* **Type:** Backend data-management microservice
* **Domain:** Storage lifecycle enforcement, file persistence, metadata management
* **Layer:** Data layer (infrastructure tier)

⠀**Pipeline Role**
* **Primary Role:**  Ensures correct placement, movement, and persistence of datasets as they pass through the SADN anonymization pipeline.
* **Pipeline Phases Owned:**  
  * **intake/** – initial data landing
  * **staging/** – processing state for NLP, Masking, and Validation
  * **quarantine/** – isolated state for failed or risky datasets
  * **safe/** – validated, compliant output datasets
  * **archive/** – long-term retention storage

⠀**Criticality Level**
* **Criticality:** **High**  The service handles original datasets, anonymized outputs, validation metrics, errors, and policies. Any failure directly impacts:  
  * Data integrity
  * Legal compliance (PDPL/NDMO)
  * Auditability and traceability
  * Pipeline continuity

⠀**Data Sensitivity Classification**
The Storage Service works with the most sensitive data in the system:
* **Original raw datasets (highly sensitive)**  
* **Derived anonymized datasets (regulated)**  
* **Privacy metrics and masking policies (sensitive)**
* **Operational metadata and audit trail fragments (confidential)**

⠀It must enforce:
* Encryption at rest (AES-256)
* TLS-secured transmission
* Strict internal-only access to *intake*, *staging*, and *quarantine*
* Controlled exposure ONLY for **safe** and **archive** datasets via pre-signed URLs

⠀**Interaction Pattern**
* **Consumers:** Orchestrator, NLP, Masking, Validation, Audit
* **Communication Style:**
  * **RabbitMQ commands** for lifecycle transitions
  * **Internal HTTP APIs** for metadata retrieval and pre-signed URLs
  * **MinIO S3 API** for file operations
  * **PostgreSQL DB writes** to maintain authoritative job state

⠀**Regulatory Alignment**
The Storage Service is categorized as a **compliance-bound subsystem**, required to uphold:
* PDPL principles
* NDMO Anonymization & Data Governance frameworks
* MOH retention policies
* SDAIA data protection and audit guidelines

⠀This classification expresses that Storage is not just a file-holding component, but a **legally governed storage controller** responsible for meeting national data protection obligations.
**Security Category**
* **Security Level:** Critical
* **Threat Sensitivity:** High (direct access to raw and processed data)
* **Security Controls:**
  * Isolation of phases
  * Integrity hashing
  * No overwrite policy
  * Atomic moves only
  * Strictly controlled access credentials (Vault-managed)
  * Mandatory audit event emission

⠀**8.5.2 Definition**
The **Storage Service** is the authoritative subsystem responsible for the **physical persistence, lifecycle control, and regulatory handling** of all datasets processed within SADN. It provides a structured, enforceable storage model that maps the platform’s anonymization workflow into concrete directory phases inside an S3-compatible storage backend.
The service acts as the **single owner of all file-level artifacts**, ensuring that every dataset follows a validated, auditable, and tamper-resistant flow from initial upload through anonymization, final approval, and long-term archival.
**Core Behavioral Definition**
The Storage Service provides:
**8.5.2.1 Lifecycle Enforcement**
A guaranteed progression through the five-phase model:
**1** **intake/** - raw uploads received, basic integrity + format checks
**2** **staging/** - working state for NLP → Masking → Validation
**3** **quarantine/** - isolated state for rejected or unsafe datasets
**4** **safe/** - validated outputs approved by Validation + DPO
**5** **archive/** - long-term regulatory retention storage

⠀All transitions are executed through **atomic directory renames**, ensuring no partial states, overwrites, or lost data.
**8.5.2.2 Dataset and Artifact Persistence**
The service stores:
* Original user datasets (raw, sensitive)
* Masked/anonymized datasets (final outputs)
* Validation results and privacy metrics
* Masking policy snapshots
* Error details (for failed jobs)
* Operational metadata and audit-linked attributes

⠀All objects are stored inside MinIO using a **strict path schema**:
{phase}/{job_id}/{file}
**8.5.2.3 Metadata & State Management**
For each job, Storage maintains:
* **metadata.json** – structural attributes and current phase
* **privacy_metrics.json** – k/l/t anonymity validation metrics
* **masking_policy.json** – the policy applied by the Masking Service
* **error.json** – details for quarantined datasets
* **audit_trail.json** – appended operations from all services

⠀These metadata items act as the **source of truth** for job-level decisions, UI state, and audit trails.
**8.5.2.4 Controlled Data Exposure**
Storage decides **what is visible** and **when**, enforcing security boundaries:
* **intake**, **staging**, **quarantine** → *never exposed*
* **safe**, **archive** → available *only* through secure pre-signed URLs

⠀This ensures that **no internal processing states leak to external users**.
**8.5.2.5 Integration Authority**
The Storage Service defines the file interface for all other microservices:
* NLP, Masking, Validation read/write from **staging/**
* Orchestrator triggers lifecycle movements
* Audit receives hash-chain events
* Federation Gateway only accesses **safe**/**archive** artifacts

⠀Every service depends on Storage for **canonical paths, metadata, and job progression**.
**Purpose Summary**
The Storage Service is defined as the **backbone of the SADN data pipeline**, responsible for:
* Enforcing regulated storage behavior
* Maintaining data integrity and traceability
* Guaranteeing atomic, auditable state transitions
* Preserving sensitive data under strict isolation guarantees
* Providing consistent artifacts to downstream microservices

⠀This definition sets the scope and boundaries for all responsibilities and constraints that follow.
**8.5.3 Responsibilities**
The Storage Service has end-to-end responsibility for managing dataset persistence, lifecycle transitions, integrity assurance, and controlled exposure across the SADN anonymization pipeline. Its responsibilities cover operational, security, compliance, and integration dimensions.
**8.5.3.1 Lifecycle Phase Management**
The Storage Service is the **sole authority** responsible for implementing and enforcing the five-phase storage model:
* **intake/** – receiving raw uploads
* **staging/** – workspace for processing
* **quarantine/** – for failed or unsafe jobs
* **safe/** – validated, DPO-approved datasets
* **archive/** – long-term retention storage

⠀**Key responsibilities include:**
* Guaranteeing **atomic directory moves** between phases
* Preventing illegal transitions (e.g., safe → staging)
* Maintaining strict separation and access boundaries across phases
* Preserving all previous states through append-only behavior

⠀**8.5.3.2 Dataset Persistence & File Operations**
Storage is responsible for all file-level operations, including:
* Uploading raw files into **intake/**
* Persisting all generated artifacts in the correct phase directory
* Storing sidecar metadata files (metadata, policies, metrics, errors)
* Ensuring directory consistency, correct structure, and naming conventions
* Enforcing encryption at rest and secure transport

⠀No other microservice is allowed to directly manipulate MinIO buckets.
**8.5.3.3 Metadata Generation & Maintenance**
The service creates and maintains all job-level metadata files that describe:
* File attributes (format, size, hash)
* Current storage phase
* Privacy metrics from Validation
* Masking policies applied
* Errors and failure reason codes
* Audit information related to file operations

⠀This metadata ensures downstream services and the audit trail always operate on **authoritative, consistent information**.
**8.5.3.4 Policy Enforcement**
The Storage Service enforces all storage-related rules defined in the platform, including:
* Maximum file size enforcement (e.g., 500MB limit)
* Supported format enforcement (CSV, JSON, Parquet, Excel)
* Malware and unsafe path protection
* Retention period enforcement
* Zero-overwrite and append-only semantics
* Access restrictions by phase

⠀It serves as the primary checkpoint preventing unsafe or invalid datasets from progressing.
**8.5.3.5 Integration Responsibilities**
Storage coordinates with all pipeline services:
**With Orchestrator**
* Receives lifecycle commands
* Provides job phase and path metadata
* Supplies pre-signed URLs for safe/archive retrieval

⠀**With NLP, Masking, Validation**
* Supplies staging paths
* Accepts newly generated artifacts
* Moves datasets forward based on their outputs

⠀**With Audit**
* Emits hash-chained events for every operation
* Supplies file hashes and metadata on request

⠀**With Federation Gateway**
* Exposes anonymized datasets through controlled pre-signed URLs

⠀**8.5.3.6 Integrity & Traceability Assurance**
The Storage Service ensures:
* SHA-256 or equivalent hashing of input and output datasets
* Consistent audit event generation on every transition
* No silent failures or untracked modifications
* Long-term reproducibility of processing history

⠀Every change to dataset state must be **auditable, tamper-evident, and reversible only through approved procedures**.
**8.5.3.7 Security Controls**
Storage is responsible for applying security controls to the data it manages:
* Encryption of all objects at rest
* TLS for all internal communications
* Isolation of sensitive phases (intake, staging, quarantine)
* Credential scoping through Vault
* Controlled generation of pre-signed URLs

⠀It protects the highest-risk data in the entire system.
**8.5.3.8 Retention & Archival**
The Storage Service must:
* Track retention timers for all completed jobs
* Move eligible datasets from **safe/** to **archive/**
* Ensure archived datasets remain retrievable and auditable
* Prevent premature deletion or tampering

⠀**8.5.3.9 Error Handling & Recovery**
Storage ensures:
* Failed jobs are safely moved to **quarantine/**
* error.json is generated or updated with structured details
* Recovery workflows can reference previous states
* No partial or corrupted dataset ever re-enters the pipeline

⠀**8.5.4 Constraints**
The Storage Service operates under strict technical, security, and regulatory constraints to ensure safe and compliant dataset handling.
**8.5.4.1 Regulatory Constraints**
* Must comply with PDPL and NDMO anonymization rules.
* Raw data cannot be exposed to end users at any stage.
* Mandatory retention periods apply for finalized datasets (safe/ → archive/).
* Auditability and traceability must be preserved for the full retention window.

⠀**8.5.4.2 Security Constraints**
* **Phase isolation:** intake/, staging/, and quarantine/ are internal-only.
* **Encryption:** AES-256 at rest + TLS in transit.
* **Credentials:** Scoped, Vault-managed MinIO access keys.
* **Pre-signed URLs** allowed only for safe/ and archive/.

⠀**8.5.4.3 Architectural Constraints**
* Storage is the **sole authority** over file placement and lifecycle movement.
* All phase transitions must use **atomic rename** operations.
* Append-only behavior: no overwriting or destructive updates.
* Directory schema is fixed: {phase}/{job_id}/.

⠀**8.5.4.4 Performance & Capacity Constraints**
* Enforced maximum upload size (e.g., 500MB).
* Must support concurrent ingestion and processing jobs.
* Low-latency metadata access required for Orchestrator and UI responsiveness.

⠀**8.5.4.5 Technology Constraints**
* MinIO is the exclusive object storage backend.
* PostgreSQL holds authoritative job state; must match MinIO state.
* All lifecycle transitions triggered only through RabbitMQ commands.

⠀**8.5.4.6 Error Handling Constraints**
* Any failure must result in quarantine/ placement + error.json.
* No partial or inconsistent file states permitted.

⠀**8.5.4.8 Auditability Constraints**
* Must compute and preserve file hashes for integrity checks.
* Every storage operation must emit an audit event.  

⠀**8.5.5 Composition**
The Storage Service is composed of several internal modules, each responsible for a distinct part of the storage lifecycle, metadata handling, and integration with other microservices.
**8.5.5.1 Command & Event Handler**
* Consumes lifecycle commands from storage_queue.
* Publishes audit events to audit_queue.
* Routes actions to the correct internal controller.

⠀**8.5.5.2 Lifecycle Controller**
* Implements the five-phase storage state machine.
* Validates allowed transitions (e.g., intake → staging, staging → safe).
* Ensures atomic renames and consistent state changes.

⠀**8.5.5.3 MinIO Adapter**
* Wraps all S3/MinIO operations (PUT, GET, LIST, RENAME).
* Enforces directory structure: {phase}/{job_id}/.
* Ensures encryption, permissions, and bucket policies are applied.

⠀**8.5.5.4 Metadata Manager**
* Creates and updates all sidecar files:
  * metadata.json
  * privacy_metrics.json
  * masking_policy.json
  * error.json
  * audit_trail.json
* Syncs metadata with PostgreSQL (jobs.storage_phase, jobs.storage_path).

⠀**8.5.5.5 Pre-Signed URL Generator**
* Produces secure, time-limited URLs for datasets in safe/ and archive/.
* Ensures exposure rules are respected (no URLs for internal phases).

⠀**8.5.5.6 Retention & Archival Module**
* Detects jobs eligible for archival.
* Moves datasets from safe/ → archive/.
* Emits corresponding audit events.

⠀**8.5.5.8 Internal API Layer**
* Provides internal-only endpoints used by Orchestrator and Validation:
  * Get job metadata
  * Request pre-signed URLs
  * Retrieve storage-phase info
* Not accessible externally.  

⠀**8.5.6 Uses / Interactions**
The Storage Service interacts with several SADN microservices to manage dataset flow, metadata, and lifecycle transitions.
**8.5.6.1 Orchestrator**
* Sends commands: STORE_INTAKE, PROMOTE_TO_STAGING, MOVE_TO_SAFE, MOVE_TO_QUARANTINE, ARCHIVE_JOB.
* Receives storage paths and pre-signed URLs for safe/ and archive/.
* Uses Storage as the **source of truth** for dataset phase and location.

⠀**8.5.6.2 NLP, Masking, and Validation Services**
* Read datasets from staging/.
* Write derived outputs (masked files, metrics, policies) to the same job directory.
* Trigger transitions via Orchestrator once processing is complete.

⠀**8.5.6.3 Audit Service**
* Receives all storage-related events through audit_queue.
* Uses file hashes, metadata changes, and transitions to build the hash-chain audit log.
* Ensures storage behavior is fully auditable.

⠀**8.5.6.4 Federation Gateway**
* Accesses datasets only from **safe/** and **archive/** using Storage-provided pre-signed URLs.
* Cannot access internal phases.

⠀**8.5.6.5 PostgreSQL Database**
* Receives updates to jobs.storage_phase and jobs.storage_path after every transition.
* Provides authoritative state for UI and Orchestrator.

⠀**8.5.6.6 MinIO Object Storage**
* Acts as the physical persistence layer for all datasets and metadata.
* Storage Service manages **all** object operations; no other service interacts with MinIO directly.

⠀**8.5.6.7 UI / Dashboard (Indirect)**
* UI requests status and dataset availability through Orchestrator → Storage.

⠀**8.5.7 Resources**
The Storage Service requires specific compute, storage, configuration, and integration resources to operate reliably and securely.
**8.5.7.1 Compute & Memory**
* Lightweight container (≈ 0.5–1 CPU and 512MB–1GB RAM).
* Sufficient for metadata processing and MinIO operations.
* Scales horizontally if ingestion volume increases.

⠀**8.5.7.2 Object Storage (MinIO)**
* Primary storage backend for all datasets and metadata.
* Requires persistent volumes sized according to expected dataset load.
* Encryption at rest enabled (AES-256 SSE).
* Bucket structure enforced by Storage Service.

⠀**8.5.7.3 Database Resources (PostgreSQL)**
* Stores job-level metadata:
  * storage_phase
  * storage_path
  * timestamps
* Must maintain strong consistency with MinIO state.

⠀**8.5.7.5 Message Queue (RabbitMQ)**
* Consumes commands from storage_queue.
* Publishes events to audit_queue.
* Long-lived connections required for reliable transitions.

⠀**8.5.7.6 Configuration & Secrets**
* MinIO credentials (access key, secret key).
* RabbitMQ connection settings.
* Database connection string.
* All secrets retrieved via **Vault**.
* Configurable limits: max file size, retention periods.

⠀**8.5.7.7 Internal API Endpoints**
* Metadata lookup
* Pre-signed URL generation
* Job state and path queries  (All internal-only, not externally exposed.)

⠀**8.5.7.8 File System / Volume Requirements**
* MinIO backend persists objects on attached storage volumes.
* Volumes must support:
  * High I/O throughput
  * Durable writes
  * Consistent read operations

⠀**8.5.8 Processing Logic**
**8.5.8.1 Intake Save**
**Steps**
* Receive STORE_INTAKE command.
* Create intake/{job_id}/ directory.
* Upload raw dataset file.
* Generate metadata.json with initial attributes.
* Update DB: storage_phase = intake.
* Emit STORAGE_INTAKE_SAVED audit event.  

⠀


**8.5.8.2 Promote to Staging**
**Steps**
* Receive PROMOTE_TO_STAGING.
* Atomically rename intake/{job_id}/ → staging/{job_id}/.
* Add .processing lock if enabled.
* Update DB: storage_phase = staging.
* Emit STORAGE_PHASE_PROMOTION event.

⠀**8.5.8.3 Move to Safe**
**Steps**
* **3.1** Confirm Validation passed and DPO approval exists.
* **3.2** Rename staging/{job_id}/ → safe/{job_id}/.
* **3.3** Update DB: storage_phase = safe.
* **3.4** Emit STORAGE_SAFE_FINALIZED event.

⠀**8.5.8.4 Move to Quarantine**
**Steps**
* Ensure error.json is present or create it.
* Rename staging/{job_id}/ → quarantine/{job_id}/.
* Update DB: storage_phase = quarantine.
* Emit STORAGE_QUARANTINED event.

⠀**8.5.8.5 Archive Job**
**Steps**
* Check retention period eligibility.
* Rename safe/{job_id}/ → archive/{job_id}/.
* Update DB: storage_phase = archive.
* Emit STORAGE_ARCHIVED event.

⠀8.6 Audit Service
**8.6.1 Classification**
The Audit Service is classified as a **security-critical, compliance-bound microservice** responsible for generating, storing, and maintaining a **tamper-evident audit trail** for all dataset operations across SADN.
**Category**
* **Type:** Backend security & compliance microservice
* **Domain:** Audit logging, hash-chain integrity, compliance reporting
* **Criticality:** **Very High** (affects legal defensibility and PDPL compliance)

⠀**Data Sensitivity**
Handles only **metadata**, not raw datasets, but the metadata itself is sensitive (operations, identities, decision logs).
**Interaction Style**
* Consumes events from all services via audit_queue.
* Generates **cryptographic hash-chained logs**.
* Exposes internal APIs for audit retrieval and compliance reports.

⠀**8.6.2 Definition**
The Audit Service provides an **append-only, tamper-evident audit ledger** that records every significant action performed by SADN microservices.
It ensures:
* Traceability of dataset flow
* Forensic visibility into all state transitions
* Compliance with PDPL, NDMO, and institutional audit requirements
* Cryptographic integrity verification through SHA-256 hash-chaining

⠀Audit does **not** store raw data - only **events, metadata, timestamps, and signatures**.
**8.6.3 Responsibilities**
**Core Responsibilities**
* Maintain an **append-only audit log** for all microservices.
* Compute **SHA-256 hash chains** to ensure logs cannot be altered.
* Store structured event data (service, timestamp, action, job_id, metadata).
* Provide APIs for DPO/compliance staff to query, filter, and export logs.
* Ensure long-term retention of audit data.

⠀**Integration Responsibilities**
* Consume all events from audit_queue.
* Validate event structure and reject malformed entries.
* Link each event to the previous event in the chain.
* Provide summary and report generation features (optional phase).

⠀**8.6.4 Constraints**
**Regulatory Constraints**
* Must meet PDPL & NDMO logging requirements.
* Must preserve audit logs for the same duration as archived datasets.
* Deletion or overwriting of logs is prohibited.

⠀**Security Constraints**
* Mandatory **hash-chain integrity** (Merkle chain model).
* Restricted access (internal-only APIs).
* Encryption in transit and at rest.

⠀**Architectural Constraints**
* Append-only semantics - no update operations allowed.
* All audit events must originate from audit_queue.
* Stored events must be timestamped, signed, and hash-linked.

⠀**Performance Constraints**
* Must handle high-frequency events during peak pipeline activity.
* Low-latency event ingestion is required to avoid queue backlog.

⠀**8.6.5 Composition**
**8.6.5.1 Event Consumer**
* Subscribes to audit_queue.
* Validates event schema.
* Routes events to hash-chain builder.

⠀**8.6.5.2 Hash-Chain Engine**
* Computes current_hash = SHA256(previous_hash + event_payload).
* Maintains chain consistency and ensures tamper detection.

⠀**8.6.5.3 Audit Log Store**
* Append-only storage (PostgreSQL table or dedicated ledger store).
* Stores event payload + hash + previous_hash + timestamp.

⠀**8.6.5.4 Query & Reporting Module**
* Supports internal API queries by job_id, service, time range.
* Generates compliance reports (daily/weekly/monthly).

⠀**8.6.5.5 Integrity Verification Module**
* Recomputes chain for verification requests.
* Detects missing, reordered, or modified entries.

⠀**8.6.6 Uses / Interactions**
**With All Microservices**
* Receives a continuous stream of audit events (ingestion, masking, validation, storage movements, errors, etc.).

⠀**With Orchestrator**
* Provides system-wide audit summaries.
* Supports workflow-level tracing.

⠀**With Storage Service**
* Receives integrity-sensitive events (phase promotions, file hashes).

⠀**With UI / Compliance Dashboard**
* Exposes internal endpoints for audit browsing and exporting (restricted to DPO/compliance team).

⠀**With PostgreSQL**
* Stores all audit entries with hash-chain fields.

⠀**8.6.7 Resources**
**Compute**
* Moderate CPU/RAM (audit events are lightweight).

⠀**Database**
* Dedicated audit log table with append-only semantics:
  * event_id
  * timestamp
  * service
  * action
  * job_id
  * metadata
  * prev_hash
  * curr_hash

⠀**Message Queue**
* Relies on audit_queue for ingestion.

⠀**Configuration & Secrets**
* Signing/crypto keys
* DB credentials
* Hash-chain root seed

⠀**8.6.8 Processing Logic**
**8.6.8.1 Event Ingestion**
**Steps**
* Receive event from audit_queue.
* Validate schema (service, action, job_id).
* Normalize metadata and timestamps.

⠀**8.6.8.2 Hash-Chain Construction**
**Steps**
* Fetch previous hash from the last audit record.
* Compute new hash:  H = SHA256(previous_hash + event_json)
* Attach previous_hash and current_hash to event.

⠀**8.6.8.3 Append to Audit Log**
**Steps**
* Insert event into audit log table.
* Guarantee append-only behavior (no updates).
* Confirm write durability.

⠀**8.6.8.4 Integrity Verification (On Request)**
**Steps**
* Retrieve full chain or required subset.
* Recompute hashes sequentially.
* Detect any mismatch or missing record.

⠀**8.6.8.5 Query & Reporting**
**Steps**
* Filter logs by job_id, service, or timeframe.
* Apply aggregation rules for compliance summaries.
* Export results to DPO dashboard.

⠀8.7 Federation Gateway
**8.7.1 Classification**
The Federation Gateway is classified as an independent microservice responsible for secure cross-institutional data exchange. It is implemented in Python using the FastAPI framework and operates on a dedicated port (8443) separated from standard API traffic. Unlike other SADN services that communicate exclusively within the internal Docker network, the Federation Gateway establishes encrypted connections with external peer institutions using mutual TLS authentication. For the capstone deployment, the gateway operates in outbound-only mode, meaning it can transmit datasets to peer institutions but does not accept inbound transfers.
**8.7.2 Definition**
The Federation Gateway enables secure sharing of validated, anonymized datasets between Saudi Anonymization and Data Masking Network instances operated by partner institutions. Its purpose is to support collaborative research scenarios where anonymized data must cross organizational boundaries while maintaining compliance with PDPL cross-border transfer requirements and institutional data governance policies.
The gateway serves as the trust boundary between the local SADN instance and external parties. It ensures that only datasets meeting strict eligibility criteria-completed validation, adequate privacy metrics, and active legal agreements-can be transmitted. By centralizing federation logic in a dedicated service, the architecture isolates external communication risks from the core anonymization pipeline.
**8.7.3 Responsibilities**
The Federation Gateway validates transfer eligibility before initiating any external communication. This includes verifying that the requested job has completed the full anonymization pipeline, resides in safe storage, and meets the privacy metric thresholds configured for federation. Jobs that have not been approved by the Data Owner or that failed validation cannot be shared regardless of the request.
Data Use Agreement enforcement is a critical responsibility. Before any dataset transmission, the gateway queries the agreements registry to confirm that an active, unexpired agreement exists between the local institution and the target peer. The agreement must cover the data category being shared and must not have been revoked. Without a valid agreement, the transfer is refused.
The gateway establishes secure connections using mutual TLS, where both the local instance and the peer must present valid X.509 certificates. This two-way authentication ensures that datasets are transmitted only to verified institutions and that transmission occurs over encrypted channels. The Certificate Manager module handles certificate validation, expiration checking, and revocation verification.
Once eligibility and trust are confirmed, the gateway retrieves the masked dataset from safe storage, applies hybrid encryption (symmetric encryption for the dataset, asymmetric encryption for the key), generates a digital signature for integrity verification, and transmits the secure container to the peer endpoint. It then awaits acknowledgment confirming successful receipt and decryption before marking the transfer complete.
All federation activities are recorded through audit events published to the audit queue, providing complete traceability of cross-institutional data movement.
**8.7.4 Constraints**
The Federation Gateway operates under strict eligibility constraints. Only jobs with COMPLETED status residing in the safe storage phase can be shared. This ensures that raw data, partially processed data, or failed datasets never leave the institution. The privacy metrics of the dataset must meet federation-specific thresholds, which may be stricter than general validation thresholds.
Legal constraints require an active Data Use Agreement for every transfer. Agreements are stored in PostgreSQL with expiration dates, permitted data categories, and purpose limitations. The gateway refuses transfers when agreements are expired, revoked, or do not cover the requested data type. This constraint reflects PDPL requirements for lawful basis when sharing personal data between institutions.
Security constraints mandate mutual TLS for all peer communication. Both parties must possess valid certificates issued by trusted authorities. Self-signed certificates are not accepted in production deployments. The gateway verifies certificate chains, checks expiration, and consults revocation lists before establishing connections.
Architectural constraints limit the gateway to outbound transfers for the capstone scope. Inbound federation, where the local instance receives datasets from peers, is not implemented. This simplification reduces the attack surface and aligns with the initial deployment requirements. Future releases may enable bidirectional federation.
The gateway communicates with peers exclusively on port 8443, which is separate from the standard API port used by the Orchestrator. This separation enables network-level access controls that restrict federation traffic to authorized peer networks while keeping internal API traffic isolated.
**8.7.5 Composition**
The Federation Gateway comprises four internal modules that collectively implement the secure transfer protocol.
The Certificate Manager handles all aspects of X.509 certificate lifecycle. It loads the institutional certificate and private key at startup, validates peer certificates during connection establishment, checks certificate expiration and revocation status, and manages the TLS context for outbound connections. When certificates approach expiration, the module can trigger rotation workflows.
The Peer Registry maintains the list of authorized partner institutions. Each peer record includes the institution name, federation endpoint URL, public certificate, connection status, and health check timestamps. The registry is populated through an administrative registration process that occurs outside the normal data flow. Periodic health checks verify that registered peers remain reachable.
The DUA Validator enforces Data Use Agreement requirements. When a transfer is requested, this module queries the agreements table to find active agreements between the local institution and the target peer. It verifies that the agreement covers the data category, has not expired, and permits the intended use. If multiple agreements exist, the most specific applicable agreement is selected.
The Transfer Handler executes the actual transmission. It retrieves the dataset from MinIO, computes integrity hashes, generates digital signatures using the institutional private key, applies hybrid encryption using the peer's public key, packages everything into a secure container, and transmits via mTLS. It then processes the peer's acknowledgment to confirm successful delivery.
**8.7.6 Uses/Interactions**
The Federation Gateway receives transfer requests from the Orchestrator through an internal HTTP endpoint. When a Data Owner or DPO initiates federation through the external API, the Orchestrator validates authorization and delegates to the gateway. This separation ensures that external users never interact directly with the federation service.
The gateway reads validated datasets from MinIO safe storage. It has read-only access to the safe phase and cannot access intake, staging, or quarantine phases. This restriction ensures that only approved, anonymized data can be transmitted externally.
PostgreSQL provides persistence for federation-related data. The gateway queries the jobs table to verify completion status, the federation_peers table to retrieve peer endpoints and certificates, the data_use_agreements table to validate legal requirements, and inserts records into the federation_transfers table to document completed transmissions.
HashiCorp Vault stores the institutional private key used for digital signatures and the certificates required for mTLS establishment. The gateway retrieves these secrets at startup and when rotation occurs. Credentials for database and storage access are also obtained from Vault.
External peer SADN instances are the ultimate destination for transmitted datasets. Communication occurs over mTLS on port 8443. The gateway initiates connections to peer endpoints registered in the Peer Registry. Peers must respond with valid acknowledgments confirming receipt.
The audit queue receives federation events documenting all transfer attempts. Both successful and failed transfers are logged with relevant details including peer identity, dataset reference, and outcome.
**8.7.7 Resources**
Network resources include outbound connectivity on port 8443 to registered peer endpoints. Firewall rules must permit this traffic to authorized peer IP ranges. The gateway also requires internal connectivity to MinIO, PostgreSQL, Vault, and RabbitMQ.
Cryptographic resources include the institutional X.509 certificate and corresponding private key for mTLS and digital signatures. Peer public certificates are stored in the Peer Registry for encryption operations. All cryptographic operations use algorithms compliant with NCA requirements: AES-256-GCM for symmetric encryption, RSA-4096 with OAEP for asymmetric operations, and RSA-PSS for signatures.
Database resources include four PostgreSQL tables: jobs for eligibility verification, federation_peers for endpoint resolution, data_use_agreements for legal validation, and federation_transfers for transfer logging. The gateway requires SELECT access to the first three tables and INSERT access to the transfers table.
The audit queue is the sole RabbitMQ resource. The gateway publishes FEDERATION_TRANSFER_COMPLETE and FEDERATION_TRANSFER_FAILED events but does not consume from any queue.
**8.7.8 Processing**
Federation processing follows a twelve-step protocol designed to ensure secure, compliant data exchange.
The process begins when the gateway receives a transfer request from the Orchestrator specifying the job and target peer. The gateway first validates that the job exists, has COMPLETED status, and resides in safe storage. It then retrieves the privacy metrics and verifies they meet federation thresholds.
Next, the gateway consults the Peer Registry to retrieve the target institution's endpoint and certificate. If the peer is not registered or has been deactivated, the transfer is refused. The DUA Validator then checks for an active agreement covering this transfer. Agreement validation includes expiration checking, category matching, and purpose verification.
With eligibility confirmed, the gateway retrieves the masked dataset from MinIO. It computes a SHA-256 hash of the dataset content and generates a digital signature using the institutional private key. This signature enables the peer to verify the dataset originated from the claimed institution and was not modified in transit.
The dataset undergoes hybrid encryption. A random AES-256 session key is generated and used to encrypt the compressed dataset. The session key itself is then encrypted using the peer's RSA public key. This approach combines the efficiency of symmetric encryption for large data with the security of asymmetric encryption for key exchange.
The encrypted dataset, encrypted session key, digital signature, and metadata are packaged into a secure container. The gateway then establishes an mTLS connection to the peer endpoint on port 8443. Both parties validate certificates before the connection completes.
The secure container is transmitted to the peer's federation receive endpoint. The gateway awaits an acknowledgment containing the peer's verification results. A successful acknowledgment confirms that the peer decrypted the dataset and validated the signature.
Upon successful acknowledgment, the gateway records the transfer in PostgreSQL and publishes an audit event. If any step fails, the transfer is marked as failed, an error audit event is published, and an appropriate error response is returned to the Orchestrator.
The complete protocol specification and pseudocode are documented in Section ~[7.7.3](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.tycjiubsktau)~.
**8.7.9 Interface/Exports**
The Federation Gateway exposes a single internal HTTP endpoint for receiving transfer requests from the Orchestrator. This endpoint accepts the job identifier and target peer identifier, initiates the federation protocol, and returns the transfer outcome. External users cannot access this endpoint directly.
The gateway does not expose any external HTTP endpoints in the capstone deployment. Peer institutions communicate with their own SADN instances, which then use their federation gateways to reach this instance. The outbound-only constraint means this gateway initiates connections but does not accept incoming federation requests.
Audit events are the primary exported data. The gateway publishes events to the audit queue for every transfer attempt. Successful transfers generate FEDERATION_TRANSFER_COMPLETE events containing the transfer identifier, peer institution, dataset hash, and timestamp. Failed transfers generate FEDERATION_TRANSFER_FAILED events with error details.
Database exports include transfer records inserted into the federation_transfers table. These records document the complete history of cross-institutional data sharing for compliance and audit purposes.
Interface specifications, message formats, and endpoint details are documented in Section ~[7.7.4](https://docs.google.com/document/d/125j63hliY8vwoWbU1Y5u0TmxgIwykXaGnxd_-jE5aMI/edit?pli=1&tab=t.0#heading=h.ail5zfuw0l0r)~.
### 8 Other Design Features

⠀
### 9.1 Performance & Reliability
This section defines the performance objectives, reliability mechanisms, and operational resilience strategies that govern the SADN platform. The design ensures that the system processes datasets efficiently, recovers gracefully from failures, and maintains consistent availability under expected workloads.
**9.1.1 Performance Objectives**
The SADN platform is designed for batch-style asynchronous processing rather than real-time operations. Performance targets are established based on regulatory timelines, user expectations, and infrastructure constraints typical of institutional healthcare and educational environments.
**9.1.1.1 Processing Throughput**
The following table defines the target and maximum processing durations for each pipeline stage:
| **Pipeline Stage** | **Target Duration** | **Maximum Duration** | **Applicable Dataset Size** |
|:-:|:-:|:-:|:-:|
| Intake Validation | 30 seconds | 120 seconds | Up to 500 MB |
| Column Classification | 45 seconds | 90 seconds | Up to 500 MB |
| NLP Detection | 60 seconds | 180 seconds | Up to 500 MB |
| Masking Transformation | 5 minutes | 15 minutes | Up to 500 MB |
| Privacy Validation | 35 seconds | 60 seconds | Up to 500 MB |
| End-to-End Processing | 10 minutes | 30 minutes | Up to 500 MB |
*Table 148.* 
These targets assume standard institutional hardware and typical dataset structures. Datasets with extensive free-text columns or complex generalization hierarchies may approach maximum durations.
**9.1.1.2 API Responsiveness**
External-facing endpoints exposed by the Orchestrator maintain the following latency targets:
| **Operation** | **Target Latency** | **99th Percentile** |
|:-:|:-:|:-:|
| Job submission acknowledgment | < 2 seconds | < 5 seconds |
| Status query response | < 200 ms | < 500 ms |
| Validation report retrieval | < 500 ms | < 1 second |
| File download initiation | < 1 second | < 3 seconds |
*Table 149.* 
These targets ensure responsive user interactions while the underlying pipeline processes asynchronously.
**9.1.1.3 Concurrency and Capacity**
The system supports concurrent job processing bounded by available infrastructure resources:
| **Capacity Metric** | **Recommended** | **Maximum** |
|:-:|:-:|:-:|
| Concurrent active jobs | 5 | 10 |
| Queue depth per service | 50 messages | 100 messages |
| Database connection pool | 10 connections | 20 connections |
| Daily job throughput | 50 jobs | 100 jobs |
*Table 150.* 
Exceeding recommended thresholds may result in increased processing times but does not compromise data integrity or correctness.
### 9.1.2 Scalability Architecture
The microservices architecture enables independent scaling of pipeline components based on workload characteristics. Services are categorized by their scaling behavior:
**9.1.2.1 Horizontally Scalable Services**
The following services are stateless and support horizontal scaling through replica deployment:
| **Service** | **Scaling Trigger** | **Scaling Benefit** |
|:-:|:-:|:-:|
| NLP Service | Queue backlog > 20 messages | Parallel text processing |
| Masking Service | Queue backlog > 10 messages | Parallel transformation |
| Validation Service | Queue backlog > 15 messages | Parallel metric computation |
*Table 151.* 
Adding replicas distributes queue consumption across workers, reducing overall processing time during peak loads.
**9.1.2.2 Singleton Services**
The following services operate as single instances by design:
| **Service** | **Rationale** |
|:-:|:-:|
| Orchestrator | Centralized entry point; stateless request handling |
| Audit Service | Sequential hash-chaining requires ordered processing |
| Storage Service | Coordinates phase transitions; atomic operations |
| Federation Gateway | Certificate and connection state management |
*Table 152.* 
These services handle load through efficient internal processing rather than replication. The Orchestrator remains responsive under load because it delegates all intensive work to downstream services.
**9.1.2.3 Infrastructure Scaling**
Infrastructure components scale according to data volume growth:
| **Component** | **Scaling Approach** | **Indicator** |
|:-:|:-:|:-:|
| PostgreSQL | Vertical (CPU/RAM) | Query latency > 100 ms |
| MinIO | Horizontal (nodes) | Storage utilization > 70% |
| RabbitMQ | Vertical then horizontal | Queue depth sustained > 100 |
*Table 153.* 
**9.1.3 Reliability Mechanisms**
The platform implements multiple reliability patterns to ensure consistent operation and data protection throughout the anonymization pipeline.
**9.1.3.1 Fault Isolation**
The microservices architecture inherently isolates failures. A malfunction in one service affects only jobs currently being processed by that service, while other pipeline stages continue operating normally. This isolation is achieved through:
* **Independent container execution**: Each service runs in its own Docker container with dedicated resources.
* **Queue-based decoupling**: Services communicate exclusively through persistent message queues, eliminating direct dependencies.
* **Database connection isolation**: Each service maintains its own connection pool, preventing connection exhaustion in one service from affecting others.

⠀**9.1.3.2 Message Delivery Guarantees**
RabbitMQ provides reliable message delivery through the following configuration:
| **Guarantee** | **Implementation** |
|:-:|:-:|
| Persistence | All queues configured as durable; messages marked persistent |
| Acknowledgment | Manual consumer acknowledgment after successful processing |
| Publisher confirmation | Orchestrator and services confirm message acceptance |
| Redelivery | Unacknowledged messages automatically requeued on consumer failure |
*Table 154.* 
This configuration ensures that no job is lost due to transient service failures or restarts.
**9.1.3.3 Data Durability**
Critical data is protected through multiple durability mechanisms:
| **Data Type** | **Durability Mechanism** |
|:-:|:-:|
| Job metadata | PostgreSQL with WAL (Write-Ahead Logging) |
| Dataset files | MinIO with server-side encryption |
| Audit logs | Append-only table with Merkle chain verification |
| Processing results | Transactional database writes |
*Table 155.* 
Phase transitions in the Storage Service use atomic operations, ensuring that files are never partially moved or duplicated between storage phases.
**9.1.4 Fault Tolerance and Recovery**
The system is designed to recover from failures without data loss or corruption, maintaining pipeline integrity even when individual components experience problems.
**9.1.4.1 Retry Strategy**
Transient failures trigger automatic retry with exponential backoff:
| **Parameter** | **Value** |
|:-:|:-:|
| Maximum retry attempts | 3 |
| Initial retry delay | 1 second |
| Backoff multiplier | 2.0 |
| Maximum delay | 30 seconds |
*Table 156.* 
This strategy handles temporary network issues, brief database unavailability, and intermittent service errors without operator intervention.
**9.1.4.2 Dead Letter Queue Handling**
Messages that fail after exhausting retry attempts are routed to service-specific dead letter queues:
| **Service Queue** | **Dead Letter Queue** | **Retention** |
|:-:|:-:|:-:|
| validation_queue | validation_dlq | 7 days |
| masking_queue | masking_dlq | 7 days |
| nlp_queue | nlp_dlq | 7 days |
| storage_queue | storage_dlq | 7 days |
| audit_queue | audit_dlq | 30 days |
*Table 157.* 
Dead letter queues preserve failed messages for investigation and manual reprocessing. Operators receive alerts when messages enter any dead letter queue, enabling timely intervention.
**9.1.4.3 Service Recovery**
Each service is configured for automatic recovery following container failures:
| **Recovery Scenario** | **Mechanism** | **Recovery Time** |
|:-:|:-:|:-:|
| Container crash | Docker restart policy (always) | < 30 seconds |
| Unresponsive service | Health check failure triggers restart | < 60 seconds |
| Database connection loss | Connection pool reconnection | < 10 seconds |
| Queue connection loss | Automatic reconnection with backoff | < 30 seconds |
*Table 158.* 
Jobs in progress during a service failure are recovered through message redelivery. The idempotent design of each service ensures that reprocessing produces consistent results.
**9.1.4.4 Graceful Degradation**
Under extreme load or partial system failure, the platform degrades gracefully:
| **Condition** | **System Behavior** |
|:-:|:-:|
| Queue backlog exceeds threshold | New jobs accepted but processing delayed |
| Database connection exhaustion | API returns 503; jobs queued for later processing |
| Storage service unavailable | Pipeline pauses; jobs resume when service recovers |
| NLP service unavailable | Jobs without free-text columns continue processing |
*Table 159.* 
The system prioritizes data integrity over throughput, ensuring that no job completes with incorrect or incomplete processing.
**9.1.5 Backup and Recovery**
The backup strategy ensures data protection aligned with PDPL retention requirements and institutional disaster recovery policies.
**9.1.5.1 Backup Schedule**
| **Component** | **Backup Method** | **Frequency** | **Retention Period** |
|:-:|:-:|:-:|:-:|
| PostgreSQL | Full dump + continuous WAL archiving | Daily full; continuous incremental | 30 days |
| MinIO (safe/) | Snapshot replication | Daily | 5 years |
| MinIO (archive/) | Cold storage synchronization | Weekly | 7 years |
| Audit logs | Dedicated backup with integrity verification | Daily | 7 years |
| Configuration | Version-controlled repository | On change | Indefinite |
*Table 160.* 
Staging and intake phases are not backed up as they contain transient data that is either promoted to safe storage or moved to quarantine.
**9.1.5.2 Recovery Objectives**
| **Metric** | **Target** | **Description** |
|:-:|:-:|:-:|
| Recovery Time Objective (RTO) | 4 hours | Maximum acceptable downtime |
| Recovery Point Objective (RPO) | 1 hour | Maximum acceptable data loss |
*Table 161.* 
These objectives are achievable through the combination of continuous WAL archiving for PostgreSQL and daily MinIO snapshots.
**9.1.5.3 Recovery Procedures**
Recovery procedures are documented and tested quarterly:
* **Database recovery**: Point-in-time restoration using WAL archives
* **Storage recovery**: MinIO snapshot restoration to target timestamp
* **Job state reconstruction**: Audit log replay to identify incomplete jobs
* **Configuration restoration**: Deployment from version-controlled repository

⠀Following recovery, the Audit Service verifies hash chain integrity to confirm that no audit records were lost or corrupted.
**9.1.6 Monitoring with Prometheus**
The platform uses Prometheus for metrics collection, enabling real-time visibility into system health and performance. Each microservice exposes a metrics endpoint that Prometheus scrapes at configured intervals.
**9.1.6.1 Metrics Architecture**
| **Component** | **Metrics Endpoint** | **Scrape Interval** |
|:-:|:-:|:-:|
| Orchestrator | :8000/metrics | 15 seconds |
| NLP Service | :8001/metrics | 15 seconds |
| Masking Service | :8002/metrics | 15 seconds |
| Validation Service | :8003/metrics | 15 seconds |
| Storage Service | :8004/metrics | 15 seconds |
| Audit Service | :8005/metrics | 15 seconds |
| Federation Gateway | :8443/metrics | 15 seconds |
| PostgreSQL Exporter | :9187/metrics | 30 seconds |
| RabbitMQ Exporter | :9419/metrics | 30 seconds |
| MinIO | :9000/minio/v2/metrics | 30 seconds |
*Table 162.* 
**9.1.6.2 Key Performance Metrics**
The following metrics are collected and monitored across all services:
| **Metric Category** | **Example Metrics** | **Purpose** |
|:-:|:-:|:-:|
| Request metrics | http_requests_total, http_request_duration_seconds | API performance tracking |
| Queue metrics | rabbitmq_queue_messages, rabbitmq_queue_consumers | Pipeline throughput monitoring |
| Processing metrics | job_processing_duration_seconds, jobs_completed_total | Job performance analysis |
| Resource metrics | process_cpu_seconds_total, process_resident_memory_bytes | Capacity planning |
| Error metrics | job_failures_total, dlq_messages_total | Reliability monitoring |
*Table 163.* 
**9.1.6.3 Alerting Rules**
Prometheus alerting rules trigger notifications when thresholds are exceeded:
| **Alert** | **Condition** | **Severity** |
|:-:|:-:|:-:|
| HighQueueDepth | Queue messages > 50 for 5 minutes | Warning |
| CriticalQueueDepth | Queue messages > 100 for 5 minutes | Critical |
| ServiceDown | Service health check failed for 2 minutes | Critical |
| HighErrorRate | Error rate > 5% over 10 minutes | Warning |
| DLQMessages | Any message in dead letter queue | Warning |
| HighProcessingTime | Job duration > 20 minutes | Warning |
| DatabaseConnectionsExhausted | Available connections < 2 | Critical |
| StorageSpaceLow | MinIO utilization > 80% | Warning |
*Table 164.* 
Alerts are routed to the operations team through configured notification channels, enabling prompt response to emerging issues.
**9.1.6.4 Dashboards**
Pre-configured Grafana dashboards provide operational visibility:
| **Dashboard** | **Purpose** |
|:-:|:-:|
| Pipeline Overview | End-to-end job flow, active jobs, completion rates |
| Service Health | Per-service CPU, memory, request rates, error rates |
| Queue Monitoring | Queue depths, consumer counts, message rates |
| Storage Metrics | Phase utilization, file operations, capacity trends |
| Database Performance | Query latency, connection usage, transaction rates |
*Table 165.* 
These dashboards support both real-time monitoring during operations and historical analysis for capacity planning.
**9.1.7 Design Rationale**
The performance and reliability design reflects several architectural decisions aligned with SADN's operational requirements:
**Asynchronous processing** was chosen over synchronous request-response patterns because anonymization operations are computationally intensive and variable in duration. This approach ensures API responsiveness while allowing pipeline stages to process at their natural pace.
**Event-driven choreography** enables fault isolation and independent scaling. Unlike orchestration patterns where a central controller coordinates all steps, choreography allows each service to operate autonomously, reducing single points of failure and simplifying horizontal scaling.
**Prometheus-based monitoring** provides a standardized, well-supported observability stack that integrates seamlessly with containerized microservices. The pull-based model simplifies service configuration and ensures consistent metrics collection across all components.
**Conservative retry limits** (3 attempts) balance recovery from transient failures against the risk of repeatedly processing problematic data. Jobs that cannot complete after retries require human investigation, which is appropriate for a compliance-critical system.
**Separate dead letter queues per service** enable targeted troubleshooting and prevent failed messages in one pipeline stage from affecting visibility into problems elsewhere.
These design choices collectively ensure that SADN maintains reliable, predictable performance while providing operators with the visibility and control necessary to manage a compliance-critical data processing platform.
### 9.2 Security Feature
The SADN platform incorporates a multi-layered security model designed to ensure confidentiality, integrity, and availability of all datasets throughout the anonymization pipeline.  The following security features represent the mandatory controls implemented across the system to comply with PDPL, NCA ECC-2, NDMO, and MOH IS0303.
**1\. Data Confidentiality Controls**
1.1 Encryption at Rest
* All files stored in MinIO are encrypted using AES-256.
* PostgreSQL storage uses disk-level encryption.
* Master encryption keys are securely stored and rotated inside HashiCorp Vault.

⠀1.2 Encryption in Transit
* All inter-service communication uses TLS 1.3.
* Federation Gateway uses mutual TLS (mTLS) for cross-institution communication.

⠀1.3 Access Control & RBAC
* Every microservice operates using least-privilege roles.
* Dataset access strictly depends on storage phase (intake, staging, safe, quarantine).
* Only authorized analysts can access the *safe* zone.

⠀**2. Data Integrity Controls**
2.1 Immutable Audit Logs
* All events are logged in an append-only structure.
* Every event is cryptographically linked using a Merkle Chain to ensure tamper-evidence.
* No UPDATE/DELETE operations are allowed on audit logs.

⠀2.2 Checksum Validation
* Each uploaded file is validated using SHA-256 checksums.
* Storage Service performs integrity checks before processing.

⠀2.3 Failure-resistant Message Queues
* RabbitMQ guarantees persistence and prevents message loss via:
  * durable queues
  * publisher confirmations
  * consumer acknowledgments
  * dead letter queues (DLQ)

⠀**3. Data Availability Controls**
3.1 Fault Isolation using Microservices
* Each service runs independently to prevent system-wide failures.
* A failing service affects only its own queue, not the entire pipeline.

⠀3.2 Automatic Job Recovery
* Failed jobs are routed to DLQ and can be retried safely.
* Orchestrator manages job cancellation and retry logic.

⠀3.3 Backup & Retention
* Daily MinIO snapshots are taken.
* Archived datasets stored for minimum 7 years (PDPL requirement).

⠀**4. Privacy Protection Features**
4.1 Automated Privacy Metrics
* Sadn enforces:
  * k-anonymity ≥ 5
  * l-diversity ≥ 2
  * t-closeness ≤ 0.1

⠀4.2 Multi-stage Masking
Seven anonymization techniques ensure irreversible removal of personal identifiers:
1 Generalization
2 Suppression
3 Pseudonymization
4 Tokenization
5 Format-Preserving Encryption (FPE)
6 Perturbation
7 Redaction

⠀4.3 No Raw Data Exposure
* Only masked datasets are ever processed by Validation Service.
* Storage phase isolation prevents unauthorized access to sensitive files.

⠀**5. Secure Development & Deployment Controls**
5.1 Container Isolation
* Each microservice runs inside an isolated Docker container.
* Inter-container traffic is restricted to SADN’s internal network.

⠀5.2 Secret Management
* All secrets (DB creds, RabbitMQ creds, encryption keys) stored in Vault.
* Dynamic secrets used where applicable to reduce key exposure.

⠀5.3 Secure API Design
* Gateway enforces JWT auth and access tokens.
* Orchestrator exposes only required endpoints.

⠀**6. Monitoring & Compliance Controls**
6.1 Security Monitoring
* Logs are collected per service and aggregated for analysis.
* Alerts generated for anomalous failures or suspicious activities.

⠀6.2 Regulatory Compliance
Security features directly satisfy:
* PDPL Articles (Data Minimization, Lawful Processing, Security Controls)
* NDMO Data Sharing & Privacy Regulations
* NCA Essential Cybersecurity Controls (ECC-2)
* MOH IS0303 Health Data Rules

⠀6.3 Complete Traceability
All job actions are fully traceable end-to-end through:
* Audit logs
* Storage lifecycle
* Validation metrics
* Orchestrator events

⠀9.3 Monitoring & Logging
**9.3.1 Monitoring Overview**
The monitoring subsystem provides continuous visibility into the operational health, performance, and behavior of all SADN microservices. Its purpose is to ensure that system components remain reliable, responsive, and compliant with expected performance baselines. Monitoring focuses on capturing real-time service status, resource usage, queue backlogs, storage activity, and API responsiveness across the distributed architecture.
The monitoring layer aggregates signals from all microservices-including the Orchestrator, NLP, Masking, Validation, Storage, Federation Gateway, and Audit Service-and exposes unified dashboards for operators. These signals support proactive detection of failures, performance degradation, bottlenecks, or abnormal activity within the anonymization pipeline. By continuously assessing both infrastructure-level and application-level metrics, the monitoring subsystem helps maintain system stability and enables timely intervention before issues affect end users or compromise compliance requirements.
**9.3.2 Logging Framework**
The logging framework defines how system components generate, format, and store operational logs throughout the SADN microservices architecture. All services produce structured, timestamped logs that capture key events such as request handling, background task execution, queue processing activities, and internal state transitions.
Logs are emitted in a consistent machine-parsable format (e.g., JSON) to support automated analysis and aggregation across services. Each microservice writes logs to its container stdout/stderr streams, enabling unified collection by centralized log processors. Logged information includes service identifiers, correlation IDs, event categories, severity levels, and context-specific metadata. This structured approach ensures traceability, simplifies debugging, and supports compliance-oriented record-keeping without exposing sensitive dataset content.
**9.3.3 Metrics Collection**
The metrics collection subsystem gathers quantitative performance indicators from all SADN microservices and infrastructure components. These metrics provide insight into system throughput, resource consumption, and operational stability across the anonymization pipeline.
Each service exposes standardized metrics endpoints or emits internal counters that track key parameters such as request rates, queue consumption speed, processing durations, memory and CPU usage, worker concurrency, file transfer performance, and background task execution times. Metrics are periodically scraped or pushed into a centralized monitoring backend, enabling operators to visualize trends, identify bottlenecks, and enforce performance baselines.
This collection framework ensures that administrators can monitor service-level health, detect early performance regressions, and maintain predictable system behavior under varying workloads.
**9.3.4 Distributed Tracing**
The distributed tracing subsystem captures end-to-end execution paths across the SADN microservices, enabling operators to understand how a job flows through the anonymization pipeline. Tracing assigns correlation identifiers to incoming requests or queue messages and propagates them across all service boundaries-including NLP detection, masking transformations, validation operations, storage transitions, and audit logging.
Each microservice emits trace spans that record processing durations, sub-operation details, and service-to-service interactions. These spans are aggregated into a unified trace view, allowing operators to identify latency hotspots, failed steps, unexpected retries, or slow external dependencies. Distributed tracing provides deep visibility into pipeline behavior, supporting both debugging and optimization in a complex event-driven architecture.
**9.3.5 Log Retention & Rotation**
The log retention and rotation policy ensures that operational logs generated across the SADN microservices are stored efficiently, preserved for the required duration, and pruned before they accumulate excessive disk usage. Each service writes logs to its container output streams, which are automatically rotated based on size or time intervals to prevent uncontrolled growth.
Retention periods are defined per environment to balance compliance needs and storage constraints. Shorter retention windows may be used in development, while production environments maintain longer windows aligned with institutional policies. Old log segments are archived or removed according to configured rotation rules, ensuring that system observability is maintained without compromising storage availability or performance.
**9.3.6 Alerting & Thresholds**
The alerting subsystem defines the conditions under which automated notifications are triggered to inform operators about abnormal system behavior or emerging issues. Alerts are bound to predefined thresholds derived from performance baselines, architectural expectations, and service-level requirements.
Thresholds may be applied to key indicators such as queue backlog growth, prolonged processing durations, increased error rates, resource exhaustion, service unresponsiveness, or failed health checks. When a threshold is exceeded, the monitoring system dispatches alerts through configured channels (e.g., email, dashboard notifications, or incident management tools), allowing operators to respond promptly. This proactive approach ensures timely intervention to maintain pipeline stability, data integrity, and compliance standards.
**9.3.7 Monitoring Integration Points**
Monitoring integration points define how observability components connect with SADN microservices and infrastructure systems to collect logs, metrics, traces, and health signals. Each microservice exposes standardized interfaces-such as health endpoints, metrics endpoints, and structured logs-that are consumed by centralized monitoring tools.
Integration points include internal REST endpoints for service health checks, RabbitMQ queue statistics for pipeline monitoring, MinIO storage metrics, PostgreSQL performance indicators, and application-generated metrics from individual services. These connections ensure unified visibility across the distributed architecture, enabling the monitoring subsystem to aggregate data from diverse sources into a cohesive operational perspective.
**9.3.8 Design Rationale**
The monitoring and logging design is structured to provide reliable, actionable observability across a distributed, event-driven microservices architecture. By separating monitoring concerns into health checks, metrics, logs, traces, and alerting, the system ensures that each operational dimension is captured independently and analyzed cohesively through centralized tooling.
This modular approach supports rapid diagnosis of failures, early detection of performance regressions, and consistent visibility into service behavior across environments. The rationale prioritizes low-overhead instrumentation, standardized formats, and compatibility with industry-standard monitoring stacks to simplify deployment, reduce operational complexity, and provide long-term maintainability.


### 9 Requirements Traceability Matrix

⠀
### 10.1 Requirements Traceability Matrix (RTM)
The Requirements Traceability Matrix ensures that every functional and non-functional requirement in SADN is fully mapped to its corresponding design elements, responsible components, and verification mechanisms.
 	 This matrix guarantees complete coverage across all phases of the anonymization pipeline and ensures alignment with PDPL, NDMO, NCA ECC-2, and MOH IS0303 requirements.

**10.1.1 RTM Table**

| **Req ID** | **Requirement Description** | **Mapped Design Section** | **Responsible Component** | **Verification Method** |
|---|---|---|---|---|
| FR-ING-01 | System must accept dataset uploads | 1.1, 2.1, 7.1 | Orchestrator | API Testing |
| FR-ING-02 | Intake validation must check integrity, malware, and format | 7.5, 8.8 Storage | Storage Service | Automated Tests, ClamAV Logs |
| FR-NLP-01 | Detect PII/PHI in Arabic & English | 7.2, 8.8 NLP | NLP Service | NLP Unit Tests, Regex Matching |
| FR-NLP-02 | Identify Saudi-specific identifiers (NID, IBAN, mobile) | 7.2, 8.x | NLP Service | Regex/Pattern Validation |
| FR-MASK-01 | Apply seven masking techniques | 7.3, 8.8 Masking | Masking Service | Transformation Logs |
| FR-MASK-02 | Ensure deterministic pseudonymization | 7.3, 5.3 | Masking Service | Hash Consistency Checks |
| FR-VAL-01 | Compute k-anonymity | 7.4, 8.8 Validation | Validation Service | Metric Calculation Tests |
| FR-VAL-02 | Compute l-diversity | 7.4, 8.8 Validation | Validation Service | Unit Tests |
| FR-VAL-03 | Compute t-closeness | 7.4, 8.8 Validation | Validation Service | EMD Distribution Tests |
| FR-VAL-04 | Enforce privacy thresholds | 7.4, 8.8 | Validation Service | PASS/FAIL Outcome Review |
| FR-VAL-05 | Produce privacy risk score | 7.4 | Validation Service | Threshold Verification |
| FR-STOR-01 | Manage storage lifecycle (intake → safe → archive) | 7.5, 8.7 | Storage Service | MinIO Logs & Phase Transitions |
| FR-STOR-02 | Support atomic phase transitions | 7.5, 8.7 | Storage Service | Move Operation Validation |
| FR-AUD-01 | Record all system events | 7.6, 8.3 Audit | Audit Service | Audit Log Check |
| FR-AUD-02 | Use Merkle-chained integrity | 7.6, 8.3 Audit | Audit Service | Hash Chain Verification |
| FR-FED-01 | Enable secure inter-institution data sharing | 7.7, 8.3 Federation | Federation Gateway | mTLS Testing |
| FR-FED-02 | Enforce external access controls | 7.7 | Federation Gateway | Access Control Validation |
| NFR-SEC-01 | Encrypt data at rest using AES-256 | 9.2 | MinIO + Vault | Encryption Config Review |
| NFR-SEC-02 | Encrypt data in transit using TLS 1.3 | 9.2 | All Services | Certificate Testing |
| NFR-SEC-03 | RBAC + Least Privilege | 9.2 | All Components | Access Control Audit |
| NFR-SEC-04 | No raw PII in logs | 9.2 | NLP, Masking, Validation | Log Review |
| NFR-REL-01 | Ensure message persistence & retries | 3.2, 7.x | RabbitMQ | DLQ Review |
| NFR-PERF-01 | System should process datasets efficiently | 9.1 | All Processing Services | Benchmark Reports |
| NFR-COMP-01 | Comply with PDPL, NDMO, ECC-2 | 9.2, 3.x | Entire System | Compliance Checklist |
*Table 166.* 
RTM Table
**10.1.2 RTM Coverage Summary**
**Coverage Across All Services**
This RTM ensures traceability between requirements and:
* Orchestrator
* NLP Service
* Masking Service
* Validation Service
* Storage Service
* Audit Service
* Federation Gateway

⠀ **Coverage Across All Layers**
The matrix covers:
* Functional requirements (FR)
* Non-functional requirements (NFR)
* Regulatory requirements
* Security requirements
* Performance & reliability requirements

⠀ **Ensures End-to-End Completeness**
Every requirement is mapped to:
* A design section
* A responsible component
* A verifiable test or validation method

⠀


#bear/welcome