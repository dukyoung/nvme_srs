NVM Express [®] Base Specification, Revision 2.2


**2 Theory of Operation**


The NVM Express scalable interface is designed to address the needs of storage systems that utilize PCI
Express based solid state drives or fabric connected devices. The interface provides optimized command
submission and completion paths. It includes support for parallel operation by supporting up to 65,535 I/O
Queues with up to 65,535 outstanding commands per I/O Queue. Additionally, support has been added for
many Enterprise capabilities like end-to-end data protection (compatible with SCSI Protection Information,
commonly known as T10 DIF, and SNIA DIX standards), enhanced error reporting, and virtualization.


The interface has the following key attributes:

  - Does not require uncacheable / MMIO register reads in the command submission or completion
path;

  - A maximum of one MMIO register write or one 64B message is necessary in the command
submission path;

  - Support for up to 65,535 I/O Queues, with each I/O Queue supporting up to 65,535 outstanding
commands;

  - Priority associated with each I/O Queue with well-defined arbitration mechanism;

  - All information to complete a 4 KiB read request is included in the 64B command itself, ensuring
efficient small I/O operation;

  - Efficient and streamlined command set;

  - Support for MSI/MSI-X and interrupt aggregation;

  - Support for multiple namespaces;

  - Efficient support for I/O virtualization architectures like SR-IOV;

  - Robust error reporting and management capabilities; and

  - Support for multi-path I/O and namespace sharing.


This specification defines a streamlined set of properties that are used to configure low level controller
attributes and obtain low level controller status. These properties have a transport specific mechanism for
defining access (e.g., memory-based transports use registers, whereas message-based transports use the
Property Get and Property Set commands). The following are examples of functionality defined in
properties:

  - Indication of controller capabilities;

  - Status for controller failures (command status is provided in a CQE);

  - Admin Queue configuration (I/O Queue configuration processed via Admin commands); and

  - Doorbell registers for a scalable number of Submission and Completion Queues.


There are two defined models for communication between the host and the NVM subsystem, a memorybased transport model and a message-based transport model. All NVM subsystems require the underlying
NVMe Transport to provide reliable NVMe command and data delivery. An NVMe Transport is an abstract
protocol layer independent of any physical interconnect properties. A taxonomy of NVMe Transports, along
with examples, is shown in Figure 4. An NVMe Transport may expose a memory-based transport model or
a message-based transport model. The message-based transport model has two subtypes: the messageonly transport model and the message/memory transport model.


A memory-based transport model is one in which commands, responses, and data are transferred between
a host and an NVM subsystem by performing explicit memory read and write operations (e.g., over PCIe).


A message-based transport model is one in which messages containing command capsules and response
capsules are sent between a host and an NVM subsystem (e.g., over a fabric). The two subtypes of
message-based transport models are differentiated by how data is sent between a host and an NVM
subsystem. In the message-only transport model data is only sent between a host and an NVM subsystem
using capsules or messages. The message/memory transport model uses a combination of messages and
explicit memory read and write operations to transfer command capsules, response capsules and data
between a host and an NVM subsystem. Data may optionally be included in command capsules and
response capsules. Both the message-only transport model and the message/memory transport model are


17


NVM Express [®] Base Specification, Revision 2.2


referenced as message-based transport models throughout this specification when the description is
applicable to both subtypes.


An NVM subsystem is made up of a single domain or multiple domains as described in section 3.2.5. An
NVM subsystem may optionally include a non-volatile storage medium, and an interface between the
controller(s) of the NVM subsystem and the non-volatile storage medium. Controllers expose this nonvolatile storage medium to hosts through namespaces. An NVM subsystem is not required to have the
same namespaces attached to all controllers. An NVM subsystem that supports a Discovery controller does
not support any other controller type. A Discovery Service is an NVM subsystem that supports Discovery
controllers only (refer to section 3.1).


**Figure 4: Taxonomy of Transport Models**


**NVMe Transport Models**



**Message / Memory**
Commands/Responses use Capsules

Data may use
Capsules or Shared Memory


**Example Transports**

RDMA
(InfiniBand, RoCE, iWARP)



**Memory**
Commands/Responses & Data

use Shared Memory


_**Example Transport**_

PCI Express



**Message**
Commands/Responses use Capsules

Data may use Capsules or Messages


_**Example Transports**_

Fibre Channel

TCP



The capabilities and settings that apply to an NVM Express controller are indicated in the Controller
Capabilities (CAP) property and the Identify Controller data structure (refer to Figure 313).


A namespace is a set of resources (e.g., formatted non-volatile storage) that may be accessed by a host.
A namespace has an associated namespace identifier that a host uses to access that namespace. The set
of resources may consist of non-volatile storage and/or other resources.


Associated with each namespace is an I/O Command Set that operates on that namespace. An NVM
Express controller may support multiple namespaces. Namespaces may be created and deleted using the
Namespace Management command and Capacity Management command. The Identify Namespace data
structures (refer to section 1.5.49) indicate capabilities and settings that are specific to a particular
namespace.


The NVM Express interface is based on a paired Submission and Completion Queue mechanism.
Commands are placed by host software into a Submission Queue. Completions are placed into the
associated Completion Queue by the controller.


There are three types of commands that are defined in NVM Express: Admin commands, I/O commands,
and Fabrics commands. Figure 5 shows these different command types.


18


NVM Express [®] Base Specification, Revision 2.2


**Figure 5: Types of NVMe Command Sets**

















An Admin Submission Queue and associated Completion Queue exist for the purpose of controller
management and control (e.g., creation and deletion of I/O Submission and Completion Queues, aborting
commands, etc.). Only commands that are part of the Admin Command Set or the Fabrics Command Set
may be submitted to the Admin Submission Queue.


An I/O Command Set is used with an I/O queue pair. This specification defines common I/O commands.
I/O Command Sets are defined in I/O Command Set specifications. The example I/O Command Sets shown
in Figure 5 are the NVM Command Set, the Key Value Command Set, and the Zoned Namespace
Command Set. Other I/O Command Sets include the Computational Programs Command Set and the SLM
Command Set.


The Fabrics Command Set is NVMe over Fabrics specific. Fabrics Command Set commands are used for
operations specific to NVMe over Fabrics including establishing a connection, NVMe in-band
authentication, and to get or set a property. All Fabrics commands may be submitted on the Admin
Submission Queue and some Fabrics commands may also be submitted on an I/O Submission Queue.
Unlike Admin and I/O commands, Fabrics commands are processed by a controller regardless of whether
the controller is enabled (i.e., regardless of the state of CC.EN).


**2.1** **Memory-Based Transport Model (PCIe)**


In the memory-based model, Submission and Completion Queues are allocated in memory.


Host software creates queues, up to the maximum supported by the controller. Typically, the number of
command queues created is based on the system configuration and anticipated workload. For example, on
a four core processor based system, there may be a queue pair per core to avoid locking and ensure data
structures are created in the appropriate processor core’s cache. Figure 6 provides a graphical
representation of the queue pair mechanism, showing a 1:1 mapping between Submission Queues and
Completion Queues. Figure 7 shows an example where multiple I/O Submission Queues utilize the same
I/O Completion Queue on Core B. Figure 6 and Figure 7 show that there is always a 1:1 mapping between
the Admin Submission Queue and Admin Completion Queue.


19


NVM Express [®] Base Specification, Revision 2.2


**Figure 6: Queue Pair Example, 1:1 Mapping**





















**Figure 7: Queue Pair Example,** _**n**_ **:1 Mapping**



























A Submission Queue (SQ) is a circular buffer with a fixed slot size that the host software uses to submit
commands for execution by the controller. The host software updates the appropriate SQ Tail doorbell
register when there are one to _n_ new commands to execute. The previous SQ Tail value is overwritten in
the controller when there is a new doorbell register write. The controller fetches SQ entries in order from
the Submission Queue and may execute those commands in any order.


Each submission queue entry is a command. Commands are 64 bytes in size. The physical memory
locations in memory to use for data transfers are specified using Physical Region Page (PRP) entries or
Scatter Gather Lists (SGL). Each command may include two PRP entries or one Scatter Gather List
segment. If more than two PRP entries are necessary to describe the data buffer, then a pointer to a PRP
List that describes a list of PRP entries is provided. If more than one SGL segment is necessary to describe
the data buffer, then the SGL segment provides a pointer to the next SGL segment.


A Completion Queue (CQ) is a circular buffer with a fixed slot size used to post status for completed
commands. A completed command is uniquely identified by a combination of the associated SQ identifier
and command identifier that is assigned by host software. In the memory-based transport model multiple
Submission Queues may be associated with a single Completion Queue. A configuration with a single
Completion Queue may be used where a single worker thread processes all command completions via one
Completion Queue even when those commands originated from multiple Submission Queues. The CQ
Head pointer is updated by host software after processing completion queue entries indicating the last free


20


NVM Express [®] Base Specification, Revision 2.2


CQ slot. A Phase Tag (P) bit is defined in the completion queue entry to indicate whether an entry has been
newly posted without the host consulting a register (refer to section 4.2.4). The Phase Tag bit enables the
host to determine whether entries are new or not.


**2.2** **Message-Based Transport Model (Fabrics)**


The message-based transport model used for NVMe over Fabrics has the following differences from the
memory-based transport model:

  - There is a one-to-one mapping between I/O Submission Queues and I/O Completion Queues.
NVMe over Fabrics does not support multiple I/O Submission Queues being mapped to a single
I/O Completion Queue;

  - NVMe over Fabrics does not define an interrupt mechanism that allows a controller to generate a
host interrupt. It is the responsibility of the host fabric interface (e.g., Host Bus Adapter) to generate
host interrupts;

  - NVMe over Fabrics uses different mechanisms for I/O Submission Queue and I/O Completion
Queue creation and deletion (refer to section 3.5);

  - NVMe over Fabrics does not support transferring metadata from a separate buffer (e.g., does not
support the Metadata Pointer field, refer to Figure 92);

  - NVMe over Fabrics does not support PRPs but requires use of SGLs for Admin, I/O, and Fabrics
commands. This differs from the memory-based transport model where SGLs are not supported
for Admin commands and are optional for I/O commands;

  - NVMe over Fabrics does not support Completion Queue flow control (refer to section 3.3.1.2.1).
This requires that the host ensures there are available Completion Queue slots before submitting
new commands; and

  - NVMe over Fabrics allows Submission Queue flow control to be disabled if the host and controller
agree to disable Submission Queue flow control. If Submission Queue flow control is disabled, the
host is required to ensure that there are available Submission Queue slots before submitting new
commands.


**Fabrics and Transports**


NVMe over Fabrics utilizes the protocol layering shown in Figure 8. This specification defines core aspects
of the architecture that are independent of the NVMe Transport. An NVMe Transport binding specification
is used to describe any NVMe Transport specific specialization as well as how the services required by the
NVMe interface are mapped onto the corresponding NVMe Transport. The native fabric communication
services and other functionality used by the NVMe interface and NVMe Transports (e.g., the Fabric Protocol
and Fabric Physical layers in Figure 8) are outside the scope of the NVMe family of specifications.


21


NVM Express [®] Base Specification, Revision 2.2


**Figure 8: NVMe over Fabrics Layering**



NVMe over Fabrics

(Message-based

Model)


NVMe Transport

Specification


NVMe Transport


Fabric













Fabric Physical
(e.g., Ethernet, InfiniBand, Fibre Channel)


**NVM Subsystem Ports for Fabrics**


An NVM subsystem presents a collection of one to (64Ki - 16) controllers which are used to access
namespaces. The controllers may be associated with hosts through one to 64Ki NVM subsystem ports.


An NVM subsystem port is a protocol interface between an NVM subsystem and a fabric. An NVM
subsystem port is a collection of one or more physical fabric interfaces that together act as a single protocol
interface. When link aggregation (e.g., Ethernet) is used, the physical ports for the group of aggregated
links constitute a single NVM subsystem port.


An NVM subsystem contains one or more NVM subsystem ports.


Each NVM subsystem port has a 16-bit port identifier (Port ID). An NVM subsystem port is identified by the
NVM Subsystem NVMe Qualified Name (NQN) and Port ID. The NVM subsystem ports of an NVM
subsystem may support different NVMe Transports. An NVM subsystem port may support multiple NVMe
Transports if more than one NVMe Transport binding specifications exist for the underlying fabric (e.g., an
NVM subsystem port identified by a Port ID may support both iWARP and RoCE). An NVM subsystem
implementation may bind specific controllers to specific NVM subsystem ports or allow the flexible allocation
of controllers between NVM subsystem ports, however, once connected, each specific controller is bound
to a single NVM subsystem port.


22


NVM Express [®] Base Specification, Revision 2.2


A controller is associated with exactly one host at a time. NVMe over Fabrics allows multiple hosts to
connect to different controllers in the NVM subsystem through the same NVM subsystem port. All other
aspects of NVMe over Fabrics multi-path I/O and namespace sharing (refer to section 2.4.1) are equivalent
to that of the memory-based transport model.


**Discovery Service**


NVMe over Fabrics defines a discovery mechanism that a host uses to determine the NVM subsystems
that expose namespaces that the host may access. The Discovery Service provides a host with the
following capabilities:

  - The ability to discover a list of NVM subsystems with namespaces that are accessible to the host;

  - The ability to discover multiple paths to an NVM subsystem;

  - The ability to discover controllers that are statically configured;

  - The optional ability to establish explicit persistent connections to the Discovery controller; and

  - The optional ability to receive Asynchronous Event Notifications from the Discovery controller.


A Discovery Service is an NVM subsystem that supports only Discovery controllers (refer to section 3.1.3.3),
and shall not support any other controller type.


The method that a host uses to obtain the information necessary to connect to the initial Discovery Service
is implementation specific. This information may be determined using a host configuration file, a hypervisor
or OS property, or some other mechanism.


**Capsules and Data Transfer**


A capsule is an NVMe unit of information exchange used in NVMe over Fabrics. A capsule may be classified
as a command capsule or a response capsule. A command capsule contains a command (formatted as a
submission queue entry) and may optionally include SGLs or data. A response capsule contains a response
(formatted as a completion queue entry) and may optionally include data. Data refers to any data transferred
at an NVMe layer between a host and an NVM subsystem (e.g., logical block data or a data structure
associated with a command). A capsule is independent of any underlying NVMe Transport unit (e.g.,
packet, message, or frame and associated headers and footers) and may consist of multiple such units.


Command capsules are transferred from a host to an NVM subsystem. The SQE contains an Admin
command, an I/O command, or a Fabrics command. The minimum size of a command capsule is NVMe
Transport binding specific, but shall be at least 64B in size. The maximum size of a command capsule is
NVMe Transport binding specific. The format of a command capsule is shown in Figure 9.


**Figure 9: Command Capsule Format**


Byte 0 63 64 ( _N_ -1)


Submission Queue Entry Data or SGLs (if present)


Command Capsule of Size N Bytes


Response capsules are transferred from an NVM subsystem to a host. The CQE is associated with a
previously issued Admin command, I/O command, or Fabrics command. The size of a response capsule is
NVMe Transport binding specific, but shall be at least 16B in size. The maximum size of a response capsule
is NVMe Transport binding specific. The format of a response capsule is shown in Figure 10.


23


NVM Express [®] Base Specification, Revision 2.2


**Figure 10: Response Capsule Format**


Byte 0 15 16 ( _N_ -1)


Completion Queue Entry Data (if present)


Response Capsule of Size N Bytes


NVMe Transports using the message-only transport model and message/memory transport model require
all SGLs sent from the host to the controller be transferred within the command. NVMe Transports may
optionally support the transfer of a portion or all data within the command and response capsules.


NVMe over Fabrics requires SGLs for all commands (Fabrics, Admin, and I/O). An SGL may specify the
placement of data within a capsule or the information required to transfer data using an NVMe Transport
specific data transfer mechanism (e.g., via memory transfers as in RDMA). Each NVMe Transport binding
specification defines the SGLs used by a particular NVMe Transport and any capsule SGL and data
placement restrictions.


**Authentication**


NVMe over Fabrics supports both fabric secure channel that includes authentication (refer to section
8.3.4.1) and NVMe in-band authentication. An NVM subsystem may require a host to use fabric secure
channel, NVMe in-band authentication, or both. The Discovery Service indicates if fabric secure channel
shall be used for an NVM subsystem. The Connect response indicates if NVMe in-band authentication shall
be used with that controller.


A controller associated with an NVM subsystem that requires a fabric secure channel shall not accept any
commands (i.e., Fabrics commands, Admin commands, or I/O commands) on an NVMe Transport until a
secure channel is established. Following a Connect command, a controller that requires NVMe in-band
authentication shall not accept any commands on the queue created by that Connect command other than
authentication commands until NVMe in-band authentication has completed. Refer to section 8.3.4.


**2.3** **NVM Storage Model**


**Storage Entities**


The NVM storage model includes the following entities:

  - NVM subsystems (refer to 1.5.66);

  - Domains (refer to section 3.2.5);

  - Endurance Groups (refer to section 3.2.3);

  - Reclaim Groups and Reclaim Units (refer to section 3.2.4);

  - NVM Sets (refer to section 3.2.2); and

  - Namespaces (refer to section 3.2.1).


As illustrated below,

  - each domain is contained in a single NVM subsystem;

  - each Endurance Group is contained in a single domain and may contain either:


`o` one or more NVM Sets; or

`o` one or more Reclaim Groups;

  - each NVM Set is contained in a single Endurance Group and each namespace is contained in a
single NVM Set. Each Media Unit is contained in a single Endurance Group; and

  - each Reclaim Group is contained in a single Endurance Group, each Reclaim Unit is contained in
a Reclaim Group, and each namespace is contained in an Endurance Group within one or more
Reclaim Units of the Reclaim Groups in that Endurance Group.


24


NVM Express [®] Base Specification, Revision 2.2


Each Endurance Group is composed of storage media, which are termed Media Units (refer to section
8.1.4.2) or Reclaim Units (refer to section 3.2.4). Reclaim Unit Handles reference a Reclaim Unit in each
Reclaim group for writing user data. For clarity, Media Units, Reclaim Unit Handles, and Reclaim Units are
not shown in the examples in this section that follow.


Figure 11 shows the hierarchical relationships of these entities within a simple NVM subsystem, which has:

  - one domain;

  - one Endurance Group;

  - one NVM Set; and

  - one namespace.


**Figure 11: Simple NVM Storage Hierarchy with NVM Sets**





25


NVM Express [®] Base Specification, Revision 2.2


Figure 12 shows the hierarchical relationships in a simple NVM subsystem, which has:

  - one domain;

  - one Endurance Group;

  - one Reclaim Group; and

  - one namespace with user data written to the single Reclaim Group.


The placement (i.e., which Reclaim Group) of user data for a namespace is directed by each host write
command to that namespace (refer to section 8.1.10).


**Figure 12: Simple NVM Storage Hierarchy with One Reclaim Group**





Figure 13 shows the hierarchical relationships in a simple NVM subsystem, which has:

  - one domain;

  - one Endurance Group;

  - four Reclaim Groups; and

  - one namespace with user data written to each Reclaim Group.


The placement (i.e., which Reclaim Group) of user data for a namespace is directed by each host write
command to that namespace (refer to section 8.1.10).


26


NVM Express [®] Base Specification, Revision 2.2


**Figure 13: Simple NVM Storage Hierarchy with Multiple Reclaim Groups**













Figure 14 shows the relationships of these entities in a complex NVM subsystem, which has:

  - multiple domains;

  - multiple Endurance Groups per domain;

  - multiple NVM Sets per Endurance Group; and

  - multiple namespaces per NVM Set.


27


NVM Express [®] Base Specification, Revision 2.2


**Figure 14: Complex NVM Storage Hierarchy with NVM Sets**





























































Entity naming key (Abc):


A: Domain (capital letter)
b: Endurance Group (digit)
c: NVM Set (lower case letter)


Figure 15 shows the relationships in a complex NVM subsystem, which has:

  - multiple domains;

  - multiple Endurance Groups per domain;

  - multiple Reclaim Groups per Endurance Group; and

  - multiple namespaces per Endurance Group.


The placement (i.e., which Reclaim Group) of user data for a namespace is directed by each host write
command to that namespace (refer to section 8.1.10).


28


NVM Express [®] Base Specification, Revision 2.2


**Figure 15: Complex NVM Storage Hierarchy with Multiple Reclaim Groups**





...






|Col1|Col2|Col3|Col4|Col5|
|---|---|---|---|---|
|||Namesp|ace||
|||Reclaim<br>Group<br>A11<br>pace|Reclaim<br>Group<br>A11<br>pace|Reclaim<br>Group<br>A11<br>pace|
|Name|s|pace|pace|pace|


|Col1|Col2|Col3|Col4|Col5|Col6|
|---|---|---|---|---|---|
|||Namesp|Namesp|ace||
|||Reclaim<br>Group<br>A31<br>N|Reclaim<br>Group<br>A31<br>N|||
|||Reclaim<br>Group<br>A31<br>N|N|amespac|e|

















Endurance Group A1







Endurance Group A3



Domain A


...
















|Col1|Col2|Col3|Col4|Col5|
|---|---|---|---|---|
|||Namesp|ace||
|||Reclaim<br>Group<br>D11<br>Namesp|Reclaim<br>Group<br>D11<br>Namesp|Reclaim<br>Group<br>D11<br>Namesp|


|Na|mespace|
|---|---|
|Na|Reclaim<br>Group<br>D5i|



Endurance Group D1


Entity naming key (Abc):



Endurance Group D5



Domain D


NVM Subsystem



A: Domain (capital letter)
b: Endurance Group (digit)
c: Reclaim Group (digit or lower-case letter for maximum number)


The support of Endurance Groups, Reclaim Groups within an Endurance Group, or NVM Sets within an
Endurance Group is optional, but the storage model supports these concepts. An NVM subsystem may be
shipped by the vendor with storage entities configured, or an NVM subsystem may be configured or reconfigured by the customer. Typical changes to the configuration are creation and deletion of namespaces.


An NVM subsystem that does not support multiple NVM Sets does not require reporting of NVM Sets. An
NVM subsystem that does not support multiple Endurance Groups does not require reporting of Endurance
Groups.


29


NVM Express [®] Base Specification, Revision 2.2


**I/O Command Sets**


I/O commands perform operations on namespaces, and each namespace is associated with exactly one
I/O command set. For example, commands in the NVM Command Set access data represented in a
namespace as logical blocks, and commands in the Key Value Command Set access data represented in
a namespace as key-value pairs.


The association of a namespace to an I/O command set is specified when the namespace is created and
is fixed for the lifetime of that namespace.


A controller may support one or more I/O command sets. Namespaces that are associated with the I/O
command sets that are supported and enabled on a controller may be attached to that controller. A host
issues commands to a namespace and those commands are interpreted based on the I/O command set
associated with that namespace.


**NVM Subsystem Examples**


Figure 16 illustrates a simple NVM subsystem that has a single instance of each storage entity.


**Figure 16: Single-Namespace NVM Subsystem**




- The NVM subsystem consists of a single port and a single domain.

- The domain contains a controller and storage media.

- All of the storage media are contained in one Endurance Group.

- All of the storage media in that Endurance Group are organized into one NVM Set.

- That NVM Set contains a single namespace.


30


NVM Express [®] Base Specification, Revision 2.2


Figure 17 shows an NVM subsystem with two namespaces.


**Figure 17: Two-Namespace NVM Subsystem**









31


NVM Express [®] Base Specification, Revision 2.2


An NVM subsystem may have multiple domains, multiple namespaces, multiple controllers, and multiple
ports, as shown in Figure 18.


**Figure 18: Complex NVM Subsystem**



















**2.4** **Extended Capabilities Theory**


**Multi-Path I/O and Namespace Sharing**


This section provides an overview of multi-path I/O and namespace sharing. Multi-path I/O refers to two or
more completely independent paths between a single host and a namespace while namespace sharing
refers to the ability for two or more hosts to access a common shared namespace using different NVM
Express controllers. Both multi-path I/O and namespace sharing require that the NVM subsystem contain
two or more controllers. NVM subsystems that support Multi-Path I/O and Namespace Sharing may also
support asymmetric controller behavior (refer to section 2.4.2). Concurrent access to a shared namespace
by two or more hosts requires some form of coordination between hosts. The procedure used to coordinate
these hosts is outside the scope of this specification.


Figure 19 shows an NVM subsystem that contains a single NVM Express controller implemented over PCI
Express and a single PCI Express port. Since this is a single Function PCI Express device, the NVM
Express controller shall be associated with PCI Function 0. A controller may support multiple namespaces.
The controller in Figure 19 supports two namespaces labeled NS A and NS B. Associated with each
controller namespace is a namespace ID, labeled as NSID 1 and NSID 2, that is used by the controller to
reference a specific namespace. The namespace ID is distinct from the namespace itself and is the handle
a host and controller use to specify a particular namespace in a command. The selection of a controller’s
namespace IDs is outside the scope of this specification. In this example, NSID 1 is associated with


32


NVM Express [®] Base Specification, Revision 2.2


namespace A and NSID 2 is associated with namespace B. Both namespaces are private to the controller
and this configuration supports neither multi-path I/O nor namespace sharing.


**Figure 19: NVM Express Controller with Two Namespaces**


PCIe Port







Figure 20 shows a multi-Function NVM subsystem with a single PCI Express port containing two controllers
implementing NVMe over PCIe. One controller is associated with PCI Function 0 and the other controller is
associated with PCI Function 1. Each controller supports a single private namespace and access to shared
namespace B. The namespace ID shall be the same in all controllers that have access to a particular shared
namespace. In this example, both controllers use NSID 2 to access shared namespace B.


**Figure 20: NVM Subsystem with Two Controllers and One Port**


PCIe Port









There is one or more Identify Controller data structures for each controller and one or more Identify
Namespace data structures (refer to section 1.5.49) for each namespace (refer to Figure 311). Controllers
with access to a shared namespace return the Identify Namespace data structure associated with that
shared namespace (i.e., the same data structure contents are returned by all controllers with access to the
same shared namespace). There is a globally unique identifier (refer to section 4.7.1) associated with the
namespace itself and may be used to determine when there are multiple paths to the same shared
namespace.


Controllers associated with a shared namespace may operate on the namespace concurrently. Operations
performed by individual controllers are atomic to the shared namespace at the write atomicity level of the


33


NVM Express [®] Base Specification, Revision 2.2


controller to which the command was submitted (refer to section 3.4.3). The write atomicity level is not
required to be the same across controllers that share a namespace. If there are any ordering requirements
between commands issued to different controllers that access a shared namespace, then host software or
an associated application, is required to enforce these ordering requirements.


Figure 21 illustrates an NVM subsystem with two PCI Express ports, each with an associated controller
implementing NVMe over PCIe. Both controllers map to PCI Function 0 of the corresponding port. Each
PCI Express port in this example is completely independent and has its own PCI Express Fundamental
Reset and reference clock input. A reset of a port only affects the controller associated with that port and
has no impact on the other controller, shared namespace, or operations performed by the other controller
on the shared namespace. Refer to section 4.4 for Feature behavior on reset. The functional behavior of
this example is otherwise the same as that illustrated in Figure 20.


**Figure 21: NVM Subsystem with Two Controllers and Two Ports**


PCIe Port _x_ PCIe Port _y_









The two ports shown in Figure 21 may be associated with the same Root Complex or with different Root
Complexes and may be used to implement both multi-path I/O and I/O sharing architectures. System-level
architectural aspects and use of multiple ports in a PCI Express fabric are beyond the scope of this
specification.


Figure 22 illustrates an NVM subsystem that supports Single Root I/O Virtualization (SR-IOV) and has one
Physical Function and four Virtual Functions. An NVM Express controller implementing NVMe over PCIe is
associated with each Function with each controller having a private namespace and access to a namespace
shared by all controllers, labeled NS F. The behavior of the controllers in this example parallels that of the
other examples in this section. Refer to section 8.2.6.4 for more information on SR-IOV.


34


NVM Express [®] Base Specification, Revision 2.2


**Figure 22: PCI Express Device Supporting Single Root I/O Virtualization (SR-IOV)**


PCIe Port



























Examples provided in this section are meant to illustrate concepts and are not intended to enumerate all
possible configurations. For example, an NVM subsystem may contain multiple PCI Express ports with
each port supporting SR-IOV.


**Asymmetric Controller Behavior**


Asymmetric controller behavior occurs in NVM subsystems where namespace access characteristics (e.g.,
performance) may vary based on:

  - the internal configuration of the NVM subsystem; or

  - which controller is used to access a namespace (e.g., Fabrics).


NVM subsystems that provide asymmetric controller behavior may support Asymmetric Namespace
Access Reporting as described in section 8.1.1.


35


