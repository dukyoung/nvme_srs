NVM Express [®] NVM Command Set Specification, Revision 1.2


**1 Introduction**


**1.1** **Overview**


NVM Express [®] (NVMe [®] ) Base Specification defines an interface for a host to communicate with a nonvolatile memory subsystem (NVM subsystem) over a variety of memory-based transports and messagebased transports.


This document defines a specific NVMe I/O Command Set, the NVM Command Set, which extends the
NVM Express Base Specification.


**1.2** **Scope**


Figure 1 shows the relationship of the NVM Express [®] NVM Command Set Specification to other
specifications within the NVMe Family of Specifications.


**Figure 1: NVMe Family of Specifications**


This specification supplements the NVM Express Base Specification. This specification defines additional
data structures, features, log pages, commands, and status values. This specification also defines
extensions to existing data structures, features, log pages, commands, and status values. This specification
defines requirements and behaviors that are specific to the NVM Command Set. Functionality that is
applicable generally to NVMe or that is applicable across multiple I/O Command Sets is defined in the NVM
Express Base Specification.


If a conflict arises among requirements defined in different specifications, then a lower-numbered
specification in the following list shall take precedence over a higher-numbered specification:


1. Non-NVMe specifications
2. NVM Express Base Specification
3. NVM Express Transport specifications
4. NVM Express I/O Command Set specifications
5. NVM Express Management Interface Specification
6. NVM Express Boot Specification


8


NVM Express [®] NVM Command Set Specification, Revision 1.2


**1.3** **Conventions**


This specification conforms to the Conventions section, Keywords section, and Byte, Word, and Dword
Relationships section of the NVM Express Base Specification.


**1.4** **Definitions**


**Definitions from the NVM Express Base Specification**


This specification uses the definitions in the NVM Express Base Specification.


**Definitions in the NVM Express Base Specification specified in the NVM Command set**


The following terms used in this specification are defined in each NVM Express I/O Command Set
specification.


**1.4.2.1** **Endurance Group Host Read Command**


The Compare command, Copy command, Read command, and Verify command.


**1.4.2.2** **Format Index**


A value used to index into the LBA Formats list (refer to Figure 114) and the Extended LBA Formats list
(refer to Figure 118).


**1.4.2.3** **Identify Controller data structures**


All controller data structures that are able to be retrieved via the Identify command for the NVM Command
Set:


  - the Identify Controller data structure (refer to the NVM Express Base Specification and section
4.1.5.2); and

  - the I/O Command Set specific Identify Controller data structure for the NVM Command Set (refer
to section 4.1.5.4).


**1.4.2.4** **Identify Namespace data structures**


All namespace data structures that are able to be retrieved via the Identify command for the NVM Command
Set:


  - the I/O Command Set Independent Identify Namespace data structure (refer to the NVM Express
Base Specification);

  - the Identify Namespace data structure (refer to section 4.1.5.1); and

  - the I/O Command Set specific Identify Namespace data structure for the NVM Command Set (refer
to section 4.1.5.3).


**1.4.2.5** **logical block data size**


The size in bytes of a logical block, excluding metadata, if any. The size is calculated using the following
formula:


2 ^ DataExponent


Where:


  - DataExponent is the value in the LBA Data Size field in the NVM Command Set specific LBA
Format data structure (refer to Figure 116).


9


NVM Express [®] NVM Command Set Specification, Revision 1.2


**1.4.2.6** **logical block size**


The size in bytes of a logical block, including metadata size. The size is calculated using the following
formula:


Logical block data size + MetadataBytes


where:


  - logical block data size is defined in section 1.4.2.5.

  - MetadataBytes is the value in the Metadata Size field in the NVM Command Set specific LBA
Format data structure (refer to Figure 116).


**1.4.2.7** **SMART Data Units Read Command**


The Compare command, Read command, and Verify command.


**1.4.2.8** **SMART Host Read Command**


The Compare command, Copy command, and Read command.


**1.4.2.9** **User Data Format**


The layout of the data on the NVM media as described by the LBA Format of the namespace.


**1.4.2.10 User Data Out Command**


The Copy command and Write command.


**Definitions specific to the NVM Command Set**


This section defines terms that are specific to this specification.


**1.4.3.1** **extended LBA**


An extended LBA is a larger LBA that is created when metadata associated with the LBA is transferred
contiguously with the LBA data. Refer to Figure 145.


**1.4.3.2** **LBA range**


A collection of contiguous logical blocks specified by a starting LBA and number of logical blocks.


**1.4.3.3** **logical block**


The smallest addressable data unit for Read and Write commands.


**1.4.3.4** **logical block address (LBA)**


The address of a logical block, referred to commonly as LBA.


10


NVM Express [®] NVM Command Set Specification, Revision 1.2


**1.5** **Acronyms**


**Figure 2: Acronym definitions**

|Acronym|Definition|
|---|---|
|LBA|logical block address|



**1.6** **References**


[NVM Express Base Specification, Revision 2.3. Available from https://www.nvmexpress.org.](https://www.nvmexpress.org/)


NVM Express Management Interface Specification, Revision 2.1. Available from
[https://www.nvmexpress.org.](https://www.nvmexpress.org/)


NVM Express Subsystem Local Memory Command Set Specification, Revision 1.2. Available from
[https://www.nvmexpress.org.](https://www.nvmexpress.org/)


NVM Express Zoned Namespace Command Set Specification, Revision 1.4. Available from
[https://www.nvmexpress.org.](https://www.nvmexpress.org/)


SNIA [®] Solid State Storage (SSS) Performance Test Specification (PTS), Version 2.0.2, October 1, 2020.
[Available from https://www.snia.org.](https://www.snia.org/)


**References Under Development**


None


**Bibliography**


[INCITS 506-2021 SCSI Block Commands - 4 (SBC-4). Available from https://webstore.ansi.org.](https://webstore.ansi.org/)


[INCITS 558-2021 ATA Command Set - 5 (ACS-5). Available from https://webstore.ansi.org.](https://webstore.ansi.org/)


TCG Storage Security Subsystem Class: Key Per IO Version 1.00 Revision 1.41. Available from
[https://trustedcomputinggroup.org.](https://trustedcomputinggroup.org/)


11


