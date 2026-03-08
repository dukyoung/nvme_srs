**1 Introduction**


**1.1** **Overview**


The NVM Express [®] (NVMe [®] ) interface allows host software to communicate with a non-volatile memory
subsystem (NVM subsystem). This interface is optimized for all storage solutions, attached using a variety
of transports including PCI Express [®], Ethernet, InfiniBand [TM], and Fibre Channel. The mapping of
extensions defined in this document to a specific NVMe Transport are defined in an NVMe Transport
binding specification. The NVMe Transport binding specification for Fibre Channel is defined in INCITS 556
Fibre Channel – Non-Volatile Memory Express - 2 (FC-NVMe-2).


[For an overview of changes from revision 2.1 to revision 2.2, refer to https://nvmexpress.org/changes for a](https://nvmexpress.org/changes)
document that describes the new features, including mandatory requirements for a controller to comply with
revision 2.2.


**NVM Express** **[®]** **Specification Family**


Figure 1 shows the relationship of the NVM Express specifications to each other within the NVMe [®] family
of specifications.


**Figure 1: NVMe Family of Specifications**





The NVM Express specification family structure shown in Figure 1 is intended to show the applicability of
NVM Express specifications to each other, not a hierarchy, protocol stack, or system architecture.


The NVM Express Base Specification (i.e., this specification) defines a protocol for host software to
communicate with an NVM subsystem over a variety of memory-based transports and message-based
transports.


The NVM Express Management Interface (NVMe-MI) Specification defines an optional management
interface for all NVM Express Subsystems.


NVM Express I/O Command Set specifications define data structures, features, log pages, commands, and
status values that extend the NVM Express Base Specification.


NVM Express Transport specifications define the binding of the NVMe protocol including controller
properties to a specific transport.


The NVM Express Boot Specification defines constructs and guidelines for booting from NVM Express
interfaces.


1


NVM Express [®] Base Specification, Revision 2.2


**1.2** **Scope**


This specification defines a set of properties and commands that comprise the interface required for
communication with a controller in an NVM subsystem. These properties are to be implemented by an
instance of a controller using a specific NVMe Transport. This specification also defines common aspects
of the NVMe I/O Command Sets that may be supported by a controller.


There are three types of controllers with different capabilities (refer to section 3.1.3):


a) I/O controllers;
b) Discovery controllers; and
c) Administrative controllers.


In this document the generic term controller is often used instead of enumerating specific controller types
when applicable controller types may be determined from the context.


**1.3** **Outside of Scope**


The property interface and command set are specified apart from any usage model for the NVM, but rather
only specifies the communication interface to the NVM subsystem. Thus, this specification does not specify
whether the NVM subsystem is used as a solid-state drive, a main memory, a cache memory, a backup
memory, a redundant memory, etc. Specific usage models are outside the scope, optional, and not
licensed.


This specification defines requirements and behaviors that are implementation agnostic. The
implementation of these requirements and behaviors are outside the scope of this specification. For
example, an NVM subsystem that follows this specification may be implemented by an SSD that attaches
directly to a fabric, a device that translates between a fabric and a PCIe NVMe SSD, or software running
on a general-purpose server.


This interface is specified above any non-volatile media management, like wear leveling. Erases and other
management tasks for NVM technologies like NAND are abstracted.


This specification does not contain any information on caching algorithms or techniques.


The implementation or use of other published specifications referred to in this specification, even if required
for compliance with the specification, are outside the scope of this specification (e.g., PCI, PCI Express,
and PCI-X). This includes published specifications for fabrics and other technologies referred to by this
document or any NVMe Transport binding specification.


**1.4** **Conventions**


**Keywords**


Several keywords are used to differentiate between different levels of requirements.


**mandatory**


A keyword indicating items to be implemented as defined by this specification.


**may**


A keyword that indicates flexibility of choice with no implied preference.


**obsolete**


A keyword indicating functionality that was defined in a previous version of the NVM Express specification
and that has been removed from this specification.


2


NVM Express [®] Base Specification, Revision 2.2


**optional**


A keyword that describes features that are not required by this specification. However, if any optional
feature defined by the specification is implemented, the feature shall be implemented in the way defined by
the specification.


**R**


“R” is used as an abbreviation for “reserved” when the figure or table does not provide sufficient space for
the full word “reserved”.


**reserved**


A keyword referring to bits, bytes, words, fields, and opcode values that are set-aside for future
standardization. Their use and interpretation may be specified by future extensions to this or other
specifications. A reserved bit, byte, word, field, property, or register shall be cleared to 0h, or in accordance
with a future extension to this specification. The recipient of a command or a register write is not required
to check reserved bits, bytes, words, or fields. Receipt of reserved coded values in defined fields in
commands shall be reported as an error. Writing a reserved coded value into a controller property field
produces undefined results.


**shall**


A keyword indicating a mandatory requirement. Designers are required to implement all such mandatory
requirements to ensure interoperability with other products that conform to the specification.


**should**


A keyword indicating flexibility of choice with a strongly preferred alternative. Equivalent to the phrase “it is
recommended”.


**Numerical Descriptions**


A 0’s based value is a numbering scheme in which the number 0h represents a value of 1h, 1h represents
2h, 2h represents 3h, etc. In this numbering scheme, there is no method to represent the value of 0h.
Values in this specification are 1-based (i.e., the number 1h represents a value of 1h, 2h represents 2h,
etc.) unless otherwise specified.


Size values are shown in binary units or decimal units. The symbols used to represent these values are as
shown in Figure 2.


**Figure 2: Decimal and Binary Units**

|Decimal|Binary|
|---|---|
|**Symbol**<br>**Power**<br>**(base-10)**|**Symbol**<br>**Power**<br>**(base-2)**|
|kilo / k<br>103 <br>mega / M<br>106 <br>giga / G<br>109 <br>tera / T<br>1012 <br>peta / P<br>1015 <br>exa / E<br>1018 <br>zetta / Z<br>1021 <br>yotta / Y<br>1024|kibi / Ki<br>210 <br>mebi / Mi<br>220 <br>gibi / Gi<br>230 <br>tebi / Ti<br>240 <br>pebi / Pi<br>250 <br>exbi / Ei<br>260 <br>zebi / Zi<br>270 <br>yobi / Yi<br>280|



The ^ operator is used to denote the power to which that number, symbol, or expression is to be raised.


Some parameters are defined as an ASCII string. ASCII strings shall contain only code values (i.e., byte
values or octet values) 20h through 7Eh. For the string “Copyright”, the character “C” is the first byte, the
character “o” is the second byte, etc. ASCII strings are left justified. If padding is necessary, then the string


3


NVM Express [®] Base Specification, Revision 2.2


shall be padded with spaces (i.e., ASCII character 20h) to the right unless the string is specified as nullterminated.


Some parameters are defined as a UTF-8 string. UTF-8 strings shall contain only byte values (i.e., octet
values) 20h through 7Eh, 80h through BFh, and C2h through F4h (refer to sections 1 to 3 of RFC 3629).
For the string “Copyright”, the character “C” is the first byte, the character “o” is the second byte, etc. UTF-8
strings are left justified. If padding is necessary, then the string shall be padded with spaces (i.e., ASCII
character 20h, Unicode character U+0020) to the right unless the string is specified as null-terminated.


If padding is necessary for a field that contains a null-terminated string then the field should be padded with
nulls (i.e., ASCII character 00h, Unicode character U+0000) to the right of the string.


A hexadecimal ASCII string is an ASCII string that uses a subset of the code values: “0” to “9”, “A” to “F”
uppercase, and “a” to “f” lowercase.


Hexadecimal (i.e., base 16) numbers are written with a lower case “h” suffix (e.g., 0FFFh, 80h).
Hexadecimal numbers larger than eight digits are represented with an underscore character dividing each
group of eight digits (e.g., 1E_DEADBEEFh).


Binary (i.e., base 2) numbers are written with a lower case “b” suffix (e.g., 1001b, 10b). Binary numbers
larger than four digits are written with an underscore character dividing each group of four digits (e.g.,
1000_0101_0010b).


All other numbers are decimal (i.e., base 10). A decimal number is represented in this specification by any
sequence of digits consisting of only the Western-Arabic numerals 0 to 9 not immediately followed by a
lower-case b or a lower-case h (e.g., 175). This specification uses the following conventions for representing
decimal numbers:


a) the decimal separator (i.e., separating the integer and fractional portions of the number) is a period;
b) the thousands separator (i.e., separating groups of three decimal digits in a portion of the number)

is a comma;
c) the thousands separator is used in only the integer portion of a number and not the fractional portion

of a number; and
d) the decimal representation for a year does not include a comma (e.g., 2019 instead of 2,019).


4


NVM Express [®] Base Specification, Revision 2.2


**Byte, Word, and Dword Relationships**


Figure 3 illustrates the relationship between bytes, words and dwords. A qword (quadruple word) is a unit
of data that is four times the size of a word; it is not illustrated due to space constraints. Unless otherwise
specified, this specification specifies data in a little endian format.


**Figure 3: Byte, Word, and Dword Relationships**



0



0



0



0



0


0



0


0



byte


word


dword



1


1



1


1



1



1



1



1



0



0



0





3



3



2



2



2



2



2



2



2



2



2



2



1



1



1



1



1


1



1



1



0



0



0



0



0



0



0



0


0



**1.5** **Definitions**


**admin label**


An admin label is an administratively configured ASCII or UTF-8 string (refer to section 1.4.2) that may be
used to help identify specific NVMe entities (i.e., Hosts, NVM subsystems and namespaces). An admin
label is capable of describing the entity’s physical location, DNS name or other information.


**admin label ASCII**


An ASCII string. Refer to section 1.4.2 for ASCII string requirements. Refer to section 1.5.1 for admin label
usage.


5


NVM Express [®] Base Specification, Revision 2.2


**admin label UTF-8**


A UTF-8 string. Refer to section 1.4.2 for UTF-8 string requirements. Refer to section 1.5.1 for admin label
usage.


**Admin Queue**


The Admin Queue is the Submission Queue and Completion Queue with identifier 0. The Admin
Submission Queue and corresponding Admin Completion Queue are used to submit administrative
commands and receive completions for those administrative commands, respectively.


The Admin Submission Queue is uniquely associated with the Admin Completion Queue.


**Administrative controller**


A controller that exposes capabilities that allow a host to manage an NVM subsystem. An Administrative
controller does not implement I/O Queues, provide access to data or metadata associated with user data
on a non-volatile storage medium, or support namespaces attached to the Administrative controller (i.e.,
there are never any active NSIDs).


**allocated namespace**


A namespace that is associated with an allocated NSID.


**Allowed Host List**


A list of hosts (identified by Host NQN and Host Identifier) present in each Exported NVM Subsystem that
are granted access to the Exported NVM Subsystem via an Exported Port.


**arbitration burst**


The maximum number of commands that may be fetched by an arbitration mechanism at one time from a
Submission Queue.


**arbitration mechanism**


The method used to determine which Submission Queue is selected next to fetch commands for execution
by the controller. Refer to section 3.4.4.


**association**


An exclusive communication relationship between a particular controller and a particular host that
encompasses the Admin Queue and all I/O Queues of that controller.


**audit**


The process of accessing media to determine correct operation of a sanitize operation. Refer to section
8.1.24 and to ISO/IEC 27040.


**authentication commands**


Used to refer to Fabrics Authentication Send or Authentication Receive commands.


**cache**


A data storage area used by the NVM subsystem, that is not accessible to a host, and that may contain a
subset of user data stored in the non-volatile storage media or may contain user data that is not committed
to non-volatile storage media.


**candidate command**


A candidate command is a submitted command which has been transferred into the controller and the
controller deems ready for processing.


6


NVM Express [®] Base Specification, Revision 2.2


**capsule**


An NVMe unit of information exchange used in NVMe over Fabrics. A capsule contains a command or
response and may optionally contain command/response data and SGLs.


**Centralized Discovery controller (CDC)**


A Discovery controller that reports discovery information registered by Direct Discovery controllers and
hosts.


**Channel**


A Channel represents a communication path between the controller and one or more Media Units in an
NVM subsystem.


**command completion**


A command is completed when the controller has completed processing the command, has updated status
information in the completion queue entry, and has posted the completion queue entry to the associated
Completion Queue.


**command submission**


For memory-based transport model (e.g., PCIe) implementations, a command is submitted when a
Submission Queue Tail Doorbell write has completed that moves the Submission Queue Tail Pointer value
past the Submission Queue slot in which the command was placed.


For message-based transport model (e.g., NVMe over Fabrics) implementations, a command is submitted
when a host adds a capsule to a Submission Queue.


**controller**


A controller is the interface between a host and an NVM subsystem. There are three types of controllers:


a) I/O controllers;
b) Discovery controllers; and
c) Administrative controllers.


A controller executes commands submitted by a host on a Submission Queue and posts a completion on
a Completion Queue. All controllers implement one Admin Submission Queue and one Admin Completion
Queue. Depending on the controller type, a controller may also implement one or more I/O Submission
Queues and I/O Completion Queues. When PCI Express is used as the transport, then a controller is a PCI
Express function.


**Controller Reset**


Host modification of the CC property that clears CC.EN from ‘1’ to ‘0’ (refer to section 3.7.2).


**Directive**


A method of information exchange between a host and either an NVM subsystem or a controller.
Information may be transmitted using the Directive Send and Directive Receive commands. A subset of I/O
commands may include a Directive Type field and a Directive Specific field to communicate more
information that is specific to the associated I/O command. Refer to section 8.1.8.


**Direct Discovery controller (DDC)**


A Discovery controller that is capable of registering discovery information with a Centralized Discovery
controller.


7


NVM Express [®] Base Specification, Revision 2.2


**Discovery controller**


A controller that exposes capabilities that allow a host to retrieve a Discovery Log Page. A Discovery
controller does not implement I/O Queues or provide access to a non-volatile storage medium. Refer to
section 3.1.3.3.


**discovery information**


Information about a host or NVM subsystem that is used for discovery (e.g., NVMe Transport address,
NQN, etc.).


**Discovery Service**


An NVM subsystem that supports Discovery controllers only. A Discovery Service shall not support a
controller that exposes namespaces.


**dispersed namespace**


A shared namespace that may be concurrently accessed by controllers in two or more NVM subsystems
(refer to section 8.1.9).


**dynamic controller**


The controller is allocated on demand with no state (e.g., Feature settings) preserved from prior
associations.


**Domain**


A domain is the smallest indivisible unit that shares state (e.g., power state, capacity information).


**embedded management controller**


An embedded management controller is a Management Controller (refer to the NVM Express Management
Interface Specification) that provides an external management interface (e.g., Redfish [®] ), typically
implemented via commands to the Management Endpoint.


**emulated controller**


An NVM Express controller that is defined in software. An emulated controller may or may not have an
underlying physical NVMe controller (e.g., physical PCIe function).


**Endurance Group**


A portion of non-volatile storage in the NVM subsystem whose endurance is managed as a group. Refer to
section 3.2.3.


**Entry Key**


A set of discovery information entry fields that allow for the unique identification of each discovery
information entry registered with the CDC or DDC. Refer to the Entry Key Type (EKTYPE) field.


**Exported Namespace**


A namespace in an Exported NVM Subsystem.


**Exported NVM Resources**


NVM resources created to enable remote access to physical NVM resources that includes:


a) Exported NVM Subsystems;
b) Exported Namespaces; and
c) Exported Ports.


8


NVM Express [®] Base Specification, Revision 2.2


**Exported NVM Subsystem**


A logical NVM subsystem that exports underlying NVM resources and that:


a) contains zero or more Exported Namespaces;
b) contains zero or more controllers;
c) contains zero or more Exported Ports; and
d) may contain an Allowed Host List.


**Exported Port**


A port used to export an NVMe subsystem over a specific fabrics transport and represented by an Exported
Port ID.


**Exported Port ID**


A port identifier used to specify an Exported Port.


**fabric (network fabric)**


A network topology in which nodes pass data to each other.


**Fabric Zoning**


A technique to specify access control configurations between hosts and NVM subsystems.


**firmware/boot partition image update command sequence**


The sequence of one or more Firmware Image Download commands that download a firmware image or a
boot partition image followed by a Firmware Commit command that commits that downloaded image to a
firmware slot or a boot partition.


**firmware slot**


A firmware slot is a location in a domain used to store a firmware image. The domain stores from one to
seven firmware images. Controllers in the same domain share the same firmware slots.


**host**


An entity that interfaces to an NVM subsystem through one or more controllers and submits commands to
Submission Queues and retrieves command completions from Completion Queues.


**host-accessible memory**


Memory that the host is able to access (e.g., host memory, Controller Memory Buffer (CMB), Persistent
Memory Region (PMR)).


**host management agent**


A host management agent is a part of the host that provides an external management interface (e.g.,
Redfish) to external managers, typically via Admin commands to the controller (refer to the NVM Express
Management Interface Specification).


**host memory**


Memory that may be read and written by both a host and a controller and that is not exposed by a controller
(i.e., Controller Memory Buffer or Persistent Memory Region). Host memory may be implemented inside or
outside a host (e.g., a memory region exposed by a device that is neither the host nor controller).


**idempotent command**


A command that produces the same end state in the NVM subsystem and returns the same results if that
command is resubmitted one or more times with no intervening commands. Refer to section 9.6.3.1.


9


NVM Express [®] Base Specification, Revision 2.2


**Identify Controller data structures**


All controller data structures that are able to be retrieved via the Identify command:

  - Identify Controller data structure (i.e., CNS 01h); and

  - each of the I/O Command Set specific Identify Controller data structure (i.e., CNS 06h).


**Identify Namespace data structures**


All namespace data structures that are able to be retrieved via the Identify command:

  - Identify Namespace data structures (i.e., CNS 00h, CNS 09h, and CNS 11h);

  - I/O Command Set Independent Identify Namespace data structures (i.e., CNS 08h and CNS 1Fh);
and

  - I/O Command Set specific Identify Namespace data structures (i.e., CNS 05h, CNS 0Ah, and CNS
1Bh).


**I/O command**


An I/O command is a command submitted to an I/O Submission Queue.


**I/O Completion Queue**


An I/O Completion Queue is a Completion Queue that is used to indicate command completions and is
associated with one or more I/O Submission Queues.


**I/O controller**


A controller that implements I/O queues and is intended to be used to access a non-volatile storage
medium.


**I/O Submission Queue**


An I/O Submission Queue is a Submission Queue that is used to submit I/O commands for execution by
the controller (e.g., Read command and Write command for the NVM Command Set).


**Media Unit**


A Media Unit represents a component of the underlying media in an NVM subsystem. Endurance Groups
are composed of Media Units.


**memory-based controller**


A controller that supports a memory-based transport model (e.g., a PCIe implementation).


**message-based controller**


A controller that supports a message-based transport model (e.g., a Fabrics implementation).


**metadata**


Metadata is contextual information related to formatted user data (e.g., a particular LBA of data as defined
in the NVM Command Set Specification). The host may include metadata to be stored by the NVM
subsystem if storage space is provided by the controller. Refer to the applicable I/O Command Set
specification for details.


**MMC**


A Migration Management Controller. Refer to section 8.1.12.


**MMH**


A Migration Management Host. Refer to section 8.1.12.


10


NVM Express [®] Base Specification, Revision 2.2


**MMHD**


A Migration Management Host associated with a Migration Management Controller in a Destination NVM
Subsystem. Refer to section 8.1.12.


**MMHS**


A Migration Management Host associated with a Migration Management Controller in a Source NVM
Subsystem. Refer to section 8.1.12.


**namespace**


A set of resources that may be directly accessed by a host (e.g., formatted non-volatile storage).


**namespace ID (NSID)**


An identifier used by a controller to provide access to a namespace or the name of the field in the SQE that
contains the namespace identifier (refer to Figure 92). Refer to section 3.2.1 for the definitions of valid
NSID, invalid NSID, active NSID, inactive NSID, allocated NSID, and unallocated NSID.


**NVM**


NVM is an acronym for non-volatile memory.


**NVM Set**


A portion of NVM from an Endurance Group. Refer to section 3.2.2.


**NVM subsystem**


An NVM subsystem includes one or more domains, one or more controllers, zero or more namespaces,
and one or more ports. An NVM subsystem may include a non-volatile storage medium and an interface
between the controller(s) in the NVM subsystem and non-volatile storage medium.


**NVM subsystem port**


An NVMe over Fabrics protocol interface between an NVM subsystem and a fabric. An NVM subsystem
port is a collection of one or more physical fabric interfaces that together act as a single interface.


**NVMe over Fabrics**


An implementation of the NVM Express interface that complies with either the message-only transport
model or the message/memory transport model (refer to Figure 4 and section 2.2).


**NVMe Transport**


A protocol layer that provides reliable delivery of data, commands, and responses between a host and an
NVM subsystem. The NVMe Transport layer is layered on top of the fabric. It is independent of the fabric
physical interconnect and low-level fabric protocol layers.


**NVMe Transport binding specification**


A specification of reliable delivery of data, commands, and responses between a host and an NVM
subsystem for an NVMe Transport. The binding may exclude or restrict functionality based on the NVMe
Transport’s capabilities.


**participating NVM subsystem**


An NVM subsystem that participates in (i.e., contains controllers that provide access to) a dispersed
namespace.


11


NVM Express [®] Base Specification, Revision 2.2


**physical fabric interface (physical ports)**


A physical connection between an NVM subsystem and a fabric.


**Placement Handle**


A namespace scoped handle that maps to an Endurance Group scoped Reclaim Unit Handle which
references a Reclaim Unit in each Reclaim Group.


**Placement Identifier**


A data structure that specifies a Reclaim Group Identifier and a Placement Handle that references a
Reclaim Unit. Refer to Figure 283 and Figure 284.


**Port ID**


An identifier that is associated with an NVM subsystem port. Refer to section 2.2.2.


**Ports List**


A list of ports that may be used to export an NVM subsystem. Entries in the Ports List are in the format
specified by Underlying Fabrics Transport Entry data structure (refer to Figure 337).


**Power Loss Acknowledge (PLA)**


The transport-specific variable that is used by the controller to inform the host of the controller’s current
Power Loss Signaling processing (refer to section 8.2.5).


**Power Loss Notification (PLN)**


The transport-specific variable that is used to inform the controller that a main power loss event is expected
to occur (refer to section 8.2.5).


**primary controller**


An NVM Express controller that supports the Virtualization Management command. An NVM subsystem
may contain multiple primary controllers. Secondary controller(s) in an NVM subsystem depend on a
primary controller for dynamic resource management (refer to section 8.2.6).


A PCI Express SR-IOV Physical Function that supports the NVM Express interface and the Virtualization
Enhancements capability is an example of a primary controller (refer to section 8.2.6.4).


**private namespace**


A namespace that is only able to be attached to one controller at a time. Refer to the Namespace Multipath I/O and Namespace Sharing Capabilities (NMIC) field in Figure 320.


**property**


The generalization of memory mapped controller registers defined for NVMe over PCIe. Properties are
used to configure low level controller attributes and obtain low level controller status. Refer to section 3.1.4.


**Reclaim Group (RG)**


An entity that contains one or more Reclaim Units. Refer to section 3.2.4.


**Reclaim Unit (RU)**


A logical representation of non-volatile storage within a Reclaim Group that is able to be physically erased
by the controller without disturbing any other Reclaim Units. Refer to section 3.2.4.


**Reclaim Unit Handle (RUH)**


A controller resource that references a Reclaim Unit in each Reclaim Group. Refer to section 3.2.4.


12


NVM Express [®] Base Specification, Revision 2.2


**rotational media**


Media that stores data on rotating platters (refer to section 8.1.23).


**Runtime D3 (Power Removed)**


In Runtime D3 (RTD3) main power is removed from the controller. Auxiliary power may or may not be
provided. For PCI Express, RTD3 is the D3cold power state (refer to section 8.1.17.4).


**sanitize operation**


Process by which all user data in the NVM subsystem is altered such that recovery of the previous user
data from any cache or the non-volatile storage media is infeasible for a given level of effort (refer to IEEE
2883™-2022).


**sanitization target**


The target of a sanitize operation (i.e., an NVM subsystem).


**secondary controller**


An NVM Express controller that depends on a primary controller in an NVM subsystem for management of
some controller resources (refer to section 8.2.6).


A PCI Express SR-IOV Virtual Function that supports the NVM Express interface and receives resources
from a primary controller is an example of a secondary controller (refer to section 8.2.6.4).


**shared namespace**


A namespace that may be attached to two or more controllers in an NVM subsystem concurrently. Refer to
the Namespace Multi-path I/O and Namespace Sharing Capabilities (NMIC) field in Figure 320.


**specified namespace**


The namespace that is associated with the value specified by the Namespace Identifier (NSID) field in a
command as defined by the Common Command Format (refer to Figure 92).


**spindown**


The process of changing a spindle from an operational power state to a non-operational power state, for
an Endurance Group that stores data on rotational media (refer to section 8.1.23).


**spinup**


The process of changing a spindle from a non-operational power state to an operational power state, for
an Endurance Group associated with rotational media (refer to section 8.1.23).


**static controller**


The controller is pre-existing with a specific Controller ID and its state (e.g., Feature settings) is preserved
from prior associations.


**Underlying Namespace**


A namespace (defined in section 1.5.62) accessible through physical or virtual functions in an Underlying
NVM Subsystem that may be used to associate with an Exported NVM Subsystem. Underlying
Namespaces are identified by the Underlying Namespace Entry data structure (refer to Figure 335).


**Underlying Namespace List**


A list of namespaces (refer to section 5.1.13.4.1) in all underlying NVM subsystems that may be used to
create an Exported Namespace.


13


NVM Express [®] Base Specification, Revision 2.2


**Underlying NVM Subsystem**


Defined as NVM subsystem.


**Underlying Port**


A port through which an NVMe subsystem is attached to a transport (e.g., Ethernet, InfiniBand, Fibre
Channel) (refer to section 1.5.72).


**user data**


Data stored in a namespace that is composed of data that the host may store and later retrieve including
metadata if supported.


**1.6** **I/O Command Set specific definitions used in this specification**


The following terms used in this specification are defined in each I/O Command Set specification.


**Endurance Group Host Read Command**


An I/O Command Set specific command that results in the controller reading user data, but may or may not
return the data to the host.


**Format Index**


A value used to index into the I/O Command Set Specific Format table (i.e., the User Data Format number).


**SMART Data Units Read Command**


An I/O Command Set specific command that results in the controller reading user data, but may or may not
return the data to the host.


**SMART Host Read Command**


An I/O Command Set specific command that results in the controller reading user data, but may or may not
return the data to the host.


**User Data Format**


An I/O Command Set specific format that describes the layout of the data on the NVM media.


**User Data Out Command**


An I/O Command Set specific command that results in the controller writing user data, but may or may not
transfer user data from the host to the controller.


**1.7** **NVM Command Set specific definitions used in this specification**


The following terms used in this specification are defined in the NVM Command Set Specification. These
terms are used throughout the document as examples for a specific I/O Command Set.


**logical block**


The smallest addressable data unit for Read and Write commands.


**logical block address (LBA)**


The address of a logical block, referred to commonly as LBA.


**1.8** **References**


CNSA 1.0, “USE OF PUBLIC STANDARDS FOR SECURE INFORMATION SHARING”, CNSSP 15
ANNEX B “NSA-APPROVED COMMERCIAL NATIONAL SECURITY ALGORITHM (CNSA) SUITE”, 20
[October 2016. Available from https://www.cnss.gov/CNSS/issuances/Policies.cfm.](https://www.cnss.gov/CNSS/issuances/Policies.cfm)


14


NVM Express [®] Base Specification, Revision 2.2


[IEEE Std 2883™-2022, IEEE Standard for Sanitizing Storage. Available from https://standards.ieee.org.](https://standards.ieee.org/)


INCITS 502-2019, Information Technology – SCSI Primary Commands - 5 (SPC-5). Available from
[https://webstore.ansi.org.](https://webstore.ansi.org/)


INCITS 556-2020, Information Technology – Non-Volatile Memory Express - 2 (FC-NVMe-2). Available
[from https://webstore.ansi.org.](https://webstore.ansi.org/)


ISO 8601, Data elements and interchange formats – Information interchange – Representations of dates
[and times. Available from https://www.iso.org.](https://www.iso.org/)


ISO/IEC 27040:2024 Information technology – Security techniques – Storage security. Available from
[https://www.iso.org.](https://www.iso.org/)


JEDEC JESD218B-02: Solid State Drive (SSD) Requirements and Endurance Test Method standard.
[Available from https://www.jedec.org.](https://www.jedec.org/)


[NVM Express Boot Specification, Revision 1.2. Available from https://www.nvmexpress.org.](https://www.nvmexpress.org/)


NVM Express Management Interface Specification, Revision 2.0. Available from
[https://www.nvmexpress.org.](https://www.nvmexpress.org/)


[NVM Express NVM Command Set Specification, Revision 1.1. Available from https://www.nvmexpress.org.](https://www.nvmexpress.org/)


NVM Express Zoned Namespace Command Set Specification, Revision 1.3. Available from
[https://www.nvmexpress.org.](https://www.nvmexpress.org/)


NVM Express Key Value Command Set Specification, Revision 1.2. Available from
[https://www.nvmexpress.org.](https://www.nvmexpress.org/)


NVM Express NVMe over PCIe Transport Specification, Revision 1.2. Available from
[https://www.nvmexpress.org.](https://www.nvmexpress.org/)


[NVM Express RDMA Transport Specification, Revision 1.1. Available from https://www.nvmexpress.org.](https://www.nvmexpress.org/)


[NVM Express TCP Transport Specification, Revision 1.1. Available from https://www.nvmexpress.org.](https://www.nvmexpress.org/)


[PCI-SIG PCI Express® Base Specification, Revision 6.2. Available from https://www.pcisig.com.](https://www.pcisig.com/)


RFC 1952, P. Deutsch, “GZIP file format specification version 4.3”, May 1996. Available from
[https://www.rfc-editor.org/info/rfc1952.](https://www.rfc-editor.org/info/rfc1952)


RFC 1994, W. Simpson, “PPP Challenge Handshake Authentication Protocol (CHAP)”, August 1996.
[Available from https://www.rfc-editor.org/info/rfc1994.](https://www.rfc-editor.org/info/rfc1994)


RFC 2104, H. Krawczyk, M. Bellare, R. Canetti, “HMAC: Keyed-Hashing for Message Authentication”,
[February 1997. Available from https://www.rfc-editor.org/info/rfc2104.](https://www.rfc-editor.org/info/rfc2104)


RFC 2631, E. Rescorla, “Diffie-Hellman Key Agreement Method”, June 1999. Available from
[https://www.rfc-editor.org/info/rfc2631.](https://www.rfc-editor.org/info/rfc2631)


RFC 3629, F. Yergeau, “UTF-8, a transformation format of ISO 10646”, November 2003. Available from
[https://www.rfc-editor.org/info/rfc3629.](https://www.rfc-editor.org/info/rfc3629)


RFC 3986, T. Berners-Lee, R. Fielding, L. Masinter, “Uniform Resource Identifier (URI): Generic Syntax”,
[January 2005. Available from https://www.rfc-editor.org/info/rfc3986.](https://www.rfc-editor.org/info/rfc3986)


RFC 4086, D. Eastlake 3rd, J. Schiller, S. Crocker, “Randomness Requirements for Security”, June 2005.
[Available from https://www.rfc-editor.org/info/rfc4086.](https://www.rfc-editor.org/info/rfc4086)


RFC 4088, D. Black, K. McCloghrie, J. Schoenwaelder, “Uniform Resource Identifier (URI) Scheme for the
Simple Network Management Protocol (SNMP)”, June 2005. Available from [https://www.rfc-](https://www.rfc-editor.org/info/rfc4088)
[editor.org/info/rfc4088.](https://www.rfc-editor.org/info/rfc4088)


RFC 4301, S. Kent, K. Seo, “Security Architecture for the Internet Protocol”, December 2005. Available
[from https://www.rfc-editor.org/info/rfc4301.](https://www.rfc-editor.org/info/rfc4301)


15


NVM Express [®] Base Specification, Revision 2.2


RFC 4648, S. Josefsson, “The Base16, Base32, and Base64 Data Encodings”, October 2006. Available
[from https://www.rfc-editor.org/info/rfc4648.](https://www.rfc-editor.org/info/rfc4648)


RFC 5869, H. Krawczyk, P. Eronen, “HMAC-based Extract-and-Expand Key Derivation Function (HKDF)”,
[May 2010. Available from https://www.rfc-editor.org/info/rfc5869.](https://www.rfc-editor.org/info/rfc5869)


RFC 6234, D. Eastlake 3rd, and T. Hansen, "US Secure Hash Algorithms (SHA and SHA-based HMAC
[and HKDF)", May 2011. Available from https://www.rfc-editor.org/info/rfc6234.](https://www.rfc-editor.org/info/rfc6234)


RFC 6520, R. Seggelmann, M. Tuexen, M. Williams, "Transport Layer Security (TLS) and Datagram
Transport Layer Security (DTLS) Heartbeat Extension", February 2012. Available from [https://www.rfc-](https://www.rfc-editor.org/info/rfc6520)
[editor.org/info/rfc6520.](https://www.rfc-editor.org/info/rfc6520)


RFC 7296, C. Kaufman, P. Hoffman, Y. Nir, P. Eronen, T. Kivinen, “Internet Key Exchange Protocol Version
[2 (IKEv2)”, October 2014. Available from https://www.rfc-editor.org/info/rfc7296.](https://www.rfc-editor.org/info/rfc7296)


RFC 7919, D. Gillmor, “Negotiated Finite Field Diffie-Hellman Ephemeral Parameters for Transport Layer
[Security (TLS)”, August 2016. Available from https://www.rfc-editor.org/info/rfc7919.](https://www.rfc-editor.org/info/rfc7919)


RFC 8446, E. Rescorla, “The Transport Layer Security (TLS) Protocol Version 1.3”, August 2018. Available
[from https://www.rfc-editor.org/info/rfc8446.](https://www.rfc-editor.org/info/rfc8446)


RFC 9562, K. Davis, B. Peabody, and P. Leach, “Universally Unique Identifiers, May 2024”. Available from
[https://www.rfc-editor.org/info/rfc9562.](https://www.rfc-editor.org/info/rfc9562)


[UEFI Specification Version 2.10, August 2022. Available from https://uefi.org.](https://uefi.org/)


Advanced Configuration and Power Interface (ACPI) Specification, Version 6.5, August 2022. Available
[from https://www.uefi.org.](https://www.uefi.org/)


TCG Storage Architecture Core Specification, Version 2.01 Revision 1.00. Available from
[https://www.trustedcomputinggroup.org.](https://www.trustedcomputinggroup.org/)


TCG Storage Interface Interactions Specification (SIIS), Version 1.11 Revision 1.18. Available from
[https://www.trustedcomputinggroup.org.](https://www.trustedcomputinggroup.org/)


TCG Storage Security Subsystem Class: Key Per I/O Version 1.00 Revision 1.41. Available from
[https://trustedcomputinggroup.org.](https://trustedcomputinggroup.org/)


**1.9** **References Under Development**


None.


16


