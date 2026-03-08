NVM Express [®] Base Specification, Revision 2.2


**3 NVM Express Architecture**


**3.1** **NVM Controller Architecture**


A controller is the interface between a host and an NVM subsystem. This specification defines two controller
models, the static controller model and the dynamic controller model. All controllers in an NVM subsystem
shall support the same controller model.


In an NVM subsystem that supports the static controller model, state (e.g., controller ID, saved Feature
settings) is preserved:

  - across a Controller Level Reset for memory-based controllers and message-based controllers; and

  - from prior associations for message-based controllers.


In an NVM subsystem that supports the dynamic controller model, the NVM subsystem allocates controllers
on demand with no state preserved from prior associations.


**Memory-Based Controller Architecture (PCIe)**


Memory-based controllers shall support only the static controller model.


**Message-Based Controller Architecture (Fabrics)**


Message-based controllers, other than Discovery controllers, may support either the dynamic controller
model or the static controller model. A Discovery controller shall support only the dynamic controller model.


In an NVM subsystem that supports the static controller model, each controller that is allocated to a
particular host may have different state at the time the association is established (e.g., each controller may
have state that is preserved from a prior association). The controllers within such an NVM subsystem are
distinguished by their controller identifier. The host may request a particular controller based on the
Controller ID (refer to the CNTLID field in Figure 547).


In an NVM subsystem that supports the dynamic controller model, each controller is allocated by the NVM
subsystem on demand with no state (e.g., Controller ID, Feature settings) preserved from prior
associations. In this model, all controllers allocated to a specific host have the same state at the time the
association is established, including Feature settings. The initial set of attached namespaces should be the
same for all controllers that are allocated to a specific host and accessed via the same NVM subsystem
port. The initial set of attached namespaces may differ among controllers that are each accessed via a
different NVM subsystem port. Changes to a dynamic controller (e.g., attached namespaces, Feature
settings) after the association is established do not impact other dynamic controllers in that NVM
subsystem.


An association is established between a host and a controller when the host connects to a controller’s
Admin Queue using the Fabrics Connect command (refer to section 6.3). Within the Connect command,
the host specifies the Host NQN, NVM Subsystem NQN, Host Identifier, and may request a specific
Controller ID (e.g., the static controller model is being used) or may request a connection to any available
controller (e.g., the dynamic controller model is being used). A controller has only one association at a time.


While an association exists between a host and a controller, only that host may establish connections with
I/O Queues of that controller. To establish a new connection with I/O Queues of that controller, the host
sends subsequent Connect commands using the same NVM subsystem port, NVMe Transport type, and
NVMe Transport address and specifies the:

  - same Host NQN;

  - same NVM Subsystem NQN;

  - same Controller ID; and

  - either the:


`o` same Host Identifier; or

`o` a Host Identifier value of 0h, if supported (refer to section 5.1.12.3.1).


36


NVM Express [®] Base Specification, Revision 2.2


An association between a host and controller is terminated if:

  - the controller is shutdown as described in section 3.6.2;

  - a Controller Level Reset occurs;

  - the NVMe Transport connection is lost between the host and controller for the Admin Queue; or

  - an NVMe Transport connection is lost between the host and controller for any I/O Queue and the
host or controller does not support individual I/O Queue deletion (refer to section 3.3.2.4).


There is no explicit NVMe command that breaks the NVMe Transport association between a host and
controller. The Disconnect command (refer to section 6.4) provides a method to delete an I/O Queue (refer
to section 3.3.2.4). While a controller is associated with a host, that controller is busy, and no other
associations may be made with that controller.


To use the dynamic controller model, the host specifies a controller identifier of FFFFh when using the
Fabrics Connect command (refer to section 6.3) to establish an association with an NVM subsystem.


When using the static controller model with a fabric connected controller, the state that persists across
associations is any state that persists across a Controller Level Reset. Additionally, different controllers
may present different Feature settings or namespace attachments to the same host. The NVM subsystem
may allocate particular controllers to specific hosts.


While allocation of static controllers to hosts are expected to be durable (so that hosts can expect to form
associations to the same controllers repeatedly (e.g., after each host reboot)), the NVM subsystem may
remove the host allocation of a controller that is not in use at any time for implementation specific reasons
(e.g., controller resource reclamation, subsystem reconfiguration).


**Controller Types**


As shown in Figure 23Figure 23, there are three types of controllers. An I/O controller (refer to section
3.1.3.1) is a controller that supports commands that provide access to user data stored on an NVM
subsystem’s non-volatile storage medium and may support commands that provide management
capabilities. An Administrative controller (refer to section 3.1.3.2) is a controller that supports commands
that provide management capabilities, but does not support I/O commands that access to user data stored
on an NVM subsystem’s non-volatile storage medium. A Discovery controller (refer to section 3.1.3.3) is a
controller used in NVMe over Fabrics to provide access to a Discovery log page.


**Figure 23: Controller Types**


The Controller Type (CNTRLTYPE) field in the Identify Controller data structure indicates a controller’s
type. Regardless of controller type, all controllers implement one Admin Submission Queue and one Admin
Completion Queue. Depending on the controller type, a controller may also support one or more I/O
Submission Queues and I/O Completion Queues.


When using a memory-based transport implementation (e.g., PCIe), host software submits commands to a
controller through pre-allocated Submission Queues. A controller is alerted to newly submitted commands
through SQ Tail Doorbell register writes. The difference between the previous doorbell register value and
the current register write indicates the number of commands that were submitted.


A controller fetches commands from the Submission Queue(s) and processes them. Except for fused
operations, there are no ordering restrictions for processing of commands within or across Submission
Queues. Host software should not submit commands to a Submission Queue that may not be re-ordered


37


NVM Express [®] Base Specification, Revision 2.2


arbitrarily by the controller. Data associated with the processing of a command may or may not be
committed to the NVM subsystem non-volatile storage medium in the order that commands are submitted.


Host software submits commands of higher priorities to the appropriate Submission Queues. Priority is
associated with the Submission Queue itself, thus the priority of the command is based on the Submission
Queue to which that command was submitted. The controller arbitrates across the Submission Queues
based on fairness and priority according to the arbitration scheme specified in section 3.4.4.


Upon completion of the command execution by the NVM subsystem, the controller presents completion
queue entries to the host through the appropriate Completion Queues. Transport specific methods (e.g.,
PCIe interrupts) are used to notify the host of completion queue entries to process (refer to the appropriate
Transport specification).


There are no ordering restrictions for completions to the host. Each completion queue entry identifies the
Submission Queue Identifier and Command Identifier of the associated command. Host software uses this
information to correlate the completions with the commands submitted to the Submission Queue(s).


Host software is responsible for creating I/O Submission Queues and I/O Completion Queues prior to using
those queue pairs to submit commands to the controller. I/O Submission Queues and I/O Completion
Queues are created using the Create I/O Submission Queue command (refer to section 5.2.2) and the
Create I/O Completion Queue command (refer to section 5.2.1).


**I/O Controller**


An I/O controller is a controller that supports commands that provide access to user data stored on an NVM
subsystem’s non-volatile storage medium using an I/O command set and may support commands that
provide management capabilities.


An I/O controller may simultaneously support multiple I/O Command Sets. The I/O Command Sets that the
controller supports and which of these I/O Command Sets the controller simultaneously supports is reported
in the Identify I/O Command Set data structure (refer to section 5.1.13.2.19). The contents of the Identify
I/O Command Set data structure are not required to be the same for all controllers in an NVM subsystem.


Figure 24 shows an NVM subsystem with three I/O controllers. I/O controller one has two attached
namespaces, private namespace A and shared namespace B. I/O controller two also has two attached
namespaces, private namespace C and shared namespace B. I/O controller three has no attached
namespaces. At some later point in time shared namespace B may be attached to I/O controller three.


**Figure 24: NVM Subsystem with Three I/O Controllers**


38


NVM Express [®] Base Specification, Revision 2.2


**Administrative Controller**


An Administrative controller is a controller whose intended purpose is to provide NVM subsystem
management capabilities. While an I/O controller may support these same management capabilities, an
Administrative controller has fewer mandatory capabilities. Unlike an I/O controller, an Administrative
controller does not support I/O commands that access to user data stored on an NVM subsystem’s nonvolatile storage medium. NVMe Transports may support a transport specific mechanism to allow an
Administrative controller to load a dedicated NVMe management driver instead of a generic NVMe driver
(refer to the applicable NVMe Transport binding specification for details).


Examples of management capabilities that may be supported by an Administrative controller include the
following.

  - Ability to efficiently poll NVM subsystem health status via NVMe-MI using the NVMe-MI Send
command and the NVMe-MI Receive command (refer to the NVM Subsystem Health Status Poll
section in the NVM Express Management Interface Specification);

  - Ability to manage an NVMe enclosure via NVMe-MI using the NVMe-MI Send command and the
NVMe-MI Receive command;

  - Ability to manage NVM subsystem namespaces using the Namespace Attachment command and
the Namespace Management command;

  - Ability to perform virtualization management using the Virtualization Management command;

  - Ability to reset an entire NVM subsystem using the NVM Subsystem Reset (NSSR) register if
supported; and

  - Ability to shutdown an entire NVM subsystem using the NVM Subsystem Shutdown (NSSD)
property, if supported.


An Administrative controller shall not support I/O Queues. Namespaces shall not be attached to an
Administrative controller.


An Administrative controller is required to support the mandatory Admin commands listed in Figure 28. An
Administrative controller may support one or more I/O Command Sets. If an Administrative controller
supports an I/O Command Set, then only I/O Command Set specific Admin commands may be supported
since an Administrative controller only has an Admin Queue and no I/O Queues.


Figure 25 shows an NVM subsystem with one Administrative controller and two I/O controllers within an
NVM subsystem that contains a non-volatile storage medium and namespaces. I/O controller one has two
attached namespaces, private namespace A and shared namespace B. I/O controller two also has two
attached namespaces, private namespace C and shared namespace B. An Administrative controller has
no attached namespaces. The Administrative controller in this example may be used for tasks such as NVM
subsystem namespace management and efficiently polling NVM subsystem health status via NVMe-MI.
While this example shows a single Administrative controller, an NVM subsystem may support zero or more
Administrative controllers.


39


NVM Express [®] Base Specification, Revision 2.2


**Figure 25: NVM Subsystem with One Administrative and Two I/O Controllers**


Figure 26 shows an NVM subsystem with one Administrative controller within an NVM subsystem that
contains no non-volatile storage medium or namespaces. The Administrative controller in this example may
be used to manage an NVMe enclosure using NVMe-MI. Since the Administrative controller is used for a
very specific dedicated purpose, the implementer of such an Administrative controller may choose to
implement only the mandatory capabilities along with the NVMe-MI Send and NVMe-MI Receive
commands.


**Figure 26: NVM Subsystem with One Administrative Controller**


Port





**Discovery Controller**


A Discovery controller is a controller used in NVMe over Fabrics. A Discovery controller enables a host to
discover other NVM subsystems or other Discovery subsystems. A Discovery controller only implements
features related to Discovering other subsystems and does not implement I/O Queues, I/O commands, or
expose namespaces. The features supported by the Discovery controller are defined in section 3.1.3.6.


If the Discovery subsystem provides a unique Discovery Service NQN (i.e., the NVM Subsystem NVMe
Qualified Name (SUBNQN) field in that Discovery subsystem’s Identify Controller data structure contains a
unique Discovery Service NQN value), then that Discovery subsystem shall support both the unique
Discovery Service NQN and the well-known Discovery Service NQN (i.e., nqn.201408.org.nvmexpress.discovery) being specified in the Connect command (refer to section 6.3) from the host.


If the Discovery subsystem does not provide a unique Discovery Service NQN (i.e., the SUBNQN field in
that Discovery subsystem’s Identify Controller data structure contains the well-known Discovery Service
NQN), then that Discovery subsystem shall support the well-known Discovery Service NQN being specified
in the Connect command from the host.


40


NVM Express [®] Base Specification, Revision 2.2


In the Connect command to a Discovery subsystem that provides a unique Discovery Service NQN, the
host may use either of the following:

  - the well-known Discovery Service NQN; or

  - the unique Discovery Service NQN of that Discovery subsystem.


In the Connect command to a Discovery subsystem that does not provide a unique Discovery Service NQN,
the host uses the well-known Discovery Service NQN.


The method that a host uses to obtain the fabric information necessary to connect to a Discovery controller
using the well-known Discovery Service NQN or the unique NQN via the NVMe Transport may be:


a) implementation specific;
b) fabric specific;
c) known in advance (e.g., a well-known address);
d) administratively configured; or
e) for IP-based fabrics, Automated Discovery of Discovery Controllers for IP-based Fabrics (refer to

section 8.3.1) may be used.


The Discovery log page provided by a Discovery controller contains one or more entries. Each entry
specifies information necessary for the host to connect to an NVM subsystem. An entry may be associated
with an NVM subsystem that exposes namespaces or a referral to another Discovery Service. There are
no ordering requirements for log page entries within the Discovery log page.


Discovery controller(s) may provide different log page contents depending on the Host NQN provided (e.g.,
different NVM subsystems may be accessible to different hosts). The set of Discovery Log Page Entries
should include all applicable addresses on the same fabric as the Discovery Service and may include
addresses on other fabrics.


Discovery controllers that support explicit persistent connections shall support both the Asynchronous
Event Request command and the Keep Alive command (refer to sections 5.1.2 and 5.1.14 respectively). A
host requests an explicit persistent connection to a Discovery controller and Asynchronous Event
Notifications from the Discovery controller on that persistent connection by specifying a non-zero Keep
Alive Timer value in the Connect command. If the Connect command specifies a non-zero Keep Alive Timer
value and the Discovery controller does not support Asynchronous Events, then the Discovery controller
shall return a status value of Connect Invalid Parameters (refer to Figure 549) for the Connect command.
Discovery controllers shall indicate support for Discovery Log Change Notifications in the Identify Controller
data structure (refer to Figure 313).


Discovery controllers that do not support explicit persistent connections shall not support Keep Alive
commands and may use a fixed Discovery controller activity timeout value (e.g., 2 minutes). If no commands
are received by such a Discovery controller within that time period, the controller may perform the actions
for Keep Alive Timer expiration defined in section 3.9.5.


A Discovery controller shall not support the Disconnect command.


A Discovery log page with multiple Discovery Log Page Entries for the same NVM subsystem indicates that
there are multiple fabric paths to the NVM subsystem, and/or that multiple static controllers may share a
fabric path. The host may use this information to form multiple associations to controllers within an NVM
subsystem.


Multiple Discovery Log Page Entries for the same NVM subsystem with different Port ID values indicates
that the resulting NVMe Transport connections are independent with respect to NVM subsystem port
hardware failures. A host that uses a single association should pick a record to attach to an NVM
subsystem. A host that uses multiple associations should choose different ports.


A transport specific method may exist to indicate changes to a Discovery controller.


Controller IDs in the range FFF0h to FFFFh are not allocated as valid Controller IDs on completion of a
Connect command, as described in section 6.3. Figure 27 defines these Controller IDs.


41


NVM Express [®] Base Specification, Revision 2.2


**Figure 27: Controller IDs FFF0h to FFFFh**







|Controller ID|Definition|
|---|---|
|FFF0h to FFFCh|Reserved. Use of this value in a Connect command results in a status code of Connect Invalid<br>Parameters being returned, as described in section 6.3.|
|FFFDh|This value in the Controller ID (CNTLID) field of the Registered Controller data structure or<br>Registered Controller Extended data structure for a dispersed namespace indicates that the<br>controller is not contained in the same participating NVM subsystem as the controller processing<br>the command (refer to section 8.1.9.6). Use of this value in a Connect command results in a<br>status code of Connect Invalid Parameters being returned, as described in section 6.3.|
|FFFEh|This value is sent in a Connect command to specify that any available static controller is allowed<br>to be allocated.|
|FFFFh|This value is sent in a Connect command to specify that any available dynamic controller is<br>allowed to be allocated.|


The Controller ID values returned in the Discovery Log Page Entries indicate whether an NVM subsystem
supports the dynamic or static controller model. The controller ID value of FFFFh is used for NVM
subsystems that support the dynamic controller model indicating that any available controller may be
returned. The Controller ID value of FFFEh is used for NVM subsystems that support the static controller
model indicating that any available controller may be returned. An NVM subsystem supports the dynamic
controller model if Discovery Log Page Entries use the Controller ID value of FFFFh. An NVM subsystem
supports the static controller model if Discovery Log Page Entries use a Controller ID value that is less than
FFFFh. The Identify Controller data structure also indicates whether an NVM subsystem is dynamic or
static.


If an NVM subsystem implements the dynamic controller model, then multiple Discovery Log Page Entries
(refer to Figure 295) with the Controller ID set to FFFFh may be returned for that NVM subsystem (e.g., to
indicate multiple NVM subsystem ports) in the Discovery log page. If an NVM subsystem implements the
static controller model, then multiple Discovery Log Page Entries that indicate different Controller ID values
may be returned for that NVM subsystem in the Discovery log page. If an NVM subsystem that implements
the static controller model includes any Discovery Log Page Entries that indicate a Controller ID of FFFEh,
then the host should remember the Controller ID returned from the Fabrics Connect command and re-use
the allocated Controller ID for future associations to that particular controller.


**3.1.3.3.1** **Discovery Controller Asynchronous Event Configuration**


Discovery controllers that support Asynchronous Event Notifications shall implement the Get Features and
Set Features commands. A Discovery controller shall enable Asynchronous Discovery Log Event
Notifications, if a non-zero Keep Alive Timeout (KATO) value is received in the Connect command (refer to
section 6.3) sent to that controller.


Figure 392 defines Discovery controller Asynchronous Event Notifications.


**3.1.3.3.2** **Discovery Controller Asynchronous Event Information – Requests and Notifications**


If a Discovery controller detects an event about which a host has requested notification, then the Discovery
controller shall send an Asynchronous Event with the:

  - Asynchronous Event Type field set to Notice (i.e., 2h);

  - Log Page Identifier field set to either Discovery (i.e., 70h) or Host Discovery (i.e., 71h) depending
on which log page has changed; and

  - Asynchronous Event Information field set as defined in Figure 152.


As a result of a Discovery controller updating Discovery log page(s), that Discovery controller shall send a
Discovery Log Page Change Asynchronous Event notification (i.e., the Asynchronous Event Information
field set to F0h) to each entity that has requested asynchronous event notifications of this type (refer to
Figure 152).


42


NVM Express [®] Base Specification, Revision 2.2


As a result of a Discovery controller updating Host Discovery log page(s), that Discovery controller shall
send a Host Discovery Log Page Change Asynchronous Event notification (i.e., the Asynchronous Event
Information field set to F1h) to each entity that has requested asynchronous event notifications of this type
(refer to Figure 152).


**3.1.3.3.3** **Discovery Controller Initialization**


The initialization process for Discovery controllers is described in section 3.5.2.1.


**Command Support Requirements**


Figure 28 defines commands that are mandatory, optional, and prohibited for an I/O controller,
Administrative controller, and Discovery controller. I/O Command Set specific command support
requirements are described within individual I/O Command Set specifications. Since an Administrative
controller does not support I/O queues, I/O Command Set specific commands that are not Admin
commands are not supported by an Administrative controller.


A host may utilize the Commands Supported and Effects log page to determine optional commands that
are supported by a controller.


**Figure 28: Admin Command Support Requirements**









|Command|Combined<br>Opcode<br>Value|1<br>Controller Support Requirements|Col4|Col5|Reference|
|---|---|---|---|---|---|
|**Command**|**Combined**<br>**Opcode**<br>**Value**|**I/O**|**Administrative**|**Discovery**|**Discovery**|
|Delete I/O Submission Queue|00h|M 9|P|P|5.2.4|
|Create I/O Submission Queue|01h|M 9|P|P|5.2.2|
|Get Log Page|02h|M|M|M|5.1.12|
|Delete I/O Completion Queue|04h|M 9|P|P|5.2.3|
|Create I/O Completion Queue|05h|M 9|P|P|5.2.1|
|Identify|06h|M|M|M|5.1.13|
|Abort|08h|M|O|O|5.1.1|
|Set Features|09h|M|O 4|Note 6|5.1.25|
|Get Features|0Ah|M|O 4|Note 6|5.1.11|
|Asynchronous Event Request|0Ch|M|O 5|Note 6|5.1.2|
|Namespace Management|0Dh|O|O|P|5.1.21|
|Firmware Commit|10h|O|O|P|5.1.8|
|Firmware Image Download|11h|O|O|P|5.1.9|
|Device Self-test|14h|O|O|P|5.1.5|
|Namespace Attachment|15h|O|O|P|5.1.20|
|Keep Alive|18h|M 2|M 2|Note 6|5.1.14|
|Directive Send|19h|O|O|P|5.1.7|
|Directive Receive|1Ah|O|O|P|5.1.6|
|Virtualization Management|1Ch|O|O|P|5.2.6|
|NVMe-MI Send|1Dh|O|O|P|5.1.19|
|NVMe-MI Receive|1Eh|O|O|P|5.1.18|
|Capacity Management|20h|O|O|P|5.1.3|
|Discovery Information Management|21h|P|P|M 7|5.3.3|
|Fabric Zoning Receive|22h|P|P|M 7|5.3.5|
|Lockdown|24h|O|O|P|5.1.15|
|Fabric Zoning Lookup|25h|P|P|M 7|5.3.4|
|Clear Exported NVM Resource<br>Configuration|28h|P|O|P|5.3.1|
|Fabric Zoning Send|29h|P|P|M 7|5.3.6|


43


NVM Express [®] Base Specification, Revision 2.2


**Figure 28: Admin Command Support Requirements**



















|Command|Combined<br>Opcode<br>Value|1<br>Controller Support Requirements|Col4|Col5|Reference|
|---|---|---|---|---|---|
|**Command**|**Combined**<br>**Opcode**<br>**Value**|**I/O**|**Administrative**|**Discovery**|**Discovery**|
|Create Exported NVM Subsystem|2Ah|P|O|P|5.3.2|
|Manage Exported NVM Subsystem|2Dh|P|O|P|5.3.8|
|Manage Exported Namespace|31h|P|O|P|5.3.7|
|Manage Exported Port|35h|P|O|P|5.3.9|
|Send Discovery Log Page|39h|P|P|M 7|5.3.10|
|Track Send|3Dh|O|O|P|5.1.27|
|Track Receive|3Eh|O|O|P|5.1.26|
|Migration Send|41h|O|O|P|5.1.17|
|Migration Receive|42h|O|O|P|5.1.16|
|Controller Data Queue|45h|O|O|P|5.1.4|
|Doorbell Buffer Config|7Ch|O|O|P|5.2.5|
|**I/O Command Set specific Admin commands**|**I/O Command Set specific Admin commands**|**I/O Command Set specific Admin commands**|**I/O Command Set specific Admin commands**|**I/O Command Set specific Admin commands**|**I/O Command Set specific Admin commands**|
|Format NVM|80h|O|O|P|5.1.10|
|Security Send|81h|O|O|P|5.1.24|
|Security Receive|82h|O|O|P|5.1.23|
|Sanitize|84h|O 3|O 3|P|5.1.22|
|I/O Command Set specific Admin<br>command|85h|Note 8|P|P|Note 8|
|I/O Command Set specific Admin<br>command|86h|86h|86h|86h|86h|
|I/O Command Set specific Admin<br>command|88h|88h|88h|88h|88h|
|I/O Command Set specific Admin<br>command|89h|89h|89h|89h|89h|
|**Vendor Specific**|**Vendor Specific**|**Vendor Specific**|**Vendor Specific**|**Vendor Specific**|**Vendor Specific**|
|Vendor Specific||O|O|O||
|Notes:<br>1.<br>O/M/P definition: O = Optional, M = Mandatory, P = Prohibited<br>2.<br>Prohibited if the Keep Alive Timer feature is not supported (refer to section 3.9).<br>3.<br>Prohibited for an Exported NVM Subsystem (refer to section 8.3.3).<br>4.<br>Mandatory if any of the features in Figure 32 are implemented.<br>5.<br>Mandatory if Telemetry Log, Firmware Commit, or SMART/Health Critical Warnings are supported.<br>6.<br>For Discovery controllers that support explicit persistent connections, this command is mandatory. For Discovery<br>controllers that do not support explicit persistent connections, this command is prohibited.<br>7.<br>Mandatory for CDCs and optional for Discovery controllers that are not a CDC.<br>8.<br>Refer to the applicable I/O Command Set specification.<br>9.<br>Mandatory for NVMe over PCIe. This command is not supported for NVMe over Fabrics.|Notes:<br>1.<br>O/M/P definition: O = Optional, M = Mandatory, P = Prohibited<br>2.<br>Prohibited if the Keep Alive Timer feature is not supported (refer to section 3.9).<br>3.<br>Prohibited for an Exported NVM Subsystem (refer to section 8.3.3).<br>4.<br>Mandatory if any of the features in Figure 32 are implemented.<br>5.<br>Mandatory if Telemetry Log, Firmware Commit, or SMART/Health Critical Warnings are supported.<br>6.<br>For Discovery controllers that support explicit persistent connections, this command is mandatory. For Discovery<br>controllers that do not support explicit persistent connections, this command is prohibited.<br>7.<br>Mandatory for CDCs and optional for Discovery controllers that are not a CDC.<br>8.<br>Refer to the applicable I/O Command Set specification.<br>9.<br>Mandatory for NVMe over PCIe. This command is not supported for NVMe over Fabrics.|Notes:<br>1.<br>O/M/P definition: O = Optional, M = Mandatory, P = Prohibited<br>2.<br>Prohibited if the Keep Alive Timer feature is not supported (refer to section 3.9).<br>3.<br>Prohibited for an Exported NVM Subsystem (refer to section 8.3.3).<br>4.<br>Mandatory if any of the features in Figure 32 are implemented.<br>5.<br>Mandatory if Telemetry Log, Firmware Commit, or SMART/Health Critical Warnings are supported.<br>6.<br>For Discovery controllers that support explicit persistent connections, this command is mandatory. For Discovery<br>controllers that do not support explicit persistent connections, this command is prohibited.<br>7.<br>Mandatory for CDCs and optional for Discovery controllers that are not a CDC.<br>8.<br>Refer to the applicable I/O Command Set specification.<br>9.<br>Mandatory for NVMe over PCIe. This command is not supported for NVMe over Fabrics.|Notes:<br>1.<br>O/M/P definition: O = Optional, M = Mandatory, P = Prohibited<br>2.<br>Prohibited if the Keep Alive Timer feature is not supported (refer to section 3.9).<br>3.<br>Prohibited for an Exported NVM Subsystem (refer to section 8.3.3).<br>4.<br>Mandatory if any of the features in Figure 32 are implemented.<br>5.<br>Mandatory if Telemetry Log, Firmware Commit, or SMART/Health Critical Warnings are supported.<br>6.<br>For Discovery controllers that support explicit persistent connections, this command is mandatory. For Discovery<br>controllers that do not support explicit persistent connections, this command is prohibited.<br>7.<br>Mandatory for CDCs and optional for Discovery controllers that are not a CDC.<br>8.<br>Refer to the applicable I/O Command Set specification.<br>9.<br>Mandatory for NVMe over PCIe. This command is not supported for NVMe over Fabrics.|Notes:<br>1.<br>O/M/P definition: O = Optional, M = Mandatory, P = Prohibited<br>2.<br>Prohibited if the Keep Alive Timer feature is not supported (refer to section 3.9).<br>3.<br>Prohibited for an Exported NVM Subsystem (refer to section 8.3.3).<br>4.<br>Mandatory if any of the features in Figure 32 are implemented.<br>5.<br>Mandatory if Telemetry Log, Firmware Commit, or SMART/Health Critical Warnings are supported.<br>6.<br>For Discovery controllers that support explicit persistent connections, this command is mandatory. For Discovery<br>controllers that do not support explicit persistent connections, this command is prohibited.<br>7.<br>Mandatory for CDCs and optional for Discovery controllers that are not a CDC.<br>8.<br>Refer to the applicable I/O Command Set specification.<br>9.<br>Mandatory for NVMe over PCIe. This command is not supported for NVMe over Fabrics.|Notes:<br>1.<br>O/M/P definition: O = Optional, M = Mandatory, P = Prohibited<br>2.<br>Prohibited if the Keep Alive Timer feature is not supported (refer to section 3.9).<br>3.<br>Prohibited for an Exported NVM Subsystem (refer to section 8.3.3).<br>4.<br>Mandatory if any of the features in Figure 32 are implemented.<br>5.<br>Mandatory if Telemetry Log, Firmware Commit, or SMART/Health Critical Warnings are supported.<br>6.<br>For Discovery controllers that support explicit persistent connections, this command is mandatory. For Discovery<br>controllers that do not support explicit persistent connections, this command is prohibited.<br>7.<br>Mandatory for CDCs and optional for Discovery controllers that are not a CDC.<br>8.<br>Refer to the applicable I/O Command Set specification.<br>9.<br>Mandatory for NVMe over PCIe. This command is not supported for NVMe over Fabrics.|


**Figure 29: Fabrics Command Support Requirements**














|Command|Opcode<br>Value|Fabrics<br>Command<br>Type|1, 2<br>Controller Support Requirements|Col5|Col6|Reference|
|---|---|---|---|---|---|---|
|**Command**|**Opcode**<br>**Value**|**Fabrics**<br>**Command**<br>**Type**|**I/O**|Administrative|**Discovery**|**Discovery**|
|Property Set|**7Fh**|00h|M|M|M|6.6|
|Connect|Connect|01h|M|M|M|6.3|
|Property Get|Property Get|04h|M|M|M|6.5|
|Authentication Send|Authentication Send|05h|O|O|O|6.2|
|Authentication Receive|Authentication Receive|06h|O|O|O|6.1|
|Disconnect|Disconnect|08h|O|P|P|6.4|
|**Vendor Specific**|**Vendor Specific**|**Vendor Specific**|**Vendor Specific**|**Vendor Specific**|**Vendor Specific**|**Vendor Specific**|
|Vendor Specific|**7Fh**|C0h to FFh|O|O|O||
|Notes:<br>1.<br>O/M/P definition: O = Optional, M = Mandatory, P = Prohibited<br>2.<br>For NVMe over PCIe implementations, all Fabrics commands are prohibited. For NVMe over Fabrics<br>implementations, the commands are as noted in the table.|Notes:<br>1.<br>O/M/P definition: O = Optional, M = Mandatory, P = Prohibited<br>2.<br>For NVMe over PCIe implementations, all Fabrics commands are prohibited. For NVMe over Fabrics<br>implementations, the commands are as noted in the table.|Notes:<br>1.<br>O/M/P definition: O = Optional, M = Mandatory, P = Prohibited<br>2.<br>For NVMe over PCIe implementations, all Fabrics commands are prohibited. For NVMe over Fabrics<br>implementations, the commands are as noted in the table.|Notes:<br>1.<br>O/M/P definition: O = Optional, M = Mandatory, P = Prohibited<br>2.<br>For NVMe over PCIe implementations, all Fabrics commands are prohibited. For NVMe over Fabrics<br>implementations, the commands are as noted in the table.|Notes:<br>1.<br>O/M/P definition: O = Optional, M = Mandatory, P = Prohibited<br>2.<br>For NVMe over PCIe implementations, all Fabrics commands are prohibited. For NVMe over Fabrics<br>implementations, the commands are as noted in the table.|Notes:<br>1.<br>O/M/P definition: O = Optional, M = Mandatory, P = Prohibited<br>2.<br>For NVMe over PCIe implementations, all Fabrics commands are prohibited. For NVMe over Fabrics<br>implementations, the commands are as noted in the table.|Notes:<br>1.<br>O/M/P definition: O = Optional, M = Mandatory, P = Prohibited<br>2.<br>For NVMe over PCIe implementations, all Fabrics commands are prohibited. For NVMe over Fabrics<br>implementations, the commands are as noted in the table.|



44


NVM Express [®] Base Specification, Revision 2.2


**Figure 30: Common I/O Command Support Requirements**













|Command|Combined<br>Opcode<br>Value|1<br>Controller Support Requirements|Col4|Col5|Reference|
|---|---|---|---|---|---|
|**Command**|**Combined**<br>**Opcode**<br>**Value**|**I/O**|Administrative|**Discovery**|**Discovery**|
|Flush|00h|M|P|P|7.2|
|Reservation Register|0Dh|O 2|P|P|7.6|
|Reservation Report|0Eh|O 2|P|P|7.8|
|Reservation Acquire|11h|O 2|P|P|7.5|
|I/O Management Receive|12h|O 3|P|P|7.3|
|Reservation Release|15h|O 2|P|P|7.7|
|Cancel|18h|O|P|P|7.1|
|I/O Management Send|1Dh|O 3|P|P|7.4|
|**Vendor Specific**|**Vendor Specific**|**Vendor Specific**|**Vendor Specific**|**Vendor Specific**|**Vendor Specific**|
|Vendor Specific||O|O|O||
|Notes:<br>1.<br>O/M/P definition: O = Optional, M = Mandatory, P = Prohibited<br>2.<br>Mandatory if reservations are supported as indicated in the Identify Controller data structure.<br>3.<br>Mandatory for controllers that support the Flexible Data Placement capability (refer to section 8.1.10). Refer to<br>the FDPS bit in Figure 313.|Notes:<br>1.<br>O/M/P definition: O = Optional, M = Mandatory, P = Prohibited<br>2.<br>Mandatory if reservations are supported as indicated in the Identify Controller data structure.<br>3.<br>Mandatory for controllers that support the Flexible Data Placement capability (refer to section 8.1.10). Refer to<br>the FDPS bit in Figure 313.|Notes:<br>1.<br>O/M/P definition: O = Optional, M = Mandatory, P = Prohibited<br>2.<br>Mandatory if reservations are supported as indicated in the Identify Controller data structure.<br>3.<br>Mandatory for controllers that support the Flexible Data Placement capability (refer to section 8.1.10). Refer to<br>the FDPS bit in Figure 313.|Notes:<br>1.<br>O/M/P definition: O = Optional, M = Mandatory, P = Prohibited<br>2.<br>Mandatory if reservations are supported as indicated in the Identify Controller data structure.<br>3.<br>Mandatory for controllers that support the Flexible Data Placement capability (refer to section 8.1.10). Refer to<br>the FDPS bit in Figure 313.|Notes:<br>1.<br>O/M/P definition: O = Optional, M = Mandatory, P = Prohibited<br>2.<br>Mandatory if reservations are supported as indicated in the Identify Controller data structure.<br>3.<br>Mandatory for controllers that support the Flexible Data Placement capability (refer to section 8.1.10). Refer to<br>the FDPS bit in Figure 313.|Notes:<br>1.<br>O/M/P definition: O = Optional, M = Mandatory, P = Prohibited<br>2.<br>Mandatory if reservations are supported as indicated in the Identify Controller data structure.<br>3.<br>Mandatory for controllers that support the Flexible Data Placement capability (refer to section 8.1.10). Refer to<br>the FDPS bit in Figure 313.|


**Log Page Support Requirements**


Figure 31 defines log pages that are mandatory, optional, and prohibited for an I/O controller, Administrative
controller, and Discovery controller. I/O Command Set specific log page support requirements are
described within individual I/O Command Set specifications.


**Figure 31: Log Page Support Requirements**







|Log Page Name|Log Page<br>Identifier|1<br>Controller Support Requirements|Col4|Col5|Reference|
|---|---|---|---|---|---|
|**Log Page Name**|**Log Page**<br>**Identifier**|**I/O**|**Administrative**|**Discovery**|**Discovery**|
|Supported Log Pages|00h|M3|M3|M|5.1.12.1.1|
|Error Information|01h|M|M|O|5.1.12.1.2|
|SMART / Health Information<br>(Controller scope)|02h|M|O|P|5.1.12.1.3|
|SMART / Health Information<br>(Namespace scope)|02h|O|O|P|P|
|Firmware Slot Information|03h|M|O|P|5.1.12.1.4|
|Changed Attached Namespace List|04h|O|O|P|5.1.12.1.5|
|Commands Supported and Effects|05h|M3|M|M|5.1.12.1.6|
|Device Self-test|06h|O|O|P|5.1.12.1.7|
|Telemetry Host-Initiated|07h|O|O|P|5.1.12.1.8|
|Telemetry Controller-Initiated|08h|O|O8|P|5.1.12.1.9|
|Endurance Group Information|09h|O||P|5.1.12.1.10|
|Predictable Latency Per NVM Set|0Ah|O|O8|P|5.1.12.1.11|
|Predictable Latency Event Aggregate|0Bh|O|O8|P|5.1.12.1.12|
|Asymmetric Namespace Access|0Ch|O|P|P|5.1.12.1.13|
|Persistent Event|0Dh|O|O|P|5.1.12.1.14|
|LBA Status Information|0Eh|Refer to the NVM Command Set Specification|Refer to the NVM Command Set Specification|Refer to the NVM Command Set Specification|Refer to the NVM Command Set Specification|
|Endurance Group Event Aggregate|0Fh|O|O|P|5.1.12.1.15|
|Media Unit Status|10h|O2|P|P|5.1.12.1.16|
|Supported Capacity Configuration List|11h|O2|P|P|5.1.12.1.17|


45


NVM Express [®] Base Specification, Revision 2.2


**Figure 31: Log Page Support Requirements**









|Log Page Name|Log Page<br>Identifier|1<br>Controller Support Requirements|Col4|Col5|Reference|
|---|---|---|---|---|---|
|**Log Page Name**|**Log Page**<br>**Identifier**|**I/O**|**Administrative**|**Discovery**|**Discovery**|
|Feature Identifiers Supported and<br>Effects|12h|M3|M3,9|M9|5.1.12.1.18|
|NVMe-MI Commands Supported and<br>Effects|13h|M3,7|M3,7|O|5.1.12.1.19|
|Command and Feature Lockdown|14h|O|O|P|5.1.12.1.20|
|Boot Partition|15h|O|O|P|5.1.12.1.21|
|Rotational Media Information|16h|O|P|P|5.1.12.1.22|
|Dispersed Namespace Participating<br>NVM Subsystems|17h|O|O|P|5.1.12.1.23|
|Management Address List|18h|O|O|O|5.1.12.1.24|
|Physical Interface Receiver Eye<br>Opening Measurement|19h|O4|O4|P|Note 11|
|Reachability Groups|1Ah|M6|P|P|5.1.12.1.25|
|Reachability Associations|1Bh|M6|P|P|5.1.12.1.26|
|Changed Allocated Namespace List|1Ch|O|O|P|5.1.12.1.27|
|FDP Configurations|20h|O5|P|P|5.1.12.1.28|
|Reclaim Unit Handle Usage|21h|O5|P|P|5.1.12.1.29|
|FDP Statistics|22h|O5|P|P|5.1.12.1.30|
|FDP Events|23h|O5|P|P|5.1.12.1.31|
|Discovery|70h|P|P|M|5.1.12.3.1|
|Host Discovery|71h|P|P|O|5.1.12.3.2|
|AVE Discovery|72h|P|P|O|5.1.12.3.3|
|Pull Model DDC Request|73h|P|P|M10|5.1.12.3.4|
|Reservation Notification|80h|O|P|P|5.1.12.1.32|
|Sanitize Status|81h|O|O8|P|5.1.12.1.33|
|Program List|82h|Refer to the Computational Programs Command Set<br>Specification|Refer to the Computational Programs Command Set<br>Specification|Refer to the Computational Programs Command Set<br>Specification|Refer to the Computational Programs Command Set<br>Specification|
|Downloadable Program Types List|83h|83h|83h|83h|83h|
|Memory Range Set List|84h|84h|84h|84h|84h|
||85h to BEh|Refer to the applicable I/O Command Set specification|Refer to the applicable I/O Command Set specification|Refer to the applicable I/O Command Set specification|Refer to the applicable I/O Command Set specification|
|Changed Zone List|BFh|Refer to the Zoned Namespace Command Set<br>Specification|Refer to the Zoned Namespace Command Set<br>Specification|Refer to the Zoned Namespace Command Set<br>Specification|Refer to the Zoned Namespace Command Set<br>Specification|
|Vendor Specific|C0h to FFh|||||
|Notes:<br>1.<br>O/M/P definition: O = Optional, M = Mandatory, P = Prohibited<br>2.<br>Mandatory for controllers that support Fixed Capacity Management (refer to section 8.1.4.2).<br>3.<br>Optional for NVM Express revision 1.4 and earlier.<br>4.<br>If this log page is not described for a specific physical interface (refer to the applicable NVM Express transport<br>specification), then this log page is prohibited for that transport.<br>5.<br>Mandatory for controllers that support the Flexible Data Placement capability (refer to section 8.1.10). Refer to<br>the FDPS bit in Figure 313.<br>6.<br>Optional for controllers that do not support Reachability Reporting (refer to section 8.1.19).<br>7.<br>Optional if the NVMe-MI Send command and the NVMe-MI Receive command are not supported (refer to Figure<br>28).<br>8.<br>Prohibited for an Exported NVM subsystem (refer to section 8.3.3).<br>9.<br>Optional if the Set Features command is not supported (refer to Figure 28).<br>10. Mandatory for CDCs and prohibited for Discovery controllers that are not a CDC.<br>11. Refer to the applicable NVM Express transport specification.|Notes:<br>1.<br>O/M/P definition: O = Optional, M = Mandatory, P = Prohibited<br>2.<br>Mandatory for controllers that support Fixed Capacity Management (refer to section 8.1.4.2).<br>3.<br>Optional for NVM Express revision 1.4 and earlier.<br>4.<br>If this log page is not described for a specific physical interface (refer to the applicable NVM Express transport<br>specification), then this log page is prohibited for that transport.<br>5.<br>Mandatory for controllers that support the Flexible Data Placement capability (refer to section 8.1.10). Refer to<br>the FDPS bit in Figure 313.<br>6.<br>Optional for controllers that do not support Reachability Reporting (refer to section 8.1.19).<br>7.<br>Optional if the NVMe-MI Send command and the NVMe-MI Receive command are not supported (refer to Figure<br>28).<br>8.<br>Prohibited for an Exported NVM subsystem (refer to section 8.3.3).<br>9.<br>Optional if the Set Features command is not supported (refer to Figure 28).<br>10. Mandatory for CDCs and prohibited for Discovery controllers that are not a CDC.<br>11. Refer to the applicable NVM Express transport specification.|Notes:<br>1.<br>O/M/P definition: O = Optional, M = Mandatory, P = Prohibited<br>2.<br>Mandatory for controllers that support Fixed Capacity Management (refer to section 8.1.4.2).<br>3.<br>Optional for NVM Express revision 1.4 and earlier.<br>4.<br>If this log page is not described for a specific physical interface (refer to the applicable NVM Express transport<br>specification), then this log page is prohibited for that transport.<br>5.<br>Mandatory for controllers that support the Flexible Data Placement capability (refer to section 8.1.10). Refer to<br>the FDPS bit in Figure 313.<br>6.<br>Optional for controllers that do not support Reachability Reporting (refer to section 8.1.19).<br>7.<br>Optional if the NVMe-MI Send command and the NVMe-MI Receive command are not supported (refer to Figure<br>28).<br>8.<br>Prohibited for an Exported NVM subsystem (refer to section 8.3.3).<br>9.<br>Optional if the Set Features command is not supported (refer to Figure 28).<br>10. Mandatory for CDCs and prohibited for Discovery controllers that are not a CDC.<br>11. Refer to the applicable NVM Express transport specification.|Notes:<br>1.<br>O/M/P definition: O = Optional, M = Mandatory, P = Prohibited<br>2.<br>Mandatory for controllers that support Fixed Capacity Management (refer to section 8.1.4.2).<br>3.<br>Optional for NVM Express revision 1.4 and earlier.<br>4.<br>If this log page is not described for a specific physical interface (refer to the applicable NVM Express transport<br>specification), then this log page is prohibited for that transport.<br>5.<br>Mandatory for controllers that support the Flexible Data Placement capability (refer to section 8.1.10). Refer to<br>the FDPS bit in Figure 313.<br>6.<br>Optional for controllers that do not support Reachability Reporting (refer to section 8.1.19).<br>7.<br>Optional if the NVMe-MI Send command and the NVMe-MI Receive command are not supported (refer to Figure<br>28).<br>8.<br>Prohibited for an Exported NVM subsystem (refer to section 8.3.3).<br>9.<br>Optional if the Set Features command is not supported (refer to Figure 28).<br>10. Mandatory for CDCs and prohibited for Discovery controllers that are not a CDC.<br>11. Refer to the applicable NVM Express transport specification.|Notes:<br>1.<br>O/M/P definition: O = Optional, M = Mandatory, P = Prohibited<br>2.<br>Mandatory for controllers that support Fixed Capacity Management (refer to section 8.1.4.2).<br>3.<br>Optional for NVM Express revision 1.4 and earlier.<br>4.<br>If this log page is not described for a specific physical interface (refer to the applicable NVM Express transport<br>specification), then this log page is prohibited for that transport.<br>5.<br>Mandatory for controllers that support the Flexible Data Placement capability (refer to section 8.1.10). Refer to<br>the FDPS bit in Figure 313.<br>6.<br>Optional for controllers that do not support Reachability Reporting (refer to section 8.1.19).<br>7.<br>Optional if the NVMe-MI Send command and the NVMe-MI Receive command are not supported (refer to Figure<br>28).<br>8.<br>Prohibited for an Exported NVM subsystem (refer to section 8.3.3).<br>9.<br>Optional if the Set Features command is not supported (refer to Figure 28).<br>10. Mandatory for CDCs and prohibited for Discovery controllers that are not a CDC.<br>11. Refer to the applicable NVM Express transport specification.|Notes:<br>1.<br>O/M/P definition: O = Optional, M = Mandatory, P = Prohibited<br>2.<br>Mandatory for controllers that support Fixed Capacity Management (refer to section 8.1.4.2).<br>3.<br>Optional for NVM Express revision 1.4 and earlier.<br>4.<br>If this log page is not described for a specific physical interface (refer to the applicable NVM Express transport<br>specification), then this log page is prohibited for that transport.<br>5.<br>Mandatory for controllers that support the Flexible Data Placement capability (refer to section 8.1.10). Refer to<br>the FDPS bit in Figure 313.<br>6.<br>Optional for controllers that do not support Reachability Reporting (refer to section 8.1.19).<br>7.<br>Optional if the NVMe-MI Send command and the NVMe-MI Receive command are not supported (refer to Figure<br>28).<br>8.<br>Prohibited for an Exported NVM subsystem (refer to section 8.3.3).<br>9.<br>Optional if the Set Features command is not supported (refer to Figure 28).<br>10. Mandatory for CDCs and prohibited for Discovery controllers that are not a CDC.<br>11. Refer to the applicable NVM Express transport specification.|


46


NVM Express [®] Base Specification, Revision 2.2


**Feature Support Requirements**


Figure 32 defines features that are mandatory, optional, and prohibited for an I/O controller, Administrative
controller, and Discovery controller. If any feature is supported, then the Set Features command and the
Get Features command shall be supported. I/O Command Set specific feature support requirements are
described within individual I/O Command Set specifications.


**Figure 32: Feature Support Requirements**







|Feature Name|Feature<br>Identifier|1<br>Controller Support Requirements|Col4|Col5|Reference|
|---|---|---|---|---|---|
|**Feature Name**|**Feature**<br>**Identifier**|**I/O**|**Administrative**|**Discovery**|**Discovery**|
|Arbitration|01h|M|P|P|5.1.25.1.1|
|Power Management|02h|M|O|P|5.1.25.1.2|
|LBA Range Type|03h|Refer to the NVM Command Set Specification|Refer to the NVM Command Set Specification|Refer to the NVM Command Set Specification|Refer to the NVM Command Set Specification|
|Temperature Threshold|04h|M|O|P|5.1.25.1.3|
|Error Recovery|05h|Refer to the NVM Command Set Specification|Refer to the NVM Command Set Specification|Refer to the NVM Command Set Specification|Refer to the NVM Command Set Specification|
|Volatile Write Cache|06h|O|P|P|5.1.25.1.4|
|Number of Queues|07h|M|P|P|5.1.25.2.1|
|Interrupt Coalescing|08h|Note 2|Note 2|P|5.1.25.2.2|
|Interrupt Vector Configuration|09h|Note 2|Note 2|P|5.1.25.2.3|
|Write Atomicity Normal|0Ah|Refer to the NVM Command Set Specification|Refer to the NVM Command Set Specification|Refer to the NVM Command Set Specification|Refer to the NVM Command Set Specification|
|Asynchronous Event Configuration|0Bh|M|O8|M10|5.1.25.1.5|
|Autonomous Power State Transition|0Ch|O|O|P|5.1.25.1.6|
|Host Memory Buffer|0Dh|O|O|P|5.1.25.2.4|
|Timestamp|0Eh|O|O|P|5.1.25.1.7|
|Keep Alive Timer|0Fh|M7|M7|M10|5.1.25.1.8|
|Host Controlled Thermal Management|10h|O|O|P|5.1.25.1.9|
|Non-Operational Power State Config|11h|O|O|P|5.1.25.1.10|
|Read Recovery Level Config|12h|O|O|P|5.1.25.1.11|
|Predictable Latency Mode Config|13h|O|O9|P|5.1.25.1.12|
|Predictable Latency Mode Window|14h|O|O9|P|5.1.25.1.13|
|LBA Status Information Report Interval|15h|Refer to the NVM Command Set Specification|Refer to the NVM Command Set Specification|Refer to the NVM Command Set Specification|Refer to the NVM Command Set Specification|
|Host Behavior Support|16h|O|O|P|5.1.25.1.14|
|Sanitize Config|17h|O|O9|P|5.1.25.1.15|
|Endurance Group Event Configuration|18h|O|O9|P|5.1.25.1.16|
|I/O Command Set Profile|19h|O|P|P|5.1.25.1.17|
|Spinup Control|1Ah|O|P|P|5.1.25.1.18|
|Power Loss Signaling Config|1Bh|O|O|P|5.1.25.1.19|
|Performance Characteristics|1Ch|Refer to the NVM Command Set Specification|Refer to the NVM Command Set Specification|Refer to the NVM Command Set Specification|Refer to the NVM Command Set Specification|
|Flexible Data Placement|1Dh|O6|P|P|5.1.25.1.20|
|Flexible Data Placement Events|1Eh|O6|P|P|5.1.25.1.21|
|Namespace Admin Label|1Fh|O|O|P|5.1.25.1.22|
|Key Value Configuration|20h|Refer to the Key Value Command Set Specification|Refer to the Key Value Command Set Specification|Refer to the Key Value Command Set Specification|Refer to the Key Value Command Set Specification|
|Controller Data Queue|21h|O|O|P|5.1.25.1.23|
|Embedded Management Controller<br>Address|78h|O|O|O|5.1.25.1.24|
|Host Management Agent Address|79h|O|O|O|5.1.25.1.25|
|Enhanced Controller Metadata|7Dh|O5|O5|O|5.1.25.1.26.1|
|Controller Metadata|7Eh|O5|O5|O|5.1.25.1.26.2|
|Namespace Metadata|7Fh|O5|O5|O|5.1.25.1.26.3|
|Software Progress Marker|80h|O|O|P|5.1.25.1.27|
|Host Identifier|81h|O3|O|P|5.1.25.1.28|


47


NVM Express [®] Base Specification, Revision 2.2


**Figure 32: Feature Support Requirements**







|Feature Name|Feature<br>Identifier|1<br>Controller Support Requirements|Col4|Col5|Reference|
|---|---|---|---|---|---|
|**Feature Name**|**Feature**<br>**Identifier**|**I/O**|**Administrative**|**Discovery**|**Discovery**|
|Reservation Notification Mask|82h|O4|P|P|5.1.25.1.29|
|Reservation Persistence|83h|O4|P|P|5.1.25.1.30|
|Namespace Write Protection Config|84h|O|O|P|5.1.25.1.31|
|Boot Partition Write Protection Config|85h|O|O|P|5.1.25.1.32|
|Notes:<br>1.<br>O/M/P definition: O = Optional, M = Mandatory, P = Prohibited<br>2.<br>Mandatory for NVMe over PCIe. This feature is not supported for NVMe over Fabrics.<br>3.<br>Mandatory if reservations are supported as indicated in the Identify Controller data structure.<br>4.<br>Mandatory if reservations are supported by the namespace as indicated by a non-zero value in the Reservation<br>Capabilities (RESCAP) field in the Identify Namespace data structure.<br>5.<br>Optional for NVM subsystems that do not implement a Management Endpoint. For NVM subsystems that<br>implement any Management Endpoint refer to the NVM Express Management Interface Specification.<br>6.<br>Mandatory for controllers that support the Flexible Data Placement capability (refer to section 8.1.10). Refer to<br>the FDPS bit in Figure 313.<br>7.<br>Optional if not required by the NVMe Transport (refer to section 3.9).<br>8.<br>Mandatory if Telemetry Log, Firmware Commit or SMART/Health Critical Warnings are supported.<br>9.<br>Prohibited for an Exported NVM Subsystem (refer to section 8.3.3).<br>10. For Discovery controllers that support explicit persistent connections, this feature is mandatory. For Discovery<br>controllers that do not support explicit persistent connections, this feature is prohibited.|Notes:<br>1.<br>O/M/P definition: O = Optional, M = Mandatory, P = Prohibited<br>2.<br>Mandatory for NVMe over PCIe. This feature is not supported for NVMe over Fabrics.<br>3.<br>Mandatory if reservations are supported as indicated in the Identify Controller data structure.<br>4.<br>Mandatory if reservations are supported by the namespace as indicated by a non-zero value in the Reservation<br>Capabilities (RESCAP) field in the Identify Namespace data structure.<br>5.<br>Optional for NVM subsystems that do not implement a Management Endpoint. For NVM subsystems that<br>implement any Management Endpoint refer to the NVM Express Management Interface Specification.<br>6.<br>Mandatory for controllers that support the Flexible Data Placement capability (refer to section 8.1.10). Refer to<br>the FDPS bit in Figure 313.<br>7.<br>Optional if not required by the NVMe Transport (refer to section 3.9).<br>8.<br>Mandatory if Telemetry Log, Firmware Commit or SMART/Health Critical Warnings are supported.<br>9.<br>Prohibited for an Exported NVM Subsystem (refer to section 8.3.3).<br>10. For Discovery controllers that support explicit persistent connections, this feature is mandatory. For Discovery<br>controllers that do not support explicit persistent connections, this feature is prohibited.|Notes:<br>1.<br>O/M/P definition: O = Optional, M = Mandatory, P = Prohibited<br>2.<br>Mandatory for NVMe over PCIe. This feature is not supported for NVMe over Fabrics.<br>3.<br>Mandatory if reservations are supported as indicated in the Identify Controller data structure.<br>4.<br>Mandatory if reservations are supported by the namespace as indicated by a non-zero value in the Reservation<br>Capabilities (RESCAP) field in the Identify Namespace data structure.<br>5.<br>Optional for NVM subsystems that do not implement a Management Endpoint. For NVM subsystems that<br>implement any Management Endpoint refer to the NVM Express Management Interface Specification.<br>6.<br>Mandatory for controllers that support the Flexible Data Placement capability (refer to section 8.1.10). Refer to<br>the FDPS bit in Figure 313.<br>7.<br>Optional if not required by the NVMe Transport (refer to section 3.9).<br>8.<br>Mandatory if Telemetry Log, Firmware Commit or SMART/Health Critical Warnings are supported.<br>9.<br>Prohibited for an Exported NVM Subsystem (refer to section 8.3.3).<br>10. For Discovery controllers that support explicit persistent connections, this feature is mandatory. For Discovery<br>controllers that do not support explicit persistent connections, this feature is prohibited.|Notes:<br>1.<br>O/M/P definition: O = Optional, M = Mandatory, P = Prohibited<br>2.<br>Mandatory for NVMe over PCIe. This feature is not supported for NVMe over Fabrics.<br>3.<br>Mandatory if reservations are supported as indicated in the Identify Controller data structure.<br>4.<br>Mandatory if reservations are supported by the namespace as indicated by a non-zero value in the Reservation<br>Capabilities (RESCAP) field in the Identify Namespace data structure.<br>5.<br>Optional for NVM subsystems that do not implement a Management Endpoint. For NVM subsystems that<br>implement any Management Endpoint refer to the NVM Express Management Interface Specification.<br>6.<br>Mandatory for controllers that support the Flexible Data Placement capability (refer to section 8.1.10). Refer to<br>the FDPS bit in Figure 313.<br>7.<br>Optional if not required by the NVMe Transport (refer to section 3.9).<br>8.<br>Mandatory if Telemetry Log, Firmware Commit or SMART/Health Critical Warnings are supported.<br>9.<br>Prohibited for an Exported NVM Subsystem (refer to section 8.3.3).<br>10. For Discovery controllers that support explicit persistent connections, this feature is mandatory. For Discovery<br>controllers that do not support explicit persistent connections, this feature is prohibited.|Notes:<br>1.<br>O/M/P definition: O = Optional, M = Mandatory, P = Prohibited<br>2.<br>Mandatory for NVMe over PCIe. This feature is not supported for NVMe over Fabrics.<br>3.<br>Mandatory if reservations are supported as indicated in the Identify Controller data structure.<br>4.<br>Mandatory if reservations are supported by the namespace as indicated by a non-zero value in the Reservation<br>Capabilities (RESCAP) field in the Identify Namespace data structure.<br>5.<br>Optional for NVM subsystems that do not implement a Management Endpoint. For NVM subsystems that<br>implement any Management Endpoint refer to the NVM Express Management Interface Specification.<br>6.<br>Mandatory for controllers that support the Flexible Data Placement capability (refer to section 8.1.10). Refer to<br>the FDPS bit in Figure 313.<br>7.<br>Optional if not required by the NVMe Transport (refer to section 3.9).<br>8.<br>Mandatory if Telemetry Log, Firmware Commit or SMART/Health Critical Warnings are supported.<br>9.<br>Prohibited for an Exported NVM Subsystem (refer to section 8.3.3).<br>10. For Discovery controllers that support explicit persistent connections, this feature is mandatory. For Discovery<br>controllers that do not support explicit persistent connections, this feature is prohibited.|Notes:<br>1.<br>O/M/P definition: O = Optional, M = Mandatory, P = Prohibited<br>2.<br>Mandatory for NVMe over PCIe. This feature is not supported for NVMe over Fabrics.<br>3.<br>Mandatory if reservations are supported as indicated in the Identify Controller data structure.<br>4.<br>Mandatory if reservations are supported by the namespace as indicated by a non-zero value in the Reservation<br>Capabilities (RESCAP) field in the Identify Namespace data structure.<br>5.<br>Optional for NVM subsystems that do not implement a Management Endpoint. For NVM subsystems that<br>implement any Management Endpoint refer to the NVM Express Management Interface Specification.<br>6.<br>Mandatory for controllers that support the Flexible Data Placement capability (refer to section 8.1.10). Refer to<br>the FDPS bit in Figure 313.<br>7.<br>Optional if not required by the NVMe Transport (refer to section 3.9).<br>8.<br>Mandatory if Telemetry Log, Firmware Commit or SMART/Health Critical Warnings are supported.<br>9.<br>Prohibited for an Exported NVM Subsystem (refer to section 8.3.3).<br>10. For Discovery controllers that support explicit persistent connections, this feature is mandatory. For Discovery<br>controllers that do not support explicit persistent connections, this feature is prohibited.|


**Controller Properties**


A property is a dword, or qword attribute of a controller. The attribute may have read, write, or read/write
access. The host shall access a property using the width specified for that property with an offset that is at
the beginning of the property unless otherwise noted in a transport specific specification. All reserved
properties and all reserved bits within properties are read-only and return 0h when read.


For message-based controllers, properties may be read with the Property Get command and may be written
with the Property Set command.


For memory-based controllers, refer to the applicable NVMe Transport binding specification for access
methods and rules (e.g., NVMe PCIe Transport Specification).


Figure 33 describes the property map for the controller.


Accesses that target any portion of two or more properties are not supported.


Software should not rely on 0h being returned.


**Figure 33: Property Definition**













|Offset<br>(OFST)|Size<br>(in<br>bytes)|I/O<br>1<br>Controller|Administrative<br>1<br>Controller|Discovery<br>1<br>Controller|Name|
|---|---|---|---|---|---|
|0h|8|M|M|M|**CAP:**Controller Capabilities|
|8h|4|M|M|M|**VS:**Version|
|Ch|4|M2|M2|R|**INTMS:**Interrupt Mask Set|
|Fh|4|M2|M2|R|**INTMC:**Interrupt Mask Clear|
|14h|4|M|M|M|**CC:**Controller Configuration|
|18h||R|R|R|Reserved|
|1Ch|4|M|M|M|**CSTS:**Controller Status|
|20h|4|O|O|R|**NSSR:**NVM Subsystem Reset|
|24h|4|M2|M2|R|**AQA:**Admin Queue Attributes|


48


NVM Express [®] Base Specification, Revision 2.2


**Figure 33: Property Definition**













|Offset<br>(OFST)|Size<br>(in<br>bytes)|I/O<br>1<br>Controller|Administrative<br>1<br>Controller|Discovery<br>1<br>Controller|Name|
|---|---|---|---|---|---|
|28h|8|M2|M2|R|**ASQ:**Admin Submission Queue Base<br>Address|
|30h|8|M2|M2|R|**ACQ:**Admin Completion Queue Base<br>Address|
|38h|4|O3|O3|R|**CMBLOC:**Controller Memory Buffer<br>Location|
|3Ch|4|O3|O3|R|**CMBSZ:**Controller Memory Buffer Size|
|40h|4|O3|O3|R|**BPINFO:**Boot Partition Information|
|44h|4|O3|O3|R|**BPRSEL:**Boot Partition Read Select|
|48h|8|O3|O3|R|**BPMBL:**Boot Partition Memory Buffer<br>Location|
|50h|8|O3|O3|R|**CMBMSC:**Controller Memory Buffer<br>Memory Space Control|
|58h|4|O3|O3|R|**CMBSTS:**Controller Memory Buffer<br>Status|
|5Ch|4|O3|O3|R|**CMBEBS:**Controller Memory Buffer<br>Elasticity Buffer Size|
|60h|4|O3|O3|R|**CMBSWTP:**Controller Memory Buffer<br>Sustained Write Throughput|
|64h|4|O|O|R|**NSSD:**NVM Subsystem Shutdown|
|68h|4|M|M|R|**CRTO:**Controller Ready Timeouts|
|6Ch||R|R|R|Reserved|
|E00h|4|O3|O3|R|**PMRCAP:**Persistent Memory Capabilities|
|E04h|4|O3|O3|R|**PMRCTL:**Persistent Memory Region<br>Control|
|E08h|4|O3|O3|R|**PMRSTS:**Persistent Memory Region<br>Status|
|E0Ch|4|O3|O3|R|**PMREBS:**Persistent Memory Region<br>Elasticity Buffer Size|
|E10h|4|O3|O3|R|**PMRSWTP:**Persistent Memory Region<br>Sustained Write Throughput|
|E14h|4|O3|O3|R|**PMRMSCL:**Persistent Memory Region<br>Controller Memory Space Control Lower|
|E18h|4|O3|O3|R|**PMRMSCU:**Persistent Memory Region<br>Controller Memory Space Control Upper|
|E1Ch||R|R|R|Reserved|
|1000h||Transport Specific:<br>• <br>Refer to Figure 34 for Memory-Based transport implementations.<br>• <br>Refer to Figure 35 for Message-Based transport implementations.|Transport Specific:<br>• <br>Refer to Figure 34 for Memory-Based transport implementations.<br>• <br>Refer to Figure 35 for Message-Based transport implementations.|Transport Specific:<br>• <br>Refer to Figure 34 for Memory-Based transport implementations.<br>• <br>Refer to Figure 35 for Message-Based transport implementations.|Transport Specific:<br>• <br>Refer to Figure 34 for Memory-Based transport implementations.<br>• <br>Refer to Figure 35 for Message-Based transport implementations.|
|Notes:<br>1.<br>O/M/R definition: O = Optional, M = Mandatory, R = Reserved<br>2.<br>Mandatory for memory-based controllers. For message-based controllers this property is reserved.<br>3.<br>Optional for memory-based controllers. For message-based controllers this property is reserved.<br>4.<br>Determined by the transport (e.g., the offset calculation formula Offset (1000h + ((2y) * (4 << CAP.DSTRD))) for<br>the memory-based PCIe transport).|Notes:<br>1.<br>O/M/R definition: O = Optional, M = Mandatory, R = Reserved<br>2.<br>Mandatory for memory-based controllers. For message-based controllers this property is reserved.<br>3.<br>Optional for memory-based controllers. For message-based controllers this property is reserved.<br>4.<br>Determined by the transport (e.g., the offset calculation formula Offset (1000h + ((2y) * (4 << CAP.DSTRD))) for<br>the memory-based PCIe transport).|Notes:<br>1.<br>O/M/R definition: O = Optional, M = Mandatory, R = Reserved<br>2.<br>Mandatory for memory-based controllers. For message-based controllers this property is reserved.<br>3.<br>Optional for memory-based controllers. For message-based controllers this property is reserved.<br>4.<br>Determined by the transport (e.g., the offset calculation formula Offset (1000h + ((2y) * (4 << CAP.DSTRD))) for<br>the memory-based PCIe transport).|Notes:<br>1.<br>O/M/R definition: O = Optional, M = Mandatory, R = Reserved<br>2.<br>Mandatory for memory-based controllers. For message-based controllers this property is reserved.<br>3.<br>Optional for memory-based controllers. For message-based controllers this property is reserved.<br>4.<br>Determined by the transport (e.g., the offset calculation formula Offset (1000h + ((2y) * (4 << CAP.DSTRD))) for<br>the memory-based PCIe transport).|Notes:<br>1.<br>O/M/R definition: O = Optional, M = Mandatory, R = Reserved<br>2.<br>Mandatory for memory-based controllers. For message-based controllers this property is reserved.<br>3.<br>Optional for memory-based controllers. For message-based controllers this property is reserved.<br>4.<br>Determined by the transport (e.g., the offset calculation formula Offset (1000h + ((2y) * (4 << CAP.DSTRD))) for<br>the memory-based PCIe transport).|Notes:<br>1.<br>O/M/R definition: O = Optional, M = Mandatory, R = Reserved<br>2.<br>Mandatory for memory-based controllers. For message-based controllers this property is reserved.<br>3.<br>Optional for memory-based controllers. For message-based controllers this property is reserved.<br>4.<br>Determined by the transport (e.g., the offset calculation formula Offset (1000h + ((2y) * (4 << CAP.DSTRD))) for<br>the memory-based PCIe transport).|


49


NVM Express [®] Base Specification, Revision 2.2


**Figure 34: Memory-Based Property Definition**



















|Offset<br>(OFST)|Size (in<br>bytes)|I/O<br>1<br>Controller|Admin.<br>1<br>Controller|Discovery<br>1<br>Controller|Name|
|---|---|---|---|---|---|
|1000h|Variable2|T|T|T|Transport Specific (e.g., PCIe doorbell<br>registers as specified in the NVMe over<br>PCIe Transport Specification)|
|1000h +<br>Variable2||O|O|O|Vendor Specific|
|Notes:<br>1.<br>O/T definition: O = Optional, T = Transport Specific<br>2.<br>Determined by the transport (e.g., the offset calculation formula Offset (1000h + ((2y) * (4 << CAP.DSTRD)))<br>for the PCIe transport).|Notes:<br>1.<br>O/T definition: O = Optional, T = Transport Specific<br>2.<br>Determined by the transport (e.g., the offset calculation formula Offset (1000h + ((2y) * (4 << CAP.DSTRD)))<br>for the PCIe transport).|Notes:<br>1.<br>O/T definition: O = Optional, T = Transport Specific<br>2.<br>Determined by the transport (e.g., the offset calculation formula Offset (1000h + ((2y) * (4 << CAP.DSTRD)))<br>for the PCIe transport).|Notes:<br>1.<br>O/T definition: O = Optional, T = Transport Specific<br>2.<br>Determined by the transport (e.g., the offset calculation formula Offset (1000h + ((2y) * (4 << CAP.DSTRD)))<br>for the PCIe transport).|Notes:<br>1.<br>O/T definition: O = Optional, T = Transport Specific<br>2.<br>Determined by the transport (e.g., the offset calculation formula Offset (1000h + ((2y) * (4 << CAP.DSTRD)))<br>for the PCIe transport).|Notes:<br>1.<br>O/T definition: O = Optional, T = Transport Specific<br>2.<br>Determined by the transport (e.g., the offset calculation formula Offset (1000h + ((2y) * (4 << CAP.DSTRD)))<br>for the PCIe transport).|


**Figure 35: Message-Based Property Definition**













|Offset<br>(OFST)|Size (in<br>bytes)|I/O<br>1<br>Controller|Admin.<br>1<br>Controller|Discovery<br>1<br>Controller|Name|
|---|---|---|---|---|---|
|1000h|300h|R|R|R|Reserved for Fabrics|
|1300h||O|O|O|Vendor Specific|
|Notes:<br>1.<br>O/R definition: O = Optional, R = Reserved|Notes:<br>1.<br>O/R definition: O = Optional, R = Reserved|Notes:<br>1.<br>O/R definition: O = Optional, R = Reserved|Notes:<br>1.<br>O/R definition: O = Optional, R = Reserved|Notes:<br>1.<br>O/R definition: O = Optional, R = Reserved|Notes:<br>1.<br>O/R definition: O = Optional, R = Reserved|


The following conventions are used to describe controller properties for all transport models. Hardware
shall return ‘0’ for all bits that are marked as reserved, and host software shall write all reserved bits and
properties with the value of 0h.


The following terms and abbreviations are used:


**RO** Read Only
**RW** Read Write
**RWC** Read/Write ‘1’ to clear
**RWS** Read/Write ‘1’ to set
**Impl Spec** Implementation Specific – the controller has the freedom to choose
its implementation.
**HwInit** The default state is dependent on NVM Express controller and
system configuration.
**Reset** This column indicates the value of the field after a Controller Level
Reset as defined in section 3.7.2.


For some fields, it is implementation specific as to whether the field is RW, RWC, or RO; this is typically
shown as RW/RO or RWC/RO to indicate that if the functionality is not supported that the field is read only.


When a field is referred to in the document, the convention used is “Property Symbol.Field Symbol”. For
example, the PCI command register Parity Error Response Enable bit is referred to by the name CMD.PEE.
If the field is an array of bits, the field is referred to as “Property Symbol.Field Symbol (array offset to
element)”. When a sub-field is referred to in the document, the convention used is “Property Symbol.Field
Symbol.Sub Field Symbol”. For example, when the Controller Ready With Media Support sub-field of the
Controller Ready Modes Supported field within the Controller Capability property, the sub-field is referred
to by the name CAP.CRMS.CRWMS.


**Offset 0h: CAP – Controller Capabilities**


This property indicates basic capabilities of the controller to host software.


50


NVM Express [®] Base Specification, Revision 2.2


**Figure 36: Offset 0h: CAP – Controller Capabilities**






|Bits|Description|
|---|---|
|1|**Controller Ready Independent of Media Support (CRIMS):**If this bit<br>is set to ‘1’, then the controller supports the Controller Ready<br>Independent of Media mode.<br>If this bit is cleared to ‘0’, then the controller does not support Controller<br>Ready Independent of Media mode.|
|0|**Controller Ready With Media Support (CRWMS):**If this bit is set to<br>‘1’, then the controller supports the Controller Ready With Media mode.<br>If this bit is cleared to ‘0’, then the controller does not support Controller<br>Ready With Media mode.<br>This bit shall be set to ‘1’ on controllers compliant with NVM Express<br>Base Specification, Revision 2.0 and later.|



|Bits|Type|Reset|Description|
|---|---|---|---|
|63:62|RO|0h|Reserved|
|61|RO|Impl<br>Spec|**NVM Subsystem Shutdown Enhancements Supported (NSSES):**This bit<br>indicates whether the controller supports enhancements to the NVM Subsystem<br>Shutdown feature.<br>If the controller supports the enhancements to the NVM Subsystem Shutdown<br>feature as defined in section 3.6.3, then this bit shall be set to ‘1’ and the NSSS bit<br>shall be set to ‘1’. If a controller compliant with a revision of the NVM Express Base<br>Specification later than revision 2.0 sets the NSSS bit to ‘1’, then that controller<br>shall set this bit to ‘1’.<br>If this bit is cleared to ‘0’, then the controller does not support the enhancements to<br>the NVM Subsystem Shutdown feature as defined in section 3.6.3.<br>If the NSSRS bit is cleared to ‘0’ or the NSSS bit is cleared to ‘0’, then this bit shall<br>be cleared to ‘0’.|
|60:59|RO|Impl<br>Spec|**Controller Ready Modes Supported (CRMS):**This field indicates the ready<br>capabilities of the controller. Refer to sections 3.5.3 and 3.5.4 for more detail.<br>**Bits**<br>**Description**<br>1 <br>**Controller Ready Independent of Media Support (CRIMS):**If this bit<br>is set to ‘1’, then the controller supports the Controller Ready<br>Independent of Media mode.<br>If this bit is cleared to ‘0’, then the controller does not support Controller<br>Ready Independent of Media mode.<br>0 <br>**Controller Ready With Media Support (CRWMS):**If this bit is set to<br>‘1’, then the controller supports the Controller Ready With Media mode.<br>If this bit is cleared to ‘0’, then the controller does not support Controller<br>Ready With Media mode.<br>This bit shall be set to ‘1’ on controllers compliant with NVM Express<br>Base Specification, Revision 2.0 and later.|
|58|RO|Impl<br>Spec|**NVM Subsystem Shutdown Supported (NSSS): T**his bit indicates whether the<br>controller supports the NVM Subsystem Shutdown feature.<br>If this bit is set to ‘1’, then the controller supports the NVM Subsystem Shutdown<br>feature. If the NSSES bit is set to ‘1’, then this bit shall be set to ‘1’.<br>If this bit is cleared to ‘0’, then the controller does not support the NVM Subsystem<br>Shutdown feature. If the NSSRS bit is cleared to ‘0’, then this bit shall be cleared<br>to ‘0’.<br>Refer to section 3.6.3 for a description of the NVM Subsystem Shutdown feature<br>and the behavioral enhancements associated with the NSSES bit being set to ‘1’.|
|57|RO|Impl<br>Spec|**Controller Memory Buffer Supported (CMBS):** If this bit is set to ‘1’, then this bit<br>indicates that the controller supports the Controller Memory Buffer, and that<br>addresses supplied by the host are permitted to reference the Controller Memory<br>Buffer only if the host has enabled the Controller Memory Buffer’s controller<br>memory space.<br>If the controller supports the Controller Memory Buffer, then this bit shall be set to<br>‘1’.|
|56|RO|Impl<br>Spec|**Persistent Memory Region Supported (PMRS):** This bit indicates whether the<br>Persistent Memory Region is supported. This bit is set to ‘1’ if the Persistent<br>Memory Region is supported. This bit is cleared to ‘0’ if the Persistent Memory<br>Region is not supported.|


51






NVM Express [®] Base Specification, Revision 2.2


**Figure 36: Offset 0h: CAP – Controller Capabilities**






|Value|Power Scope|
|---|---|
|00b|Not Reported|
|01b|Controller scope|
|10b|Domain scope (i.e., the NVM subsystem supports multiple domains<br>(refer to section 3.2.5).|
|11b|NVM subsystem scope (i.e., the NVM subsystem does not support<br>multiple domains).|


|Bits|Description|
|---|---|
|7|**No I/O Command Set Support (NOIOCSS):** This bit indicates whether<br>no I/O Command Set is supported (i.e., only the Admin Command Set<br>is supported).<br>This bit shall be set to ‘1’ if no I/O Command Set is supported.|
|6|**I/O Command Set Support (IOCSS):** This bit indicates whether the<br>controller supports one or more I/O Command Sets and supports the<br>Identify I/O Command Set data structure (refer to section 5.1.13.2.19).<br>Controllers that support I/O Command Sets other than the NVM<br>Command Set shall set this bit to ‘1’. Controllers that only support the<br>NVM Command Set may set this bit to ‘1’.|
|5:1|Reserved|
|0|**NVM Command Set Support (NCSS):** This bit indicates whether the<br>controller supports the NVM Command Set or a Discovery controller.|



|Bits|Type|Reset|Description|
|---|---|---|---|
|55:52|RO|Impl<br>Spec|**Memory Page Size Maximum (MPSMAX):**This field indicates the maximum host<br>memory page size that the controller supports. The maximum memory page size<br>is (2 ^ (12 + MPSMAX)). The host shall not configure a memory page size in<br>CC.MPS that is larger than this value.<br>For Discovery controllers this field shall be cleared to 0h.|
|51:48|RO|Impl<br>Spec|**Memory Page Size Minimum (MPSMIN):**This field indicates the minimum host<br>memory page size that the controller supports. The minimum memory page size is<br>(2 ^ (12 + MPSMIN)). The host shall not configure a memory page size in CC.MPS<br>that is smaller than this value.<br>For Discovery controllers this shall be cleared to 0h.|
|47:46|RO|Impl<br>Spec|**Controller Power Scope (CPS):** This field indicates scope of controlling the main<br>power for this controller.<br>**Value**<br>**Power Scope**<br>00b<br>Not Reported<br>01b<br>Controller scope<br>10b<br>Domain scope (i.e., the NVM subsystem supports multiple domains<br>(refer to section 3.2.5).<br>11b<br>NVM subsystem scope (i.e., the NVM subsystem does not support<br>multiple domains).<br>If the NSSS bit is set to ‘1’, then this field shall not be cleared to 00b.|
|45|RO|Impl<br>Spec|**Boot Partition Support (BPS):**This bit indicates whether the controller supports<br>Boot Partitions. If this bit is set to '1‘, then the controller supports Boot Partitions. If<br>this bit is cleared to ‘0‘, then the controller does not support Boot Partitions. Refer<br>to section 8.1.3.|
|44:37|RO|Impl<br>Spec|**Command Sets Supported (CSS):**This field indicates the I/O Command Set(s)<br>that the controller supports.<br>For Discovery controllers, this field should have only the NCSS bit set to 1.<br>**Bits**<br>**Description**<br>7 <br>**No I/O Command Set Support (NOIOCSS):** This bit indicates whether<br>no I/O Command Set is supported (i.e., only the Admin Command Set<br>is supported).<br>This bit shall be set to ‘1’ if no I/O Command Set is supported.<br>6 <br>**I/O Command Set Support (IOCSS):** This bit indicates whether the<br>controller supports one or more I/O Command Sets and supports the<br>Identify I/O Command Set data structure (refer to section 5.1.13.2.19).<br>Controllers that support I/O Command Sets other than the NVM<br>Command Set shall set this bit to ‘1’. Controllers that only support the<br>NVM Command Set may set this bit to ‘1’.<br>5:1<br>Reserved<br>0 <br>**NVM Command Set Support (NCSS):** This bit indicates whether the<br>controller supports the NVM Command Set or a Discovery controller.|
|36|RO|Impl<br>Spec|**NVM Subsystem Reset Supported (NSSRS):**This bit indicates whether the<br>controller supports the NVM Subsystem Reset feature defined in section 3.7.1. This<br>bit is set to '1' if the controller supports the NVM Subsystem Reset feature. This bit<br>is cleared to ‘0' if the controller does not support the NVM Subsystem Reset feature.<br>For Discovery controllers, this field shall be cleared to 0h.|


52








NVM Express [®] Base Specification, Revision 2.2


**Figure 36: Offset 0h: CAP – Controller Capabilities**







|Bits|Type|Reset|Description|
|---|---|---|---|
|35:32|RO|Impl<br>Spec|**Doorbell Stride (DSTRD):** Each Submission Queue and Completion Queue<br>Doorbell property is 32-bits in size. This property indicates the stride between<br>doorbell properties. The stride is specified as (2 ^ (2 + DSTRD)) in bytes. A value<br>of 0h indicates a stride of 4 bytes, where the doorbell properties are packed without<br>reserved space between each property. Refer to section 8.2.2.<br>For NVMe over Fabrics I/O controllers, this property shall be cleared to a fixed<br>value of 0h.|
|31:24|RO|Impl<br>Spec|**Timeout (TO):** This is the worst-case time that host software should wait for the<br>CSTS.RDY bit to transition from:<br>a)<br>‘0’ to ‘1’ after the CC.EN bit transitions from ‘0’ to ‘1’; or<br>b)<br>‘1’ to ‘0’ after the CC.EN bit transitions from ‘1’ to ‘0’.<br>This worst-case time may be experienced after events such as an abrupt shutdown,<br>loss of main power without shutting down the controller, or activation of a new<br>firmware image; typical times are expected to be much shorter.<br>This field is in 500 millisecond units. The maximum value of this field is FFh, which<br>indicates a 127.5 second timeout.<br>If the Controller Ready Independent of Media Enable (CC.CRIME) bit is cleared to<br>‘0’ and the worst-case time for the CSTS.RDY bit to change state is due to enabling<br>the controller after the CC.EN bit transitions from ‘0’ to ‘1’, then this field shall be<br>set to:<br>a)<br>the value in the Controller Ready With Media Timeout (CRTO.CRWMT)<br>field; or<br>b)<br>FFh if the value in the CRTO.CRWMT field is greater than FFh.<br>If the Controller Ready Independent of Media Enable (CC.CRIME) bit is set to ‘1’<br>and the worst-case time for the CSTS.RDY bit to change state is due to enabling<br>the controller after the CC.EN bit transitions from ‘0’ to ‘1’, then this field shall be<br>set to:<br>a)<br>the value in the Controller Ready Independent of Media Timeout<br>(CRTO.CRIMT); or<br>b)<br>FFh if the value in the CRTO.CRIMT field is greater than FFh.<br>Controllers that support the CRTO register (refer to Figure 57) are able to indicate<br>larger timeouts for enabling the controller. Host software should use the value in<br>the CRTO.CRWMT field or the CRTO.CRIMT field depending on the controller<br>ready mode indicated by the CC.CRIME bit to determine the worst-case timeout<br>for the CSTS.RDY bit to transition from ‘0’ to ‘1’ after the CC.EN bit transitions from<br>‘0’ to ‘1’. Host software that is based on revisions earlier than NVM Express Base<br>Specification, Revision 2.0 is not required to wait for more than 127.5 seconds for<br>the CSTS.RDY bit to transition.<br>Refer to sections 3.5.3 and 3.5.4 for more information.|
|23:19|RO|0h|Reserved|


53


NVM Express [®] Base Specification, Revision 2.2


**Figure 36: Offset 0h: CAP – Controller Capabilities**




|Bits|Description|
|---|---|
|1|**Vendor Specific (VS):** Vendor Specific arbitration mechanism.|
|0|**Weighted Round Robin with Urgent Priority Class (WRRUPC):** <br>Weighted Round Robin with Urgent Priority Class arbitration<br>mechanism.|










|Bits|Type|Reset|Description|
|---|---|---|---|
|18:17|RO|Impl<br>Spec|**Arbitration Mechanism Supported (AMS):**This field is bit significant and<br>indicates the optional arbitration mechanisms supported by the controller. If a bit is<br>set to ‘1’, then the corresponding arbitration mechanism is supported by the<br>controller. Refer to section 3.4.4 for arbitration details.<br>**Bits**<br>**Description**<br>1 <br>**Vendor Specific (VS):** Vendor Specific arbitration mechanism.<br>0 <br>**Weighted Round Robin with Urgent Priority Class (WRRUPC):** <br>Weighted Round Robin with Urgent Priority Class arbitration<br>mechanism.<br>The round robin arbitration mechanism is not listed since all controllers shall<br>support this arbitration mechanism.<br>For Discovery controllers, this property shall be cleared to 0h.|
|16|RO|Impl<br>Spec|**Contiguous Queues Required (CQR):**This bit is set to ‘1’ if the controller requires<br>that I/O Submission Queues and I/O Completion Queues are required to be<br>physically contiguous. This bit is cleared to ‘0’ if the controller supports I/O<br>Submission Queues and I/O Completion Queues that are not physically<br>contiguous. If this bit is set to ‘1’, then the Physically Contiguous bit (CDW11.PC)<br>in the Create I/O Submission Queue and Create I/O Completion Queue commands<br>shall be set to ‘1’.<br>For controllers using a message-based transport, this property shall be set to a<br>value of 1.|
|15:00|RO|Impl<br>Spec|**Maximum Queue Entries Supported (MQES):**This field indicates the maximum<br>individual queue size that the controller supports. For NVMe over PCIe<br>implementations, this value applies to the I/O Submission Queues and I/O<br>Completion Queues that the host creates. For NVMe over Fabrics implementations,<br>this value applies to only the I/O Submission Queues that the host creates. This is<br>a 0’s based value. The minimum value is 1h, indicating two entries.|



**Offset 8h: VS – Version**


This property is Read Only (RO) and indicates the version of this specification that the controller supports,
as defined in Figure 37.


**Figure 37: Specification Version Descriptor**






|Bits|Description|
|---|---|
|31:16|**Major Version (MJR):** An integer value indicating the major version number of this specification which is<br>supported by the controller.|
|15:08|**Minor Version (MNR):** An integer value indicating the minor version number of this specification which is<br>supported by the controller.|
|07:00|**Tertiary Version (TER):** An integer value indicating the tertiary version number of this specification which<br>is supported by the controller. If this field is cleared to 0h, then this specification does not have a tertiary<br>version number.|



The reset value for each field is described in Figure 38:


**Figure 38: NVM Express Base Specification Version Property Reset Values**

|1<br>Specification Version|MJR Field|MNR Field|TER Field|
|---|---|---|---|
|1.0|1h|0h|0h|
|1.1|1h|1h|0h|
|1.2|1h|2h|0h|
|1.2.1|1h|2h|1h|



54


NVM Express [®] Base Specification, Revision 2.2


**Figure 38: NVM Express Base Specification Version Property Reset Values**

|1<br>Specification Version|MJR Field|MNR Field|TER Field|
|---|---|---|---|
|1.3|1h|3h|0h|
|1.4|1h|4h|0h|
|2.0|2h|0h|0h|
|2.1|2h|1h|0h|
|2.2|2h|2h|0h|
|Notes:<br>1.<br>The specification version listed includes lettered versions (e.g., 1.4 includes 1.4, 1.4a<br>through 1.4c, etc.).|Notes:<br>1.<br>The specification version listed includes lettered versions (e.g., 1.4 includes 1.4, 1.4a<br>through 1.4c, etc.).|Notes:<br>1.<br>The specification version listed includes lettered versions (e.g., 1.4 includes 1.4, 1.4a<br>through 1.4c, etc.).|Notes:<br>1.<br>The specification version listed includes lettered versions (e.g., 1.4 includes 1.4, 1.4a<br>through 1.4c, etc.).|



**Offset Ch: INTMS – Interrupt Mask Set**


This property is used to mask interrupts when using pin-based interrupts, single message MSI, or multiple
message MSI. When using MSI-X, the interrupt mask table defined as part of MSI-X should be used to
mask interrupts. Host software shall not access this property when configured for MSI-X; any accesses
when configured for MSI-X is undefined. For interrupt behavior requirements, refer to the Interrupts section
of the NVMe over PCIe Transport Specification.


**Figure 39: Offset Ch: INTMS – Interrupt Mask Set**






|Bits|Type|Reset|Description|
|---|---|---|---|
|31:00|RWS|0h|**Interrupt Vector Mask Set (IVMS):**This field is bit significant. If a ‘1’ is written to a<br>bit, then the corresponding interrupt vector is masked from generating an interrupt<br>or reporting a pending interrupt in the MSI Capability Structure. Writing a ‘0’ to a bit<br>has no effect. When read, this field returns the current interrupt mask value within<br>the controller (not the value of this property). If a bit has a value of a ‘1’, then the<br>corresponding interrupt vector is masked. If a bit has a value of ‘0’, then the<br>corresponding interrupt vector is not masked.|



**Offset 10h: INTMC – Interrupt Mask Clear**


This property is used to unmask interrupts when using pin-based interrupts, single message MSI, or multiple
message MSI. When using MSI-X, the interrupt mask table defined as part of MSI-X should be used to
unmask interrupts. Host software shall not access this property when configured for MSI-X; any accesses
when configured for MSI-X is undefined. For interrupt behavior requirements, refer to the Interrupts section
of the NVMe over PCIe Transport Specification.


**Figure 40: Offset 10h: INTMC – Interrupt Mask Clear**






|Bits|Type|Reset|Description|
|---|---|---|---|
|31:00|RWC|0h|**Interrupt Vector Mask Clear (IVMC):**This field is bit significant. If a ‘1’ is written to<br>a bit, then the corresponding interrupt vector is unmasked. Writing a ‘0’ to a bit has<br>no effect. When read, this field returns the current interrupt mask value within the<br>controller (not the value of this property). If a bit has a value of a ‘1’, then the<br>corresponding interrupt vector is masked. If a bit has a value of ‘0’, then the<br>corresponding interrupt vector is not masked.|



**Offset 14h: CC – Controller Configuration**


This property modifies settings for the controller. Host software shall set the Arbitration Mechanism Selected
(CC.AMS), the Memory Page Size (CC.MPS), and the I/O Command Set Selected (CC.CSS) to valid values
prior to enabling the controller by setting CC.EN to ‘1’. Attempting to create an I/O queue before initializing
the I/O Completion Queue Entry Size (CC.IOCQES) and the I/O Submission Queue Entry Size
(CC.IOSQES) shall cause a controller to abort a Create I/O Completion Queue command or a Create I/O
Submission Queue command with a status code of Invalid Queue Size.


55


NVM Express [®] Base Specification, Revision 2.2


**Figure 41: Offset 14h: CC – Controller Configuration**






|Value|Definition|
|---|---|
|0b|**Controller Ready With Media Mode**: Enabling the controller (i.e.,<br>CC.EN transitions from ‘0’ to ‘1’) when this bit is cleared to ‘0’<br>enables Controller Ready With Media mode.|
|1b|**Controller Ready Independent Of Media Mode:** Enabling the<br>controller when this bit is set to ‘1’ enables Controller Ready<br>Independent of Media mode.|



|Bits|Type|Reset|Description|
|---|---|---|---|
|31:25|RO|0h|Reserved|
|24|RW/RO|0b|**Controller Ready Independent of Media Enable (CRIME):**This bit controls<br>the controller ready mode. The controller ready mode is determined by the state<br>of this bit at the time the controller is enabled by transitioning the CC.EN bit from<br>‘0’ to ‘1’.<br>If the CAP.CRMS field is set to 11b, then this bit is RW. If the CAP.CRMS field<br>is not set to 11b, then this bit is RO and shall be cleared to ‘0’. Refer to sections<br>3.5.3 and 3.5.4 for more detail.<br>Changing the value of this field may cause a change in the time reported in the<br>CAP.TO field. Refer to the definition of CAP.TO for more details.<br>**Value**<br>**Definition**<br>0b<br>**Controller Ready With Media Mode**: Enabling the controller (i.e.,<br>CC.EN transitions from ‘0’ to ‘1’) when this bit is cleared to ‘0’<br>enables Controller Ready With Media mode.<br>1b<br>**Controller Ready Independent Of Media Mode:** Enabling the<br>controller when this bit is set to ‘1’ enables Controller Ready<br>Independent of Media mode.|
|23:20|RW/RO|0h|**I/O Completion Queue Entry Size (IOCQES):** This field defines the I/O<br>completion queue entry size that is used for the selected I/O Command Set(s).<br>The required and maximum values for this field are specified in the CQES field<br>in the Identify Controller data structure in Figure 313 for each I/O Command<br>Set. The value is in bytes and is specified as a power of two (2^_n_).<br>If any I/O Completion Queues exist, then write operations that change the value<br>in this field produce undefined results.<br>If the controller does not support I/O queues, then this field shall be read-only<br>with a value of 0h.<br>For Discovery controllers, this field is reserved.|
|19:16|RW/RO|0h|**I/O Submission Queue Entry Size (IOSQES):** This field defines the I/O<br>submission queue entry size that is used for the selected I/O Command Set(s).<br>The required and maximum values for this field are specified in the SQES field<br>in the Identify Controller data structure in Figure 313 for each I/O Command<br>Set. The value is in bytes and is specified as a power of two (2^_n_).<br>If any I/O Submission Queues exist, then write operations that change the value<br>in this field produce undefined results.<br>If the controller does not support I/O queues, then this field shall be read-only<br>with a value of 0h.<br>For Discovery controllers, this field is reserved.|


56






NVM Express [®] Base Specification, Revision 2.2


**Figure 41: Offset 14h: CC – Controller Configuration**


|Value|Definition|
|---|---|
|00b|No notification and no effect|
|01b|Normal shutdown notification|
|10b|Abrupt shutdown notification|
|11b|Reserved|





|Bits|Type|Reset|Description|
|---|---|---|---|
|15:14|RW|00b|**Shutdown Notification (SHN):** This field is used to initiate a controller<br>shutdown when a power down condition is expected. For a normal controller<br>shutdown, it is expected that the controller is given time to process the controller<br>shutdown. For an abrupt shutdown, the host may not wait for the controller<br>shutdown to complete before power is lost.<br>The controller shutdown notification values are defined as:<br>**Value**<br>**Definition**<br>00b<br>No notification and no effect<br>01b<br>Normal shutdown notification<br>10b<br>Abrupt shutdown notification<br>11b<br>Reserved<br>This field should be written by host software prior to any power down condition<br>and prior to any change of the PCI power management state. It is recommended<br>that this field also be written prior to a warm reset (refer to the PCI Express<br>Base Specification). To determine when the controller shutdown processing is<br>complete, refer to the definition of the CSTS.ST bit and the definition of the<br>CSTS.SHST field. Refer to section 3.6 for additional shutdown processing<br>details.<br>Other fields in this property (including the EN bit) may be modified as part of<br>updating this field to 01b or 10b to initiate a controller shutdown. If the EN bit is<br>cleared to ‘0’ such that the EN bit transitions from ‘1’ to ‘0’, then both a Controller<br>Reset and a controller shutdown occur.<br>If an NVM Subsystem Shutdown is reported as in progress or is reported as<br>complete (i.e., CSTS.ST is set to ‘1’, and CSTS.SHST is set to 01b or 10b),<br>then writes to this field modify the field value but have no effect. Refer to section<br>3.6.3 for details.|
|13:11|RW|000b|**Arbitration Mechanism Selected (AMS):**This field selects the arbitration<br>mechanism to be used. This value shall only be changed when CC.EN is<br>cleared to ‘0’. Host software shall only set this field to supported arbitration<br>mechanisms indicated in CAP.AMS. If this field is set to an unsupported value,<br>then the behavior is undefined.<br>For Discovery controllers, this value shall be cleared to 0h.<br>**Value**<br>**Definition**<br>000b<br>Round Robin<br>001b<br>Weighted Round Robin with Urgent Priority Class<br>010b to 110b<br>Reserved<br>111b<br>Vendor Specific|
|10:07|RW|0h|**Memory Page Size (MPS):**This field indicates the host memory page size. The<br>memory page size is (2 ^ (12 + MPS)). Thus, the minimum host memory page<br>size is 4 KiB and the maximum host memory page size is 128 MiB. The value<br>set by host software shall be a supported value as indicated by the<br>CAP.MPSMAX and CAP.MPSMIN fields. This field describes the value used for<br>PRP entry size. This field shall only be modified when CC.EN is cleared to ‘0’.<br>For Discovery controllers this property shall be cleared to 0h.|


|Value|Definition|
|---|---|
|000b|Round Robin|
|001b|Weighted Round Robin with Urgent Priority Class|
|010b to 110b|Reserved|
|111b|Vendor Specific|


57


NVM Express [®] Base Specification, Revision 2.2


**Figure 41: Offset 14h: CC – Controller Configuration**














|Value|Definition|Col3|Col4|Col5|Col6|Col7|
|---|---|---|---|---|---|---|
|000b||**CAP.CSS.NCSS**<br>**Bit**|**Definition**|**Definition**|**Definition**||
|000b||1b|NVM Command Set|NVM Command Set|NVM Command Set|NVM Command Set|
|000b||0b|Reserved|Reserved|Reserved|Reserved|
|001b to 101b|Reserved|Reserved|Reserved|Reserved|Reserved|Reserved|
|110b||**CAP.CSS.IOCSS**<br>**Bit**|**CAP.CSS.IOCSS**<br>**Bit**|**Definition**|**Definition**||
|110b||1b|1b|All Supported I/O Command Sets<br>The I/O Command Sets that are<br>supported are reported in the<br>Identify I/O Command Set data<br>structure<br>(refer<br>to<br>section<br>5.1.13.2.19).|All Supported I/O Command Sets<br>The I/O Command Sets that are<br>supported are reported in the<br>Identify I/O Command Set data<br>structure<br>(refer<br>to<br>section<br>5.1.13.2.19).|All Supported I/O Command Sets<br>The I/O Command Sets that are<br>supported are reported in the<br>Identify I/O Command Set data<br>structure<br>(refer<br>to<br>section<br>5.1.13.2.19).|
|110b||0b|0b|Reserved|Reserved|Reserved|
|111b||**CAP.CSS.NOIOCSS**<br>**Bit**|**CAP.CSS.NOIOCSS**<br>**Bit**|**CAP.CSS.NOIOCSS**<br>**Bit**|**Definition**||
|111b||1b|1b|1b|Admin Command Set only<br>I/O Command Set and I/O<br>Command Set specific Admin<br>commands are not supported.<br>Any<br>I/O<br>Command<br>Set<br>specific<br>Admin<br>command<br>submitted<br>on<br>the<br>Admin<br>Submission Queue is aborted<br>with a status code of Invalid<br>Command Opcode.|Admin Command Set only<br>I/O Command Set and I/O<br>Command Set specific Admin<br>commands are not supported.<br>Any<br>I/O<br>Command<br>Set<br>specific<br>Admin<br>command<br>submitted<br>on<br>the<br>Admin<br>Submission Queue is aborted<br>with a status code of Invalid<br>Command Opcode.|
|111b||0b|0b|0b|Reserved|Reserved|



|Bits|Type|Reset|Description|
|---|---|---|---|
|06:04|RW|000b|**I/O Command Set Selected (CSS):**This field specifies the I/O Command Set<br>or Sets that are selected. This field shall only be changed when the controller is<br>disabled (i.e., CC.EN is cleared to ‘0’). The I/O Command Set or Sets that are<br>selected shall be used for all I/O Submission Queues.<br>**Value**<br>**Definition**<br>000b<br>**CAP.CSS.NCSS**<br>**Bit**<br>**Definition**<br>1b<br>NVM Command Set<br>0b<br>Reserved<br>001b to 101b<br>Reserved<br>110b<br>**CAP.CSS.IOCSS**<br>**Bit**<br>**Definition**<br>1b<br>All Supported I/O Command Sets<br>The I/O Command Sets that are<br>supported are reported in the<br>Identify I/O Command Set data<br>structure<br>(refer<br>to<br>section<br>5.1.13.2.19).<br>0b<br>Reserved<br>111b<br>**CAP.CSS.NOIOCSS**<br>**Bit**<br>**Definition**<br>1b<br>Admin Command Set only<br>I/O Command Set and I/O<br>Command Set specific Admin<br>commands are not supported.<br>Any<br>I/O<br>Command<br>Set<br>specific<br>Admin<br>command<br>submitted<br>on<br>the<br>Admin<br>Submission Queue is aborted<br>with a status code of Invalid<br>Command Opcode.<br>0b<br>Reserved<br>For Discovery controllers, this property shall be cleared to 000b.|
|03:01|RO|000b|Reserved|


58


NVM Express [®] Base Specification, Revision 2.2


**Figure 41: Offset 14h: CC – Controller Configuration**






|Bits|Type|Reset|Description|
|---|---|---|---|
|00|RW|0b|**Enable (EN):**When set to ‘1’, then the controller shall process commands.<br>When cleared to ‘0’, then the controller shall not process commands nor post<br>completion queue entries to Completion Queues. When the host modifies CC<br>to clear this bit from ‘1’ to ‘0’, the controller is reset (i.e., a Controller Reset, refer<br>to section 3.7.2). That reset deletes all I/O Submission Queues and I/O<br>Completion Queues, resets the Admin Submission Queue and the Admin<br>Completion Queue, and brings the hardware to an idle state. That reset does<br>not affect transport specific state (e.g., PCI Express registers including MMIO<br>MSI-X registers), nor the Admin Queue properties (AQA, ASQ, or ACQ). Refer<br>to section 3.7.2 for the effects of that reset on all controller properties. Internal<br>controller state (e.g., Feature values defined in section 5.1.25 that are not<br>persistent across power states) are reset to their default values. The controller<br>shall ensure that there is no impact (e.g., data loss) caused by that Controller<br>Reset to the results of commands that have had corresponding completion<br>queue entries posted to an I/O Completion Queue prior to that Controller Reset.<br>When this bit is cleared to ‘0’, the CSTS.RDY bit is cleared to ‘0’ by the controller<br>once the controller is ready to be re-enabled. When this bit is set to ‘1’, the<br>controller sets the CSTS.RDY bit to ‘1’ when it is ready to process commands.<br>The CSTS.RDY bit may be set to ‘1’ before namespace(s) are ready to be<br>accessed.<br>Setting this bit from a ‘0’ to a ‘1’ when the CSTS.RDY bit is a ‘1’ or clearing this<br>bit from a '1' to a '0' when the CSTS.RDY bit is cleared to '0' has undefined<br>results. The Admin Queue properties (AQA, ASQ, and ACQ) are only allowed<br>to be modified when this bit is cleared to ‘0’.<br>If an NVM Subsystem Shutdown is reported as in progress or is reported as<br>completed (i.e., the CSTS.ST bit is set to ‘1’, and the CSTS.SHST field is set to<br>01b or 10b), then:<br>• <br>setting this bit from ‘0’ to ‘1’ modifies the field value but has no effect<br>(e.g., the controller does not respond by setting the CSTS.RDY bit to<br>‘1’); and<br>• <br>clearing this bit from ‘1’ to ‘0’ resets the controller as defined by this<br>field.<br>Refer to section 3.6.3 for details on NVM Subsystem Shutdown functionality.|



**Offset 1Ch: CSTS – Controller Status**


**Figure 42: Offset 1Ch: CSTS – Controller Status**





|Bits|Type|1<br>Reset|Description|
|---|---|---|---|
|31:07|RO|0h|Reserved|
|06|RO|HwInit|**Shutdown Type (ST):**If CSTS.SHST is set to a non-zero value, then this bit indicates<br>the type of shutdown reported by CSTS.SHST.<br>If this bit is set to ‘1’, then CSTS.SHST is reporting the state of an NVM Subsystem<br>Shutdown and this bit remains set to ‘1’ until an NVM Subsystem Reset occurs.<br>If this bit is cleared to ‘0’, then CSTS.SHST is reporting the state of a controller<br>shutdown.<br>An NVM Subsystem Reset shall clear this bit to ‘0’. All other Controller Level Resets<br>shall not change the value of this bit.<br>If CSTS.SHST is cleared to 00b, then this bit should be ignored by the host.|


59


NVM Express [®] Base Specification, Revision 2.2


**Figure 42: Offset 1Ch: CSTS – Controller Status**





|Bits|Type|1<br>Reset|Description|
|---|---|---|---|
|05|RO|0b|**Processing Paused (PP):**This bit indicates whether the controller is processing<br>commands. If this bit is cleared to ‘0’, then the controller is processing commands<br>normally. If this bit is set to ‘1’, then the controller has temporarily stopped processing<br>commands in order to handle an event (e.g., firmware activation). This bit is only valid<br>when CC.EN is set to ‘1’ and CSTS.RDY is set to ‘1’.|
|04|RWC|HwInit|**NVM Subsystem Reset Occurred (NSSRO):** The initial value of this bit is set to '1' if<br>the last occurrence of an NVM Subsystem Reset (refer to section 3.7.1) occurred<br>while power was applied to the domain. The initial value of this bit is cleared to '0'<br>following an NVM Subsystem Reset due to application of power to the domain. This<br>bit is only valid if the controller supports the NVM Subsystem Reset feature defined in<br>section 3.7.1 as indicated by CAP.NSSRS set to ‘1’.<br>The reset value of this bit is cleared to '0' if an NVM Subsystem Reset causes<br>activation of a new firmware image in the domain.|
|03:02|RO|00b|**Shutdown Status (SHST):** This field indicates the status of shutdown processing that<br>is initiated by the host setting the CC.SHN field, the host setting the NSSD.NSSC field,<br>or a Management Endpoint processing an NVMe-MI Shutdown command (refer to the<br>NVM Express Management Interface Specification). Shutdown processing is able to<br>occur on this controller as a consequence of a host setting the NSSD.NSSC field on<br>another controller to initiate an NVM Subsystem Shutdown that affects this controller.<br>The shutdown status values are defined as:<br>**Value**<br>**Definition**<br>00b<br>Normal operation (no shutdown has been requested)<br>01b<br>Shutdown processing in progress<br>10b<br>Shutdown processing complete<br>11b<br>Reserved<br>If this field is set to 01b (i.e., shutdown processing in progress), then:<br>• <br>an NVM Subsystem Reset aborts both a controller shutdown and an NVM<br>Subsystem Shutdown; and<br>• <br>any other type of Controller Level Reset (CLR):<br>`o` <br>may or may not abort a controller shutdown; and<br>`o` <br>shall not abort an NVM Subsystem Shutdown.<br>If this field is cleared to 00b (i.e., normal operation) when a CLR is initiated, then that<br>CLR shall not change the value of this field.<br>If this field is set to 01b when a CLR is initiated, and shutdown processing is not<br>aborted by that CLR, then that CLR shall not change the value of this field.<br>If this field is set to 01b when a CLR is initiated and shutdown processing is aborted<br>by that CLR, then that CLR shall clear this field to 00b.<br>If this field is set to 10b (i.e., shutdown processing complete) when a CLR is initiated<br>by NVM Subsystem Reset, then that CLR shall clear this field to 00b.<br>If this field is set to 10b when a CLR is initiated by a method other than NVM<br>Subsystem Reset and:<br>• <br>the CSTS.ST bit is set to ‘1’, then that CLR shall not change the value of this<br>field; and<br>• <br>the CSTS.ST bit is cleared to ‘0’, then that CLR shall clear this field to 00b<br>If the CSTS.ST bit is cleared to ‘0’ and this field is set to 10b (i.e., controller shutdown<br>processing is reported as complete), then to start executing commands on the<br>controller:|


|Value|Definition|
|---|---|
|00b|Normal operation (no shutdown has been requested)|
|01b|Shutdown processing in progress|
|10b|Shutdown processing complete|
|11b|Reserved|


60


NVM Express [®] Base Specification, Revision 2.2


**Figure 42: Offset 1Ch: CSTS – Controller Status**







|Bits|Type|1<br>Reset|Description|
|---|---|---|---|
||||• <br>if the CC.EN bit is set to ‘1’, after a shutdown operation then a CLR (e.g., a<br>Controller Reset) followed by enabling the controller (i.e., host sets the<br>CC.EN bit from ‘0’ to ‘1’) is required (refer to section 3.6.1). If a host submits<br>commands to the controller without a prior CLR, then the behavior is<br>undefined; and<br>• <br>if the CC.EN bit is cleared to ‘0’, then:<br>`o` <br>a CLR followed by enabling the controller is required (refer to<br>sections 3.6.1 and 3.6.2); or<br>`o` <br>the CC.EN bit is required to be set to ‘1’ and the CC.SHN bit is<br>required to be cleared to 00b with the same write to the CC property<br>(refer to sections 3.6.1 and 3.6.2).<br>If the CSTS.ST bit is set to ‘1’ and this field is set to 10b (i.e., NVM Subsystem<br>Shutdown processing is reported as complete), then an NVM Subsystem Reset<br>followed by enabling the controller is required to start executing commands (refer to<br>section 3.6.3). If a host submits commands to the controller without a prior NVM<br>Subsystem Reset, then the behavior is undefined.|
|01|RO|HwInit|**Controller Fatal Status (CFS):** This bit is set to ’1’ when a fatal controller error<br>occurred that could not be communicated in the appropriate Completion Queue. This<br>bit is cleared to ‘0’ when a fatal controller error has not occurred. Refer to section 9.5.<br>The reset value of this bit is set to '1' when a fatal controller error is detected during<br>controller initialization.|
|00|RO|0b|**Ready (RDY):** This bit is set to ‘1’ when the controller is ready to process submission<br>queue entries after the CC.EN bit is set to ‘1’. This bit shall be cleared to ‘0’ when the<br>CC.EN bit is cleared to ‘0’ once the controller is ready to be re-enabled. Commands<br>should not be submitted to the controller until this bit is set to ‘1’ after the CC.EN bit is<br>set to ‘1’. Failure to follow this recommendation produces undefined results. Refer to<br>the definition of the CAP.TO field, section 3.5.3, and section 3.5.4 for timing<br>information related to this field.<br>If an NVM Subsystem Shutdown that affects this controller is reported as in progress<br>or is reported as complete (i.e., the CSTS.ST bit is set to ‘1’ and the CSTS.SHST field<br>is set to 01b or is set to 10b), then an NVM Subsystem Reset is required before this<br>bit is allowed to be set to ‘1’ from ‘0’. Refer to section 3.6.3.<br>If a controller shutdown is reported as in progress or is reported as complete (i.e., the<br>CSTS.ST bit is cleared to ‘0’ and the CSTS.SHST field is set to 01b or is set to 10b),<br>then before this bit is allowed to be set to ‘1’ from ‘0’, controller shutdown processing<br>shall stop (e.g., complete or be terminated) and the CSTS.SHST field shall be cleared<br>to 00b.|
|Notes:<br>1.<br>During a Controller Level Reset, the field and bit values may transition to values other than the reset value prior<br>to indicating the reset value.|Notes:<br>1.<br>During a Controller Level Reset, the field and bit values may transition to values other than the reset value prior<br>to indicating the reset value.|Notes:<br>1.<br>During a Controller Level Reset, the field and bit values may transition to values other than the reset value prior<br>to indicating the reset value.|Notes:<br>1.<br>During a Controller Level Reset, the field and bit values may transition to values other than the reset value prior<br>to indicating the reset value.|


61


NVM Express [®] Base Specification, Revision 2.2


**Offset 20h: NSSR – NVM Subsystem Reset**


This optional property provides host software with the capability to initiate an NVM Subsystem Reset.
Support for this property is indicated by the state of the NVM Subsystem Reset Supported (CAP.NSSRS)
field. If the property is not supported, then the address range occupied by the property is reserved. Refer
to section 3.7.1.


**Figure 43: Offset 20h: NSSR – NVM Subsystem Reset**






|Bits|Type|Reset|Description|
|---|---|---|---|
|31:00|RW|0h|**NVM Subsystem Reset Control (NSSRC):** A write of the value 4E564D65h ("NVMe")<br>to this field initiates an NVM Subsystem Reset. A write of any other value has no<br>functional effect on the operation of the NVM subsystem. This field shall return the<br>value 0h when read.|



**Offset 24h: AQA – Admin Queue Attributes**


This property defines the attributes for the Admin Submission Queue and Admin Completion Queue. The
Queue Identifier for the Admin Submission Queue and Admin Completion Queue is 0h. The Admin
Submission Queue’s priority is determined by the arbitration mechanism selected, refer to section 3.4.4.
The Admin Submission Queue and Admin Completion Queue are required to be in physically contiguous
memory.


This property shall not be reset by Controller Reset.


Note: It is recommended that the host use UEFI during boot operations. In low memory environments (e.g.,
Option ROMs in legacy BIOS environments) there may not be sufficient available memory to allocate the
necessary Submission and Completion Queues. In these types of conditions, low memory operation of the
controller is vendor specific.


**Figure 44: Offset 24h: AQA – Admin Queue Attributes**






|Bits|Type|Reset|Description|
|---|---|---|---|
|31:28|RO|0h|Reserved|
|27:16|RW|0h|**Admin Completion Queue Size (ACQS):**Defines the size of the Admin Completion<br>Queue in entries. Refer to section 3.3.3.1. Enabling a controller while this field is cleared<br>to 0h produces undefined results. The minimum size of the Admin Completion Queue is<br>two entries. The maximum size of the Admin Completion Queue is 4,096 entries. This is<br>a 0’s based value.|
|15:12|RO|0h|Reserved|
|11:00|RW|0h|**Admin Submission Queue Size (ASQS):** Defines the size of the Admin Submission<br>Queue in entries. Refer to section 3.3.3.1. Enabling a controller while this field is cleared<br>to 0h produces undefined results. The minimum size of the Admin Submission Queue is<br>two entries. The maximum size of the Admin Submission Queue is 4,096 entries. This is<br>a 0’s based value.|



**Offset 28h: ASQ – Admin Submission Queue Base Address**


This property defines the base memory address of the Admin Submission Queue.


This property shall not be reset by Controller Reset.


**Figure 45: Offset 28h: ASQ – Admin Submission Queue Base Address**

|Bits|Type|Reset|Description|
|---|---|---|---|
|63:12|RW|Impl<br>Spec|**Admin Submission Queue Base (ASQB):**This field specifies the 52 most significant<br>bits of the 64-bit physical address for the Admin Submission Queue. This address shall<br>be memory page aligned (based on the value in CC.MPS). All Admin commands,<br>including creation of I/O Submission Queues and I/O Completions Queues shall be<br>submitted to this queue. For the definition of Submission Queues, refer to section 4.1.|
|11:00|RO|0h|Reserved|



62


NVM Express [®] Base Specification, Revision 2.2


**Offset 30h: ACQ – Admin Completion Queue Base Address**


This property defines the base memory address of the Admin Completion Queue.


This property shall not be reset by Controller Reset.


**Figure 46: Offset 30h: ACQ – Admin Completion Queue Base Address**

|Bits|Type|Reset|Description|
|---|---|---|---|
|63:12|RW|Impl<br>Spec|**Admin Completion Queue Base (ACQB):**This field specifies the 52 most significant<br>bits of the 64-bit physical address for the Admin Completion Queue. This address shall<br>be memory page aligned (based on the value in CC.MPS). All completion queue entries<br>for the commands submitted to the Admin Submission Queue shall be posted to this<br>Completion Queue. This queue is always associated with interrupt vector 0. For the<br>definition of Completion Queues, refer to section 4.1.|
|11:00|RO|0h|Reserved|



**Offset 38h: CMBLOC – Controller Memory Buffer Location**


This optional property defines the location of the Controller Memory Buffer (refer to section 8.2.1). If the
controller does not support the Controller Memory Buffer (CAP.CMBS), this property is reserved. If the
controller supports the Controller Memory Buffer and CMBMSC.CRE is cleared to ‘0’, this property shall be
cleared to 0h.


**Figure 47: Offset 38h: CMBLOC – Controller Memory Buffer Location**





|Bits|Type|Reset|Description|
|---|---|---|---|
|31:12|RO|Impl<br>Spec|**Offset (OFST):**Indicates the offset of the Controller Memory Buffer in multiples of the<br>Size Unit specified in CMBSZ.|
|11:09|RO|000b|Reserved|
|08|RO|Impl<br>Spec|**CMB Queue Dword Alignment (CQDA):** If this bit is set to ‘1’, CDW11.PC is set to ‘1’;<br>and the address pointer specifies Controller Memory Buffer, then the address pointer in<br>a Create I/O Submission Queue command (refer to Figure 478) or a Create I/O<br>Completion Queue command (refer to Figure 474) shall be Dword aligned.<br>If this bit is cleared to ‘0’, then the I/O Submission Queues and I/O Completion Queues<br>contained in the Controller Memory Buffer are aligned as defined by the PRP1 field of a<br>Create I/O Submission Queue command (refer to Figure 478) or a Create I/O Completion<br>Queue command (refer to Figure 474).|
|07|RO|Impl<br>Spec|**CMB Data Metadata Mixed Memory Support (CDMMMS):** If this bit is set to ‘1’, then<br>the restriction on data and metadata use of Controller Memory Buffer by a command as<br>defined in section 8.2.1 is not enforced. If this bit is cleared to ‘0’, then the restriction on<br>data and metadata use of Controller Memory Buffer by a command as defined in section<br>8.2.1 is enforced.|
|06|RO|Impl<br>Spec|**CMB Data Pointer and Command Independent Locations Support (CDPCILS):** If this<br>bit is set to ‘1’, then the restriction that the PRP Lists and SGLs shall not be located in<br>the Controller Memory Buffer if the command that they are associated with is not located<br>in the Controller Memory Buffer is not enforced (refer to section 8.2.1). If this bit is cleared<br>to ‘0’, then that restriction is enforced.|
|05|RO|Impl<br>Spec|**CMB Data Pointer Mixed Locations Support (CDPMLS):** If this bit is set to ‘1’, then<br>the restriction that for a particular PRP List or SGL associated with a single command,<br>all memory that contains that particular PRP List or SGL shall reside in either the<br>Controller Memory Buffer or outside the Controller Memory Buffer, is not enforced (refer<br>to section 8.2.1). If this bit is cleared to ‘0’, then that restriction is enforced.|
|04|RO|Impl<br>Spec|**CMB Queue Physically Discontiguous Support (CQPDS):** If this bit is set to ‘1’, then<br>the restriction that for all queues in the Controller Memory Buffer, the queue shall be<br>physically contiguous, is not enforced (refer to section 8.2.1). If this bit is cleared to ‘0’,<br>then that restriction is enforced.|


63


NVM Express [®] Base Specification, Revision 2.2


**Figure 47: Offset 38h: CMBLOC – Controller Memory Buffer Location**






|Bits|Type|Reset|Description|
|---|---|---|---|
|03|RO|Impl<br>Spec|**CMB Queue Mixed Memory Support (CQMMS):** If this bit is set to ‘1’, then for a<br>particular queue placed in the Controller Memory Buffer, the restriction that all memory<br>associated with that queue shall reside in the Controller Memory Buffer is not enforced<br>(refer to section 8.2.1). If this bit is cleared to ‘0’, then that requirement is enforced.|
|02:00|RO|Impl<br>Spec|**Base Indicator Register (BIR):** Indicates the Base Address Register (BAR) that<br>contains the Controller Memory Buffer. For a 64-bit BAR, the BAR for the least significant<br>32-bits of the address is specified. Values 000b, 010b, 011b, 100b, and 101b are valid.<br>The address specified by the BAR shall be 4 KiB aligned.|



**Offset 3Ch: CMBSZ – Controller Memory Buffer Size**


This optional property defines the size of the Controller Memory Buffer (refer to section 8.2.1). If the
controller does not support the Controller Memory Buffer feature or if the controller supports the Controller
Memory Buffer (CAP.CMBS) and CMBMSC.CRE is cleared to ‘0’, then this property shall be cleared to 0h.


**Figure 48: Offset 3Ch: CMBSZ – Controller Memory Buffer Size**








|Value|Granularity|
|---|---|
|0h|4 KiB|
|1h|64 KiB|
|2h|1 MiB|
|3h|16 MiB|
|4h|256 MiB|
|5h|4 GiB|
|6h|64 GiB|
|7h to Fh|Reserved|





|Bits|Type|Reset|Description|
|---|---|---|---|
|31:12|RO|Impl<br>Spec|**Size (SZ):**Indicates the size of the Controller Memory Buffer available for use by the<br>host. The size is in multiples of the Size Unit. If the Offset + Size exceeds the length of<br>the indicated BAR, the size available to the host is limited by the length of the BAR.|
|11:08|RO|Impl<br>Spec|**Size Units (SZU):** Indicates the granularity of the Size field. <br>**Value**<br>**Granularity**<br>0h<br>4 KiB<br>1h<br>64 KiB<br>2h<br>1 MiB<br>3h<br>16 MiB<br>4h<br>256 MiB<br>5h<br>4 GiB<br>6h<br>64 GiB<br>7h to Fh<br>Reserved|
|07:05|RO|000b|Reserved|
|04|RO|Impl<br>Spec|**Write Data Support (WDS):** If this bit is set to ‘1’, then the controller supports data and<br>metadata in the Controller Memory Buffer for commands that transfer data from the host<br>to the controller (e.g., Write). If this bit is cleared to ‘0’, then data and metadata for<br>commands that transfer data from the host to the controller shall not be transferred to<br>the Controller Memory Buffer.|
|03|RO|Impl<br>Spec|**Read Data Support (RDS):** If this bit is set to ‘1’, then the controller supports data and<br>metadata in the Controller Memory Buffer for commands that transfer data from the<br>controller to the host (e.g., Read). If this bit is cleared to ‘0’, then data and metadata for<br>commands that transfer data from the controller to the host shall not be transferred from<br>the Controller Memory Buffer.|
|02|RO|Impl<br>Spec|**PRP SGL List Support (LISTS):** If this bit is set to ‘1’, then the controller supports PRP<br>Lists in the Controller Memory Buffer. If this bit is set to ‘1’ and SGLs are supported by<br>the controller, then the controller supports Scatter Gather Lists in the Controller Memory<br>Buffer. If this bit is set to ‘1’, then the Submission Queue Support bit shall be set to ‘1’. If<br>this bit is cleared to ‘0’, then PRP Lists and SGLs shall not be placed in the Controller<br>Memory Buffer.|
|01|RO|Impl<br>Spec|**Completion Queue Support (CQS):** If this bit is set to ‘1’, then the controller supports<br>Admin and I/O Completion Queues in the Controller Memory Buffer. If this bit is cleared<br>to ‘0’, then Completion Queues shall not be placed in the Controller Memory Buffer.|
|00|RO|Impl<br>Spec|**Submission Queue Support (SQS):** If this bit is set to ‘1’, then the controller supports<br>Admin and I/O Submission Queues in the Controller Memory Buffer. If this bit is cleared<br>to ‘0’, then Submission Queues shall not be placed in the Controller Memory Buffer.|


64


NVM Express [®] Base Specification, Revision 2.2


**Offset 40h: BPINFO – Boot Partition Information**


This optional property defines the characteristics of Boot Partitions (refer to section 8.1.3). If the controller
does not support the Boot Partitions feature, then this property shall be cleared to 0h.


**Figure 49: Offset 40h: BPINFO – Boot Partition Information**






|Value|Definition|
|---|---|
|00b|No Boot Partition read operation requested|
|01b|Boot Partition read in progress|
|10b|Boot Partition read completed successfully|
|11b|Error completing Boot Partition read|








|Bits|Type|Reset|Description|
|---|---|---|---|
|31|RO|Impl<br>Spec|**Active Boot Partition ID (ABPID):**This bit indicates the identifier of the active Boot<br>Partition.|
|30:26|RO|0h|Reserved|
|25:24|RO|00b|**Boot Read Status (BRS):**This field indicates the status of Boot Partition read<br>operations initiated by the host writing to the BPRSEL.BPID field. Refer to section<br>8.1.3.<br>The boot read status values are defined as:<br>**Value**<br>**Definition**<br>00b<br>No Boot Partition read operation requested<br>01b<br>Boot Partition read in progress<br>10b<br>Boot Partition read completed successfully<br>11b<br>Error completing Boot Partition read<br>If host software writes the BPRSEL.BPID field, this field transitions to 01b. After<br>successfully completing a Boot Partition read operation (i.e., transferring the contents<br>to the boot memory buffer), the controller sets this field to 10b. If there is an error<br>completing a Boot Partition read operation, this field is set to 11b, and the contents<br>of the boot memory buffer are undefined.|
|23:15|RO|0h|Reserved|
|14:00|RO|Impl<br>Spec|**Boot Partition Size (BPSZ):**This field defines the size of each Boot Partition in<br>multiples of 128 KiB. Both Boot Partitions are the same size.|



**Offset 44h: BPRSEL – Boot Partition Read Select**


This optional property is used to initiate the transfer of a data in the Boot Partition (refer to section 8.1.3)
from the controller to the host. If the controller does not support the Boot Partitions feature, then this property
shall be cleared to 0h.


If the host attempts to read beyond the end of a Boot Partition (i.e., the Boot Partition Read Offset plus Boot
Partition Read Size, is greater than the Boot Partition Size in bytes), the controller shall not transfer data
and report an error in the BPINFO.BRS field.


**Figure 50: Offset 44h: BPRSEL – Boot Partition Read Select**







|Bits|Type|Reset|Description|
|---|---|---|---|
|31|RW|0b|**Boot Partition Identifier (BPID):** This bit specifies the Boot Partition identifier for the<br>Boot Partition read operation.|
|30|RO|0b|Reserved|
|29:10|RW|0h|**Boot Partition Read Offset (BPROF):** This field selects the offset into the Boot<br>Partition, in 4 KiB units, that the controller copies into the Boot Partition Memory<br>Buffer.|
|09:00|RW|0h|**Boot Partition Read Size (BPRSZ):** This field selects the read size in multiples of<br>4 KiB to copy into the Boot Partition Memory Buffer.|


**Offset 48h: BPMBL – Boot Partition Memory Buffer Location**


This optional property specifies the memory buffer that is used as the destination for data when a Boot
Partition is read (refer to section 8.1.3). If the controller does not support the Boot Partitions feature, then
this property shall be cleared to 0h.


65


NVM Express [®] Base Specification, Revision 2.2


**Figure 51: Offset 48h: BPMBL – Boot Partition Memory Buffer Location**

|Bits|Type|Reset|Description|
|---|---|---|---|
|63:12|RW|0h|**Boot Partition Memory Buffer Base Address (BMBBA):** This field specifies the 52<br>most significant bits of the 64-bit physical address for the Boot Partition Memory Buffer.|
|11:00|RO|0h|Reserved|



**Offset 50h: CMBMSC – Controller Memory Buffer Memory Space Control**


This optional property specifies how the controller references the Controller Memory Buffer with hostsupplied addresses. If the controller supports the Controller Memory Buffer (CAP.CMBS), this property is
mandatory. Otherwise, this property is reserved.


This property shall be reset by Controller Level Resets other than Controller Lever Resets caused by:

  - a Controller Reset; and

  - a Function Level Reset (refer to the NVM Express NVMe over PCIe Transport Specification).


**Figure 52: Offset 50h: CMBMSC – Controller Memory Buffer Memory Space Control**












|Bits|Type|Reset|Description|
|---|---|---|---|
|63:12|RW|0h|**Controller Base Address (CBA):** This field specifies the 52 most significant bits of the<br>64-bit base address for the Controller Memory Buffer’s controller address range. The<br>Controller Memory Buffer’s controller base address and its size determine its controller<br>address range.<br>The specified address shall be valid only under the following conditions:<br>a)<br>no part of the Controller Memory Buffer’s controller address range is greater<br>than 264 − 1; and<br>b)<br>if the Persistent Memory Region’s controller memory space is enabled, then the<br>Controller Memory Buffer’s controller address range does not overlap the<br>Persistent Memory Region’s controller address range.|
|11:02|RO|0h|Reserved|
|01|RW|0b|**Controller Memory Space Enable (CMSE):** This bit specifies whether addresses<br>supplied by the host are permitted to reference the Controller Memory Buffer.<br>If CMBSMSC.CRE is cleared to ‘0’ this bit has no effect, and the Controller Memory<br>Buffer’s controller memory space is not enabled.<br>If this bit is set to ‘1’ and the controller base address is valid, then the Controller Memory<br>Buffer’s controller memory space is enabled. Otherwise, the controller memory space is<br>not enabled.<br>If the Controller Memory Buffer’s controller memory space is enabled, then addresses<br>supplied by the host that fall within the Controller Memory Buffer’s controller address<br>range shall reference the Controller Memory Buffer.<br>If the Controller Memory Buffer’s controller memory space is not enabled, then no<br>address supplied by the host shall reference the Controller Memory Buffer. Instead, such<br>addresses shall reference memory spaces other than the Controller Memory Buffer.|
|00|RW|0b|**Capabilities Registers Enabled (CRE):** This bit specifies whether the CMBLOC and<br>CMBSZ properties are enabled. If this bit is set to ‘1’, then CMBLOC is defined as shown<br>in Figure 47 and CMBSZ is defined as shown in Figure 48. If this bit is cleared to ‘0’, then<br>CMBSZ and CMBLOC are cleared to 0h.|



**Offset 58h: CMBSTS – Controller Memory Buffer Status**


This optional property indicates the status of the Controller Memory Buffer. If the controller supports the
Controller Memory Buffer (CAP.CMBS), this property is mandatory. Otherwise, this property is reserved.


66


NVM Express [®] Base Specification, Revision 2.2


**Figure 53: Offset 58h: CMBSTS – Controller Memory Buffer Status**






|Bits|Type|Reset|Description|
|---|---|---|---|
|31:01|RO|0h|Reserved|
|00|RO|0b|**Controller Base Address Invalid (CBAI):** This bit indicates whether the controller has<br>failed to enable the Controller Memory Buffer’s controller memory space because<br>CMBMSC.CBA is invalid. If CMBMSC.CRE and CMBMSC.CMSE are set to ‘1’, and<br>CMBMSC.CBA is invalid, this bit shall be set to ‘1’. Otherwise, this bit shall be cleared to<br>‘0’.|



**Offset 5Ch: CMBEBS – Controller Memory Buffer Elasticity Buffer Size**


This optional property identifies to the host the size of the CMB elasticity buffer. A value of 0h in this property
indicates to the host that no information regarding the presence or size of a CMB elasticity buffer is
available.


**Figure 54: Offset 5Ch: CMBEBS – Controller Memory Buffer Elasticity Buffer Size**






|Bits|Type|Reset|Description|
|---|---|---|---|
|31:8|RO|Impl<br>Spec|**CMB Elasticity Buffer Size Base (CMBWBZ):**Indicates the size of the CMB elasticity<br>buffer. The size of the CMB elasticity buffer is equal to the value in this field multiplied<br>by the value specified by the CMB Elasticity Buffer Size Units field.|
|7:5|RO|0h|Reserved|
|4|RO|Impl<br>Spec|**CMB Read Bypass Behavior (CMBRBB):** If a memory read does not conflict with any<br>memory write in the CMB Elasticity Buffer (i.e., if the set of memory addresses specified<br>by a read is disjoint from the set of memory addresses specified by all writes in the<br>CMB Elasticity Buffer), and this bit is:<br>a)<br>set to ‘1’, then memory reads not conflicting with memory writes in the CMB<br>Elasticity Buffer shall bypass those memory writes; and<br>b)<br>cleared to ‘0’, then memory reads not conflicting with memory writes in the<br>CMB Elasticity Buffer may bypass those memory writes.|
|3:0|RO|Impl<br>Spec|**CMB Elasticity Buffer Size Units (CMBSZU):** Indicates the granularity of the CMB<br>Elasticity Buffer Size Base field. <br>**Value**<br>**Granularity**<br>0h<br>Bytes<br>1h<br>1 KiB<br>2h<br>1 MiB<br>3h<br>1 GiB<br>4h – Fh<br>Reserved|


|Value|Granularity|
|---|---|
|0h|Bytes|
|1h|1 KiB|
|2h|1 MiB|
|3h|1 GiB|
|4h – Fh|Reserved|



**Offset 60h: CMBSWTP – Controller Memory Buffer Sustained Write Throughput**


This optional property identifies to the host the maximum CMB sustained write throughput. A value of 0h in
this property indicates to the host that no information regarding the CMB sustained write throughput is
available.


**Figure 55: Offset 60h: CMBSWTP – Controller Memory Buffer Sustained Write Throughput**

|Bits|Type|Reset|Description|
|---|---|---|---|
|31:8|RO|Impl<br>Spec|**CMB Sustained Write Throughput (CMBSWTV):**Indicates the sustained write<br>throughput of the CMB at the maximum payload size specified by the applicable NVMe<br>Transport binding specification (e.g., the PCIe TLP payload size, as specified in the<br>Max_Payload_Size (MPS) field of the PCIe Express Device Control (PXDC) register).<br>The sustained write throughput of the CMB is equal to the value in this field multiplied<br>by the units specified by the CMB Sustained Write Throughput Units field.|
|7:4|RO|0h|Reserved|



67


NVM Express [®] Base Specification, Revision 2.2


|Value|Granularity|
|---|---|
|0h|Bytes/second|
|1h|1 KiB/second|
|2h|1 MiB/second|
|3h|1 GiB/second|
|4h – Fh|Reserved|



**Offset 64h: NSSD – NVM Subsystem Shutdown**


This optional property provides host software with the capability to initiate a normal or an abrupt NVM
Subsystem Shutdown.


Support for this property is indicated by the state of the NVM Subsystem Shutdown Supported (CAP.NSSS)
field. If the property is not supported, then the address range occupied by the register is reserved.


The NVM Subsystem Shutdown Enhancements Supported (CAP.NSSES) bit affects the functionality
invoked by host modification of this property (refer to section 3.6.3).


**Figure 56: Offset 64h: NSSD – NVM Subsystem Shutdown**






|Bits|Type|Reset|Description|
|---|---|---|---|
|31:00|RW|0h|**NVM Subsystem Shutdown Control (NSSC):** A write of the value 4E726D6Ch<br>("Nrml") to this field initiates a normal NVM Subsystem Shutdown on every controller:<br>• <br>in the domain associated with the controller when CAP.CPS is set to 10b (i.e.,<br>domain scope) as specified in section 3.6.3.2 or<br>• <br>in the NVM subsystem when CAP.CPS is set to 11b (i.e., NVM subsystem<br>scope) in the NVM subsystem as specified in section 3.6.3.1.<br>A write of the value 41627074h ("Abpt") to this field initiates an abrupt NVM subsystem<br>shutdown on every controller:<br>• <br>in the domain associated with the controller when CAP.CPS is set to 10b as<br>specified in section 3.6.3.2; or<br>• <br>in the NVM subsystem when CAP.CPS is set to 11b in the NVM subsystem<br>as specified in section 3.6.3.1.<br>A write of any other value to this field has no functional effect on the operation of the<br>NVM subsystem. This field shall return the value 0h when read.|



**Offset 68h: CRTO – Controller Ready Timeouts**


This property indicates the controller ready timeout values. This property is mandatory for controllers
compliant with NVM Express Base Specification revision 2.0 and later.


68


NVM Express [®] Base Specification, Revision 2.2


**Figure 57: Offset 68h: CRTO – Controller Ready Timeouts**






|Bits|Type|Reset|Description|
|---|---|---|---|
|31:16|RO|Impl<br>Spec|**Controller Ready Independent of Media Timeout (CRIMT):** If the<br>CAP.CRMS.CRIMS bit is cleared to ‘0’, then the controller shall clear this field to<br>0h and the host should ignore this field.<br>If the CAP.CRMS.CRIMS bit is set to ‘1’, then this field contains the worst-case<br>time that host software should wait after CC.EN transitions from ‘0’ to ‘1’ for the<br>controller to become ready and be able to successfully process all commands<br>that do not access attached namespaces and Admin commands that do not<br>require access to media when the controller is in Controller Ready Independent<br>of Media mode (i.e., the CC.CRIME bit is set to ‘1’). Attached namespaces and<br>media required to process Admin commands may or may not be ready within this<br>time period (refer to section 3.5.3, section 3.5.4, and Figure 84).<br>This worst-case time may be experienced after events such as an abrupt<br>shutdown or activation of a new firmware image; typical times are expected to be<br>much shorter. This field is in 500 millisecond units.<br>The value of this field should not exceed FFh (i.e., 127.5 seconds).|
|15:0|RO|Impl<br>Spec|**Controller Ready With Media Timeout (CRWMT):** This field contains the worst-<br>case time that host software should wait after CC.EN transitions from ‘0’ to ‘1’<br>for:<br>a)<br>the controller to become ready and be able to successfully process all<br>commands; and<br>b)<br>all attached namespaces and media required to process Admin<br>commands to become ready,<br>independent of which ready mode (refer to CC.CRIME) the controller is in (refer<br>to section 3.5.3 and section 3.5.4).<br>This worst-case time may be experienced after events such as an abrupt<br>shutdown or activation of a new firmware image; typical times are expected to be<br>much shorter. This field is in 500 millisecond units.<br>The value of this field shall be greater than or equal to the value of the<br>CRTO.CRIMT field and may be significantly larger than the value of the<br>CRTO.CRIMT field.|



**Offset E00h: PMRCAP – Persistent Memory Region Capabilities**


This property indicates capabilities of the Persistent Memory Region. If the controller does not support the
Persistent Memory Region feature, then this property shall be cleared to 0h.


This property shall not be reset by Controller Reset.


**Figure 58: Offset E00h: PMRCAP – Persistent Memory Region Capabilities**







|Bits|Type|Reset|Description|
|---|---|---|---|
|31:25|RO|0h|Reserved|
|24|RO|Impl<br>Spec|**Controller Memory Space Supported (CMSS):** If this bit is set to ‘1’, then the addresses<br>supplied by the host are permitted to reference the Persistent Memory Region only if the<br>host has enabled the Persistent Memory Region’s controller memory space.<br>If the controller supports referencing the Persistent Memory Region with host-supplied<br>addresses, then this bit shall bet set to ‘1’. Otherwise, this bit shall be cleared to ‘0’.|
|23:16|RO|Impl<br>Spec|**Persistent Memory Region Timeout (PMRTO):**This field contains the minimum<br>amount of time that host software should wait for the Persistent Memory Region to<br>become ready or not ready after PMRCTL.EN is modified. The time in this field is<br>expressed in Persistent Memory Region time units (refer to PMRCAP.PMRTU).|
|15:14|RO|00b|Reserved|


69


NVM Express [®] Base Specification, Revision 2.2


**Figure 58: Offset E00h: PMRCAP – Persistent Memory Region Capabilities**






|Bits|Description|
|---|---|
|3:2|Reserved|
|1|**Completion of PMRSTS Read (CPMTSTSR):**The completion of a read to<br>the PMRSTS property shall ensure that all prior writes to the Persistent<br>Memory Region have completed and are persistent.|
|0|**Completion of Memory Read (CMR):** The completion of a memory read<br>from any Persistent Memory Region address ensures that all prior writes to<br>the Persistent Memory Region have completed and are persistent.|








|Value|Persistent Memory Region Time Units|
|---|---|
|00b|500 milliseconds|
|01b|minutes|
|10b to 11b|Reserved|



|Bits|Type|Reset|Description|
|---|---|---|---|
|13:10|RO|Impl<br>Spec|**Persistent Memory Region Write Barrier Mechanisms (PMRWBM):** This field lists<br>mechanisms that may be used to ensure that previous writes to the Persistent Memory<br>Region have completed and are persistent when the Persistent Memory Region is ready<br>and operating normally. A bit in this field is set to ‘1’ if the corresponding mechanism to<br>ensure persistence is supported. A bit in this field is cleared to ‘0’ if the corresponding<br>mechanism to ensure persistence is not supported.<br>At least one bit in this field shall be set to ‘1’.<br>**Bits**<br>**Description**<br>3:2<br>Reserved <br>1 <br>**Completion of PMRSTS Read (CPMTSTSR):**The completion of a read to<br>the PMRSTS property shall ensure that all prior writes to the Persistent<br>Memory Region have completed and are persistent. <br>0 <br>**Completion of Memory Read (CMR):** The completion of a memory read<br>from any Persistent Memory Region address ensures that all prior writes to<br>the Persistent Memory Region have completed and are persistent.|
|9:8|RO|Impl<br>Spec|**Persistent Memory Region Time Units (PMRTU):** Indicates Persistent Memory Region<br>time units.<br>**Value**<br>**Persistent Memory Region Time Units**<br>00b<br>500 milliseconds<br>01b<br>minutes<br>10b to 11b<br>Reserved|
|7:5|RO|Impl<br>Spec|**Base Indicator Register (BIR):**This field indicates the Base Address Register (BAR)<br>that specifies the address and size of the Persistent Memory Region. Values 010b, 011b,<br>100b, and 101b are valid.|
|4|RO|Impl<br>Spec|**Write Data Support (WDS):** If this bit is set to ‘1’, then the controller supports data and<br>metadata in the Persistent Memory Region for commands that transfer data from the<br>host to the controller (e.g., Write). If this bit is cleared to ‘0’, then data and metadata for<br>commands that transfer data from the host to the controller shall not be transferred to<br>the Persistent Memory Region.<br>If PMRCAP.CMSS is cleared to ‘0’, this bit shall be cleared to ‘0’.|
|3|RO|Impl<br>Spec|**Read Data Support (RDS):** If this bit is set to ‘1’, then the controller supports data and<br>metadata in the Persistent Memory Region for commands that transfer data from the<br>controller to the host (e.g., Read). If this bit is cleared to ‘0’, then all data and metadata<br>for commands that transfer data from the controller to the host shall not be transferred<br>from the Persistent Memory Region.<br>If PMRCAP.CMSS is cleared to ‘0’, this bit shall be cleared to ‘0’.|
|2:0|RO|000b|Reserved|


**Offset E04h: PMRCTL – Persistent Memory Region Control**


This optional property controls the operation of the Persistent Memory Region. If the controller does not
support the Persistent Memory Region feature, then this property shall be cleared to 0h.


This property shall not be reset by Controller Reset.


**Figure 59: Offset E04h: PMRCTL – Persistent Memory Region Control**





|Bits|Type|Reset|Description|
|---|---|---|---|
|31:1|RO|0h|Reserved|
|0|RW|0b|**Enable (EN):** When set to ‘1’, then the Persistent Memory Region is ready to process<br>PCI Express memory read and write requests once PMRSTS.NRDY is cleared to ‘0’.<br>When cleared to ‘0’, then the Persistent Memory Region is disabled and PMRSTS.NRDY<br>shall be set to ‘1’ once the Persistent Memory Region is ready to be re-enabled.|


70


NVM Express [®] Base Specification, Revision 2.2


**Offset E08h: PMRSTS – Persistent Memory Region Status**


This optional property provides the status of the Persistent Memory Region. If the controller does not
support the Persistent Memory Region feature, then this property shall be cleared to 0h.


This property shall not be reset by Controller Reset.


**Figure 60: Offset E08h: PMRSTS – Persistent Memory Region Status**







|Bits|Type|Reset|Description|
|---|---|---|---|
|31:13|RO|0h|Reserved|
|12|RO|0b|**Controller Base Address Invalid (CBAI):** This field indicates whether the controller has<br>failed to enable the Persistent Memory Region’s controller memory space because the<br>controller 64-bit base address specified by PMRMSCU.CBA and PMRMSCL.CBA are<br>invalid. If PMRCAP.CMSS is set to ‘1’, PMRMSCL.CMSE is set to ‘1’, and the controller<br>64-bit base address specified by PMRMSCU.CBA and PMRMSCL.CBA is invalid, this<br>bit shall be set to ‘1’. Otherwise, this bit shall be cleared to ‘0’.|
|11:9|RO|000b|**Health Status (HSTS):** If the Persistent Memory Region is ready, then this field indicates<br>the health status of the Persistent Memory Region. This field is always cleared to 000b<br>when the Persistent Memory Region is not ready.<br>The health status values are defined as:<br>**Value**<br>**Definition**<br>000b<br>**Normal Operation:** The Persistent Memory Region is operating<br>normally.<br>001b<br>**Restore Error:** The Persistent Memory Region is operating<br>normally and is persistent; however, the contents of the Persistent<br>Memory Region may not have been restored correctly (i.e., may not<br>contain the contents prior to the last power cycle, NVM Subsystem<br>Reset, Controller Level Reset, or Persistent Memory Region<br>disable).<br>010b<br>**Read Only:** The Persistent Memory Region is read only. PCI<br>Express memory write requests do not update the Persistent<br>Memory Region. PCI Express memory read requests to the<br>Persistent Memory Region return correct data. <br>011b<br>**Unreliable:** The Persistent Memory Region has become unreliable.<br>PCI Express memory reads may return invalid data or generate<br>poisoned PCI Express TLP(s). Persistent Memory Region memory<br>writes may not update memory or may update memory with<br>undefined data. The Persistent Memory Region may also have<br>become non-persistent. <br>100b to 111b<br>Reserved|
|8|RO|0b|**Not Ready (NRDY):** This bit indicates if the Persistent Memory Region is ready for use.<br>If this bit is cleared to ‘0’ and the PMRCTL.EN is set to ‘1’, then the Persistent Memory<br>Region is ready to accept and process PCI Express memory read and write requests. If<br>this bit is set to ‘1’ or the PMRCTL.EN bit is cleared to ‘0’, then the Persistent Memory<br>Region is not ready to process PCI Express memory read and write requests.|
|7:0|RO|0h|**Error (ERR):**When the Persistent Memory Region is ready and operating normally, this<br>field indicates whether previous memory writes to the Persistent Memory Region have<br>completed without error. If this field is cleared to 0h, then previous writes to the Persistent<br>Memory Region have completed without error and that the values written are persistent.<br>A non-zero value in this field indicates the occurrence of an error that may have caused<br>one or more of the previous writes to not have completed successfully. The meaning of<br>any particular non-zero value is vendor specific.<br>Once this field takes on a non-zero value, it maintains a non-zero value until the PCI<br>Function is reset.|


|Value|Definition|
|---|---|
|000b|**Normal Operation:** The Persistent Memory Region is operating<br>normally.|
|001b|**Restore Error:** The Persistent Memory Region is operating<br>normally and is persistent; however, the contents of the Persistent<br>Memory Region may not have been restored correctly (i.e., may not<br>contain the contents prior to the last power cycle, NVM Subsystem<br>Reset, Controller Level Reset, or Persistent Memory Region<br>disable).|
|010b|**Read Only:** The Persistent Memory Region is read only. PCI<br>Express memory write requests do not update the Persistent<br>Memory Region. PCI Express memory read requests to the<br>Persistent Memory Region return correct data.|
|011b|**Unreliable:** The Persistent Memory Region has become unreliable.<br>PCI Express memory reads may return invalid data or generate<br>poisoned PCI Express TLP(s). Persistent Memory Region memory<br>writes may not update memory or may update memory with<br>undefined data. The Persistent Memory Region may also have<br>become non-persistent.|
|100b to 111b|Reserved|


71






NVM Express [®] Base Specification, Revision 2.2


**Offset E0Ch: PMREBS – Persistent Memory Region Elasticity Buffer Size**


This optional property identifies to the host the size of the PMR elasticity buffer. A value of 0h in this property
indicates to the host that no information regarding the presence or size of a PMR elasticity buffer is
available.


This property shall not be reset by Controller Reset.


**Figure 61: Offset E0Ch: PMREBS – Persistent Memory Region Elasticity Buffer Size**






|Bits|Type|Reset|Description|
|---|---|---|---|
|31:8|RO|Impl<br>Spec|**PMR Elasticity Buffer Size Base (PMRWBZ):** Indicates the size of the PMR elasticity<br>buffer. The actual size of the PMR elasticity buffer is equal to the value in this field<br>multiplied by the value specified by the PMR Elasticity Buffer Size Units field.|
|7:5|RO|000b|Reserved|
|4|RO|Impl<br>Spec|**PMR Read Bypass Behavior (PMRRBB):** If a memory read does not conflict with any<br>memory write in the PMR Elasticity Buffer (i.e., if the set of memory addresses specified<br>by a read is disjoint from the set of memory addresses specified by all writes in the PMR<br>Elasticity Buffer), and this bit is:<br>a)<br>set to ‘1’, then memory reads not conflicting with memory writes in the PMR<br>Elasticity Buffer shall bypass those memory writes; and<br>b)<br>cleared to ‘0’, then memory reads not conflicting with memory writes in the PMR<br>Elasticity Buffer may bypass those memory writes.|
|3:0|RO|Impl<br>Spec|**PMR Elasticity Buffer Size Units (PMRSZU):** Indicates the granularity of the PMR<br>Elasticity Buffer Size Base field.<br>**Value**<br>**Definition**<br>0h<br>Bytes<br>1h<br>1 KiB<br>2h<br>1 MiB<br>3h<br>1 GiB<br>4h to Fh<br>Reserved|


|Value|Definition|
|---|---|
|0h|Bytes|
|1h|1 KiB|
|2h|1 MiB|
|3h|1 GiB|
|4h to Fh|Reserved|



**Offset E10h: PMRSWTP – Persistent Memory Region Sustained Write Throughput**


This optional property identifies to the host the maximum PMR sustained write throughput. A value of 0h in
this property indicates to the host that no information regarding the PMR sustained write throughput is
available.


This property shall not be reset by Controller Reset.


**Figure 62: Offset E10h: PMRSWTP – Persistent Memory Region Sustained Write Throughput**





|Bits|Type|Reset|Description|
|---|---|---|---|
|31:8|RO|Impl<br>Spec|**PMR Sustained Write Throughput (PMRSWTV):** Indicates the sustained write<br>throughput of the PMR at the maximum payload size specified by the applicable NVMe<br>Transport binding specification (e.g., the PCIe TLP payload size, as specified in the<br>Max_Payload_Size (MPS) field of the PCI Express Device Control (PXDC) register). The<br>actual sustained write throughput of the PMR is equal to the value in this field multiplied<br>by the units specified by the PMR Sustained Write Throughput Units field.|
|7:4|RO|0h|Reserved|
|3:0|RO|Impl<br>Spec|**PMR Sustained Write Throughput Units (PMRSWTU):** Indicates the granularity of the<br>PMR Sustained Write Throughput field.<br>**Value**<br>**Definition**<br>0h<br>Bytes per second<br>1h<br>1 KiB / s<br>2h<br>1 MiB / s<br>3h<br>1 GiB / s<br>7h to Fh<br>Reserved|


|Value|Definition|
|---|---|
|0h|Bytes per second|
|1h|1 KiB / s|
|2h|1 MiB / s|
|3h|1 GiB / s|
|7h to Fh|Reserved|


72


NVM Express [®] Base Specification, Revision 2.2


**Offset E14h: PMRMSCL – Persistent Memory Region Memory Space Control Lower**


This optional property and the PMRMSCU property specify how the controller references the Persistent
Memory Region with host-supplied addresses. If the controller supports the Persistent Memory Region’s
controller memory space (PMRCAP.CMSS), this property is mandatory. Otherwise, this property is
reserved. The host shall access this register with aligned 32-bit accesses.


This property shall not be reset by Controller Reset.


**Figure 63: Offset E14h: PMRMSCL – Persistent Memory Region Memory Space Control Lower**













|Bits|Type|Reset|Description|
|---|---|---|---|
|31:12|RW|0h|**Controller Base Address (CBA):** This field specifies the 20 least significant bits of the<br>52 most significant bits of the 64-bit base address for the Persistent Memory Region’s<br>controller address range. The Persistent Memory Region’s controller base address and<br>its size determine its controller address range.<br>The 64-bit base address specified by this field and PMRMSCU.CBA when the CMSE bit<br>is set to ‘1’ shall be valid only under the following conditions:<br>a)<br>no part of the Persistent Memory Region’s controller address range is greater<br>than 264 − 1; and<br>b)<br>if the Controller Memory Buffer’s controller memory space is enabled, then the<br>Persistent Memory Region’s controller address range does not overlap the<br>Controller Memory Buffer’s controller address range.|
|11:02|RO|0h|Reserved|
|01|RW|0b|**Controller Memory Space Enable (CMSE):** This bit specifies whether addresses<br>supplied by the host are permitted to reference the Persistent Memory Region.<br>If this bit is set to ‘1’ and the controller base address is valid, then the Persistent Memory<br>Region’s controller memory space is enabled. Otherwise, the controller memory space<br>is not enabled.<br>If the Persistent Memory Region’s controller memory space is enabled, then addresses<br>supplied by the host that fall within the Persistent Memory Region’s controller address<br>range shall reference the Persistent Memory Region.<br>If the Persistent Memory Region’s controller memory space is not enabled, then no<br>address supplied by the host shall reference the Persistent Memory Region. Instead,<br>such addresses shall reference memory spaces other than the Persistent Memory<br>Region.|
|00|RO|0b|Reserved|


**Offset E18h: PMRMSCU – Persistent Memory Region Memory Space Control Upper**


This optional property and the PMRMSCL property specify how the controller references the Persistent
Memory Region with host-supplied addresses. If the controller supports the Persistent Memory Region’s
controller memory space (PMRCAP.CMSS), this property is mandatory. Otherwise, this property is
reserved. The host shall access this register with aligned 32-bit accesses.


This register shall not be reset by Controller Reset.


**Figure 64: Offset E18h: PMRMSCU – Persistent Memory Region Memory Space Control Upper**





|Bits|Type|Reset|Description|
|---|---|---|---|
|31:00|RW|0h|**Controller Base Address (CBA):** This field specifies the 32 most significant bits of the<br>52 most significant bits of the 64-bit base address for the Persistent Memory Region’s<br>controller address range. The Persistent Memory Region’s controller base address and<br>its size determine its controller address range.|


73


NVM Express [®] Base Specification, Revision 2.2


**3.2** **NVM Subsystem Entities**


**Namespaces**


**Namespace Overview**


A namespace is a formatted quantity of non-volatile memory that may be directly accessed by a host. A
namespace ID (NSID) is an identifier used by a controller to provide access to a namespace.


**Valid and Invalid NSIDs**


Valid NSIDs are the range of possible NSIDs that may be used to refer to namespaces that exist in the
NVM subsystem. Any NSID is valid, except if that NSID is 0h or greater than the Number of Namespaces
field reported in the Identify Controller data structure (refer to Figure 313). NSID FFFFFFFFh is a broadcast
value that is used to specify all namespaces. An invalid NSID is any value that is not a valid NSID and is
also not the broadcast value.


Valid NSIDs are:


a) allocated or unallocated in the NVM subsystem; and
b) active or inactive for a specific controller.


**Allocated and Unallocated NSID Types**


In the NVM subsystem, a valid NSID is:


a) an allocated NSID; or
b) an unallocated NSID.


Allocated NSIDs refer to namespaces that exist in the NVM subsystem. Unallocated NSIDs do not refer to
any namespaces that exist in the NVM subsystem.


**Active and Inactive NSID Types**


For a specific controller, an allocated NSID is:


a) an active NSID; or
b) an inactive NSID.


Active NSIDs for a controller refer to namespaces that are attached to that controller. Allocated NSIDs that
are inactive for a controller refer to namespaces that are not attached to that controller.


Unallocated NSIDs are inactive NSIDs for all controllers in the NVM subsystem.


An allocated NSID may be an active NSID for some controllers and an inactive NSID for other controllers
in the same NVM subsystem if the namespace that the NSID refers to is attached to some controllers, but
not all controllers, in the NVM subsystem.


Refer to section 8.1.15 for actions associated with a namespace being detached or deleted.


**NSID and Namespace Relationships**


Unless otherwise noted, specifying an inactive NSID in a command that uses the Namespace Identifier
(NSID) field shall cause the controller to abort the command with a status code of Invalid Field in Command.
Specifying an invalid NSID in a command that uses the NSID field shall cause the controller to abort the
command with a status code of Invalid Namespace or Format.


Figure 65 summarizes the valid NSID types and Figure 66 visually shows the NSID types and how they
relate.


**Figure 65: NSID Types and Relationship to Namespace**

|Valid NSID Type|NSID relationship to namespace|Reference|
|---|---|---|
|Unallocated|Does not refer to any namespace that exists in the NVM subsystem|3.2.1.3|



74


NVM Express [®] Base Specification, Revision 2.2


**Figure 65: NSID Types and Relationship to Namespace**

|Valid NSID Type|NSID relationship to namespace|Reference|
|---|---|---|
|Allocated|Refers to a namespace that exists in the NVM subsystem|3.2.1.3|
|Inactive|Does not refer to a namespace that is attached to the controller1|3.2.1.4|
|Active|Refers to a namespace that is attached to the controller|3.2.1.4|
|Notes:<br>1.<br>If allocated, refers to a namespace that is not attached to the controller. If unallocated, does not refer to any<br>namespace.|Notes:<br>1.<br>If allocated, refers to a namespace that is not attached to the controller. If unallocated, does not refer to any<br>namespace.|Notes:<br>1.<br>If allocated, refers to a namespace that is not attached to the controller. If unallocated, does not refer to any<br>namespace.|



**Figure 66: NSID Types**


**NSID**



0 1 NN NN+1


Inv. Valid Invalid



FFFFFFFFh


B


Broadcast Value











**NSID and Namespace Usage**


If Namespace Management (refer to section 8.1.15), ANA Reporting (refer to section 8.1.1), or NVM Sets
(refer to section 3.2.2) capabilities are supported, then NSIDs shall be unique within the NVM subsystem
(e.g., NSID of 3 shall refer to the same physical namespace regardless of the accessing controller). If the
Namespace Management, ANA Reporting, and NVM Sets capabilities are not supported, then NSIDs:


a) for shared namespaces shall be unique within the NVM subsystem; and
b) for private namespaces are not required to be unique within the NVM subsystem.


The Identify command (refer to section 5.1.13) may be used to determine the active NSIDs for a controller
and the allocated NSIDs in the NVM subsystem.


If the MNAN field (refer to Figure 313) is cleared to 0h, then the maximum number of allocated NSIDs is
the same as the value reported in the NN field (refer to Figure 313). If the MNAN field is non-zero, then the
maximum number of allocated NSIDs may be less than the number of namespaces (e.g., an NVM
subsystem may support a maximum valid NSID value (i.e., the NN field) set to 1,000,000 but support a
maximum of 10 allocated NSID values).


To determine the active NSIDs for a particular controller, the host may follow either of the following methods:


75


NVM Express [®] Base Specification, Revision 2.2


1. Issue an Identify command with the CNS field cleared to 0h for each valid NSID (based on the

Number of Namespaces value (i.e., MNAM field or NN field) in the Identify Controller data
structure). If a non-zero data structure is returned for a particular NSID, then that is an active NSID;
or
2. Issue an Identify command with a CNS field set to 2h to retrieve a list of up to 1,024 active NSIDs.

If there are more than 1,024 active NSIDs, continue to issue Identify commands with a CNS field
set to 2h until all active NSIDs are retrieved.


To determine the allocated NSIDs in the NVM subsystem, the host may issue an Identify command with
the CNS field set to 10h to retrieve a list of up to 1,024 allocated NSIDs. If there are more than 1,024
allocated NSIDs, continue to issue Identify commands with a CNS field set to 10h until all allocated NSIDs
are retrieved.


Namespace IDs may change across power off conditions. However, it is recommended that namespace
IDs remain static across power off conditions to avoid issues with host software. To determine if the same
namespace has been encountered, the host may use the:


a) UUID field in the Namespace Identification Descriptor (refer to Figure 316), if present;
b) NGUID field in the Identify Namespace data (refer to the applicable I/O Command Set specification)

or in the Namespace Identification Descriptor, if present; or
c) EUI64 field in the Identify Namespace data or in the Namespace Identification Descriptor, if present.


UIDREUSE bit in the NSFEAT field (refer to Figure 320 or the Identify Namespace data structure in the
NVM Command Set Specification, if applicable) indicates NGUID and EUI64 reuse characteristics.


If Asymmetric Namespace Access Reporting is supported (i.e., the Asymmetric Namespace Access
Reporting Support (ANARS) bit is set to ‘1’ in the CMIC field in the Identify Controller data structure (refer
to Figure 313)), refer to the applicable I/O Command Set specification for additional detail, if any.


A namespace may or may not have a relationship to a Submission Queue; this relationship is determined
by the host software implementation. The controller shall support access to any attached namespace from
any I/O Submission Queue.


**I/O Command Set Associations**


A namespace is associated with exactly one I/O Command Set. For I/O commands and I/O Command Set
specific Admin commands, the I/O Command Set with which a submission queue entry is associated is
determined by the Namespace Identifier (NSID) field in the command.


An NVM subsystem may contain namespaces each of which is associated with a different I/O Command
Set. A controller may support attached namespaces that use any of the I/O Command Sets that the
controller simultaneously supports as indicated in the I/O Command Set Profile (refer to section
5.1.25.1.17).


**NVM Sets**


An NVM Set is a collection of NVM that is separate (logically and potentially physically) from NVM in other
NVM Sets. One or more namespaces that contain formatted storage may be created within an NVM Set
and those namespaces inherit the attributes of the NVM Set. A namespace that contains formatted storage
is wholly contained within a single NVM Set and shall not span more than one NVM Set.


Figure 67 shows an example of three NVM Sets. NVM Set A contains three namespaces (NS A1, NS A2,
and NS A3). NVM Set B contains two namespaces (NS B1 and NS B2). NVM Set C contains one
namespace (NS C1). Each NVM Set shown also contains ‘Unallocated’ regions that consist of NVM that is
not yet allocated to a namespace.


76


NVM Express [®] Base Specification, Revision 2.2


**Figure 67: NVM Sets and Associated Namespaces**


There is a subset of Admin commands that are NVM Set aware as described in Figure 68.


**Figure 68: NVM Set Aware Admin Commands**















|Admin Command|Details|
|---|---|
|Identify|• <br>The Identify Namespace data structure includes the associated NVM Set<br>Identifier.<br>• <br>The NVM Set List data structure includes attributes for each NVM Set.|
|Capacity Management|• <br>The Create NVM Set action returns the NVM Set Identifier of the NVM Set that<br>is created.<br>• <br>The Delete NVM Set action includes the NVM Set Identifier of the NVM Set that<br>is to be deleted.|
|Namespace Management|• <br>The create action includes the NVM Set Identifier as a host specified field.|
|Get Features and<br>Set Features|• <br>The Read Recovery Level Feature specifies the associated NVM Set Identifier.<br>• <br>The Predictable Latency Mode Config Feature specifies the associated NVM Set<br>Identifier.<br>• <br>The Predictable Latency Mode Window Feature specifies the associated NVM<br>Set Identifier.|
|Connect|• <br>The Connect command includes the associated NVM Set Identifier.|
|Create I/O Submission Queue|• <br>The Create I/O Submission Queue command includes the associated NVM Set<br>Identifier.|
|Get Log Page|• <br>The Predictable Latency Per NVM Set log page specifies the associated NVM<br>Set Identifier.|


The host determines the NVM Sets present and their attributes using the Identify command with CNS value
of 04h to retrieve the NVM Set List (refer to Figure 318). For each NVM Set, the attributes include:

  - an identifier associated with the NVM Set;

  - the optimal size for writes to the NVM Set;


77


NVM Express [®] Base Specification, Revision 2.2


  - the total capacity of the NVM Set; and

  - the unallocated capacity for the NVM Set.


An NVM Set Identifier is a 16-bit value that specifies the NVM Set with which an action is associated. An
NVM Set Identifier is unique with the NVM subsystem. An NVM Set Identifier may be specified in NVM Set
aware Admin commands (refer to Figure 68). An NVM Set Identifier value of 0h is reserved and is not a
valid NVM Set Identifier. Unless otherwise specified, if the host specifies an NVM Set Identifier cleared to
0h for a command that requires an NVM Set Identifier, then that command shall abort with a status code of
Invalid Field in Command.


Each NVM Set is associated with exactly one Endurance Group (refer to section 3.2.3).


The NVM Set with which a namespace that contains formatted storage is associated is reported in the
Identify Namespace data structure (refer to the applicable NVMe I/O Command Set specification). When a
host creates a namespace that contains formatted storage using the Namespace Management command,
the host specifies the NVM Set Identifier of the NVM Set that the namespace is to be created in. The
namespace that is created inherits attributes from the NVM Set (e.g., the optimal write size to the NVM).


If NVM Sets are supported, then all controllers in the NVM subsystem shall:

  - Indicate support for NVM Sets in the Controller Attributes field in the Identify Controller data
structure;

  - Support the NVM Set Identifier in all commands that use the NVM Set Identifier;

  - Support the NVM Set List for the Identify command;

  - Indicate the NVM Set Identifier with which any namespace that contains formatted storage is
associated in the Identify Namespace data structure for that namespace;

  - Support Endurance Groups; and

  - For each NVM Set, indicate the associated Endurance Group as an attribute.


If support for NVM Sets is not reported (i.e., the NVM Sets bit is cleared to ‘0’ in the CTRATT field; refer to
Figure 313), then the NVM Set Identifier field shall be cleared to 0h in all commands and data structures
that support an NVM Set Identifier field.


**Endurance Groups**


Endurance may be managed within a single NVM Set (refer to section 3.2.2) or across a collection of NVM
Sets. Each NVM Set is associated with an Endurance Group (refer to Figure 318). If two or more NVM Sets
have the same Endurance Group Identifier, then endurance is managed by the NVM subsystem across
that collection of NVM Sets. If only one NVM Set is associated with a specific Endurance Group Identifier,
then endurance is managed locally to that NVM Set.


If NVM Sets are not supported, then endurance is managed by the NVM subsystem:

  - within each Endurance Group if Endurance Groups are supported; or

  - within the domain if Endurance Groups are not supported.


An Endurance Group shall be part of only one domain (refer to section 3.2.5).


An Endurance Group Identifier is a 16-bit value that specifies the Endurance Group with which an action is
associated. An Endurance Group Identifier is unique within the NVM subsystem. An Endurance Group
Identifier value of 0h is reserved and is not a valid Endurance Group Identifier. Unless otherwise specified,
if the host specifies an Endurance Group Identifier cleared to 0h for a command that requires an Endurance
Group Identifier, then that command shall abort with a status code of Invalid Field in Command.


The information that describes an Endurance Group is indicated in the Endurance Group Information log
page (refer to section 5.1.12.1.10).


Figure 69 shows Endurance Groups added to the example in Figure 67. In this example, the endurance of
NVM Set A and NVM Set B are managed together as part of Endurance Group Y, while the endurance of
NVM Set C is managed only within NVM Set C which is the only NVM Set that is part of Endurance Group
Z.


78


NVM Express [®] Base Specification, Revision 2.2


**Figure 69: NVM Sets and Associated Namespaces**


If Endurance Groups are supported, then the NVM subsystem and all controllers shall:

  - indicate support for Endurance Groups in the Controller Attributes field in the Identify Controller
data structure;

  - indicate the Endurance Group Identifier with which the namespace is associated in the Identify
Namespace data structure;

  - support the Endurance Group Information log page; and

  - support the Endurance Group Event Aggregate log page if more than one Endurance Group is
supported in the NVM subsystem.


If Endurance Groups are not supported and the host sends a command in which an Endurance Group
Identifier field is defined (e.g., Get Log Page), then that field shall be ignored by the controller.


If Endurance Groups are not supported and the controller returns information to the host that contains an
Endurance Group Identifier field, then that field shall be cleared to 0h.


**Configuring and Managing Endurance Group Events**


The host may configure asynchronous events to be triggered when certain events occur for an Endurance
Group. The host submits a Set Features command specifying the Endurance Group Event Configuration
feature (refer to section 5.1.25.1.16), the Endurance Group, and the specific event(s) that shall trigger
adding an entry to the Endurance Group Event Aggregate log page (refer to section 5.1.12.1.15).


The host configures events using a Set Features command for each Endurance Group.


The host submits a Set Features command specifying the Asynchronous Event Configuration feature (refer
to section 5.1.25.1.5) with the Endurance Group Event Aggregate Log Change Notices bit set to ‘1’ to
specify that adding an entry to the Endurance Group Event Aggregate log page shall trigger an Endurance
Group Event Aggregate Log Page Change Notice event to the host (refer to Figure 410).


79


NVM Express [®] Base Specification, Revision 2.2


The host determines the Endurance Groups that have outstanding events by reading the Endurance Group
Event Aggregate log page. An entry is returned for each Endurance Group that has an event outstanding.
The host may use the Endurance Group Identifier Maximum value reported in the Identify Controller data
structure to determine the maximum size of this log page.


To determine the specific event(s) that have occurred for a reported Endurance Group, the host reads the
Endurance Group Information log page (refer to Figure 219) for that Endurance Group. The Critical Warning
field indicates the event(s) that have occurred (e.g., that all namespaces in the Endurance Group have
been placed in read-only mode). All events for an Endurance Group are cleared if the controller successfully
processes a read for the Endurance Group Information log page for that Endurance Group, where the Get
Log Page command has the Retain Asynchronous Event bit cleared to ‘0’. If the Critical Warning field in the
Endurance Group Information log page is cleared to 0h, then events for that Endurance Group are not
reported in the Endurance Group Event Aggregate log page.


**Reclaim Groups, Reclaim Unit Handles, and Reclaim Units**


If Flexible Data Placement is enabled in an Endurance Group (refer to section 5.1.25.1.20), then the logical
view of the non-volatile storage capacity in that Endurance Group is shown in Figure 70 and consists of:

  - a set of one or more Reclaim Groups numbered from 0 to _P_ -1 where _P_ is the value of the Number
of Reclaim Groups field in the FDP Configuration Descriptor (refer to Figure 281). A Reclaim Group
consists of one or more Reclaim Units; and

  - one or more Reclaim Unit Handles numbered from 0 to _N_ -1 where _N_ is the value of the Number of
Reclaim Unit Handles field in the FDP Configuration Descriptor (refer to Figure 281).


A Reclaim Unit Handle consists of a reference to a Reclaim Unit in each Reclaim Group where user data
from a write command is placed. A Reclaim Unit referenced by the Reclaim Unit Handle is only allowed to
be referenced by at most one Reclaim Unit Handle. However, a specific Reclaim Unit is referenced by the
same or different Reclaim Unit Handles as the Reclaim Unit is cycled from erased and back into use. When
a Reclaim Unit is written to capacity, the controller updates that Reclaim Unit Handle to reference a different
Reclaim Unit that is available for writing user data (e.g., non-volatile storage media that has been erased
which is required prior to writing for program in place memories) and has not been written with any user
data (i.e., an empty Reclaim Unit). Refer to section 8.1.10 for the details of how a host is able to issue a
write command and place the user data into a Reclaim Unit.


80


NVM Express [®] Base Specification, Revision 2.2


**Figure 70: Flexible Data Placement Logical View of Non-Volatile Storage**





















**Domains and Divisions**


**Overview**


An NVM subsystem may be made up of a single domain or multiple domains (i.e., two or more). A domain
is the smallest indivisible unit that shares state (e.g., power state, capacity information). An NVM subsystem
that supports multiple domains shall support Asymmetric Namespace Access Reporting (refer to section
8.1.1).


A common example of a simple implementation of an NVM subsystem is one that consists of a single
domain (i.e., multiple domains are not supported).


Each domain is independent, and the boundaries between domains are communication boundaries (e.g.,
fault boundaries, management boundaries). If multiple domains are present in an NVM subsystem, then
those domains cooperate in the operation of that NVM subsystem. If a domain is unable to cooperate in the
operation of the NVM subsystem, then the NVM subsystem has become divided.


A division is an event (e.g., failure of a domain) or action (e.g., management action or reconfiguration) within
the NVM subsystem that affects communication between the domains contained in the NVM subsystem
(refer to Figure 71 and Figure 72). If a division exists, global state within the NVM subsystem may be
impacted (e.g., a controller may only have information about the state of the domains with which the
controller is able to communicate). A division event or action may:


  - affect access to namespaces (refer to section 8.1.1); or

  - impact operations that have NVM subsystem scope (e.g., TNVMCAP, sanitize, format, SMART
information).


81


NVM Express [®] Base Specification, Revision 2.2


A domain is comprised of:


  - zero or more controllers; and

  - zero or more NVM Endurance Groups.


If an NVM subsystem supports multiple domains, then all controllers in that NVM subsystem shall:


  - set the MDS bit to ‘1’ in the CTRATT field in the Identify Controller data structure (refer to Figure
313);

  - set the Domain Identifier in each Endurance Group descriptor, if supported, to a non-zero value;
and

  - set the Domain Identifier in each Identify Controller data structure to a non-zero value.


If an NVM subsystem supports multiple domains, then controllers in that NVM subsystem may:

  - support Endurance Groups (refer to Endurance Groups bit in the CTRATT field of Identify Controller
data structure).


For an NVM subsystem that supports multiple domains, each domain shall be assigned a domain identifier
that is unique within the NVM subsystem (refer to the Domain Identifier field in Figure 313 and section
3.2.5.3). For an NVM subsystem that does not support multiple domains, Domain Identifier fields are
cleared to 0h.


Figure 71 shows an example of an NVM subsystem that consists of three domains. Domain 1 contains two
controllers and some amount of NVM storage capacity which has been allocated to two private namespaces
(i.e., NS A and NS C) and a shared namespace (i.e., NS B). Domain 2 contains two controllers and some
amount of NVM storage capacity which has been allocated to two shared namespaces (i.e., NS D and NS
E). Domain 3 contains one controller, and no NVM storage capacity.


**Figure 71: Example 1 Domain Structure**



Port v Port w



Port _x_ Port y Port z

































If, in the example shown in Figure 71, a division event occurs that results in Domain 1 no longer being able
to communicate with Domain 2 and Domain 3, then the NVM subsystem would consist of two parts. The
first part consists of Domain 1 and the second part consists of Domain 2 and Domain 3.


Figure 72 shows an example of an NVM subsystem that consists of six domains, of which, three are
domains that contain controllers. Domain 1 is a domain that contains two controllers and some amount of
NVM storage capacity from which NVM Endurance Groups have been created that contain a private
namespace (i.e., NS A) and a shared namespace (i.e., NS C). Domain 2 is a domain that contains no
controllers and contains some amount of NVM storage capacity from which NVM Endurance Groups have
been created that contain a shared namespace (i.e., NS B). Domain 3 is a domain that contains two


82


NVM Express [®] Base Specification, Revision 2.2


controllers and no NVM storage capacity. Domain 4 is a domain that contains no controllers and contains
some amount of NVM storage capacity from which NVM Endurance Groups have been created that contain
two shared namespaces (i.e., NS D and NS E). Domain 5 is a domain that contains one controller and no
NVM storage capacity. Domain 6 is a domain that contains no controllers and no NVM storage capacity
allocated to an NVM Endurance Group (i.e., an empty domain).


**Figure 72: Example 2 Domain Structure**



Port v Port w



Port _x_ Port y Port z













































Key: - - - - (Dashed Line) – Communication Boundary


**Domains and Reservations**


If an NVM subsystem supports multiple domains and Persistent Reservations (refer to section 8.1.22), then
resumption after a division event (e.g., resumption of operation, resumption of communication) requires
that all persistent reservation state within the domains in the NVM subsystem that are no longer divided be
synchronized (i.e., updated).


If the reservation state for a namespace is not synchronized, then the ANA Group that contains that
namespace shall transition to the ANA Inaccessible state (refer to section 8.1.1.6) and remain in that state
until the Persistent Reservation state is synchronized. If the Persistent Reservation state is not able to be
synchronized, then:


  - a transition to the ANA Persistent Loss state occurs and commands are processed as described in
section 8.1.1.7; or

  - the controller may stop processing commands and set the Controller Fatal Status (CSTS.CFS) bit
to ‘1’ (refer to section 9.5).


**Domain Identifier Use (Informative)**


Domain Identifier values indicate the parts of the NVM subsystem that comprise a domain.


The host may use these values to determine which Endurance Groups (refer to section 3.2.3) are contained
in the same domain and which are contained in a different domain. Examples of host use of the domain
identifier include:


83


NVM Express [®] Base Specification, Revision 2.2


  - host data redundancy software (e.g., RAID) that may use the Endurance Group’s Domain Identifier
to determine which Endurance Groups may fail together (e.g., Endurance Groups in the same
domain) and which Endurance Groups may fail independently (e.g., Endurance Groups in different
domains); and

  - host application software may use the controller’s Domain Identifier to determine which controllers
share domains (e.g., controllers that may fail together) and which controllers are a part of different
domains (e.g., controllers that may fail independently).


**3.3** **NVM Queue Models**


The NVM Express interface is based on a paired Submission and Completion Queue mechanism.
Commands are placed by host software into a Submission Queue. Completions are placed into the
associated Completion Queue by the controller. When using a memory-based transport queue model (refer
to section 3.3.1), multiple Submission Queues may utilize the same Completion Queue. When using a
message-based transport queue model (refer to section 3.3.2) each Submission Queue maps to a single
Completion Queue.


**Memory-based Transport Queue Model (PCIe)**


**Queue Setup and Initialization**


To setup and initialize I/O Submission Queues and I/O Completion Queues for use, host software follows
these steps:


1. Configures the Admin Submission Queue and the Admin Completion Queue ~~s~~ by initializing the

Admin Queue Attributes (AQA), Admin Submission Queue Base Address (ASQ), and Admin
Completion Queue Base Address (ACQ) properties appropriately;
2. Configures the size of the I/O Submission Queues (CC.IOSQES) and I/O Completion Queues

(CC.IOCQES);
3. Submits a Set Features command with the Number of Queues attribute set to the requested

number of I/O Submission Queues and I/O Completion Queues. The completion queue entry for
this Set Features command indicates the number of I/O Submission Queues and I/O Completion
Queues allocated by the controller;
4. Determines the maximum number of entries supported per queue (CAP.MQES) and whether the

queues are required to be physically contiguous (CAP.CQR);
5. Creates I/O Completion Queues within the limitations of the number allocated by the controller and

the queue attributes supported (maximum entries and physically contiguous requirements) by using
the Create I/O Completion Queue command; and
6. Creates I/O Submission Queues within the limitations of the number allocated by the controller and

the queue attributes supported (maximum entries and physically contiguous requirements) by using
the Create I/O Submission Queue command.


At the end of this process, I/O Submission Queues and I/O Completion Queues have been setup and
initialized and may be used to complete I/O commands.


**Queue Usage**


The submitter of entries to a memory-based transport queue uses the current Tail entry pointer to identify
the next open queue slot. The submitter increments the Tail entry pointer after placing the new entry to the
open queue slot. If the Tail entry pointer increment exceeds the queue size, the Tail entry shall roll to zero.
The submitter may continue to place entries in free queue slots as long as the Full queue condition is not
met (refer to section 3.3.1.5).


Note: The submitter shall take queue wrap conditions into account.


The consumer of entries on a memory-based transport queue uses the current Head entry pointer to identify
the slot containing the next entry to be consumed. The consumer increments the Head entry pointer after
consuming the next entry from the queue. If the Head entry pointer increment exceeds the queue size, the
Head entry pointer shall roll to zero. The consumer may continue to consume entries from the queue as
long as the Empty queue condition is not met (refer to section 3.3.1.4).


84


NVM Express [®] Base Specification, Revision 2.2


Note: The consumer shall take queue wrap conditions into account.


Creation and deletion of memory-based transport Submission Queue and associated Completion Queues
are required to be ordered correctly by host software. Host software creates the Completion Queue before
creating any associated Submission Queue. Submission Queues may be created at any time after the
associated Completion Queue is created. Host software deletes all associated Submission Queues prior to
deleting a Completion Queue. To abort all commands submitted to the Submission Queue host software
issues a Delete I/O Submission Queue command for that queue (refer to section 3.3.1.3).


Host software writes the Submission Queue Tail Doorbell and the Completion Queue Head Doorbell (refer
to the Transport Specific Controller Properties section in the NVMe over PCIe Transport Specification) to
communicate new values of the corresponding entry pointers to the controller. If host software writes an
invalid value to the Submission Queue Tail Doorbell or Completion Queue Head Doorbell property and an
Asynchronous Event Request command is outstanding, then an asynchronous event is posted to the Admin
Completion Queue with a status code of Invalid Doorbell Write Value. The associated queue is then deleted
and recreated by host software. For a Submission Queue that experiences this error, the controller may
complete previously consumed commands; no additional commands are consumed. This condition may be
caused by host software attempting to add an entry to a full Submission Queue or remove an entry from an
empty Completion Queue.


Host software checks completion queue entry Phase Tag (P) bits in memory to determine whether new
completion queue entries have been posted (refer to section 4.2.4). The Completion Queue Tail pointer is
only used internally by the controller and is not visible to the host. The controller uses the SQ Head Pointer
(SQHD) field in completion queue entries to communicate new values of the Submission Queue Head
Pointer to the host. A new SQHD value indicates that submission queue entries have been consumed, but
does not indicate either execution or completion of any command. Refer to section 4.2.


A submission queue entry is submitted to the controller when the host writes the associated Submission
Queue Tail Doorbell with a new value that indicates that the Submission Queue Tail Pointer has moved to
or past the slot in which that submission queue entry was placed. A Submission Queue Tail Doorbell write
may indicate that one or more submission queue entries have been submitted.


A submission queue entry has been consumed by the controller when a completion queue entry is posted
that indicates that the Submission Queue Head Pointer has moved past the slot in which that submission
queue entry was placed. A completion queue entry may indicate that one or more submission queue entries
have been consumed.


A completion queue entry is posted to the Completion Queue when the controller write of that completion
queue entry to the next free Completion Queue slot inverts the Phase Tag (P) bit from its previous value in
memory (refer to section 4.2.4). The controller may generate an interrupt to the host to indicate that one or
more completion queue entries have been posted.


A completion queue entry has been consumed by the host when the host writes the associated Completion
Queue Head Doorbell with a new value that indicates that the Completion Queue Head Pointer has moved
past the slot in which that completion queue entry was placed. A Completion Queue Head Doorbell write
may indicate that one or more completion queue entries have been consumed.


Once a submission queue entry or a completion queue entry has been consumed, the slot in which it was
placed is free and available for reuse. Altering a submission queue entry after that entry has been submitted
but before that entry has been consumed results in undefined behavior. Altering a completion queue entry
after that entry has been posted but before that entry has been consumed results in undefined behavior.


**3.3.1.2.1** **Completion Queue Flow Control**


If there are no free slots in a Completion Queue, then the controller shall not post status to that Completion
Queue until slots become available. In this case, the controller may stop processing additional submission
queue entries associated with the affected Completion Queue until slots become available. The controller
shall continue processing for other Submission Queues not associated with the affected Completion Queue.


85


NVM Express [®] Base Specification, Revision 2.2


**Queue Abort**


To abort a large number of commands, the host may use:

   - the Cancel command (refer to section 7.1); or

   - delete and recreate the I/O Submission Queue (refer to section 3.7.3).


Specifically, to abort all commands that are submitted to an I/O Submission Queue, host software should:

  - issue a Cancel command to that queue with the Cancel Action set to Multiple Command Cancel
and the NSID field set to FFFFFFFFh; or

  - issue a Delete I/O Submission Queue command for that queue. After that submission queue has
been successfully deleted, indicating that all commands have been completed or aborted, then
host software should recreate the queue by submitting a Create I/O Submission Queue command.
Host software may then re-submit commands to the associated I/O Submission Queue.


If the host is no longer able to communicate with the controller before that host receives either:

  - completions for all outstanding commands submitted on that I/O Submission Queue (refer to
section 3.4.5); or

  - a successful completion for the Delete I/O Submission Queue command for that I/O Submission
Queue,


then it is strongly recommended that the host take the steps described in section 9.6 to avoid possible data
corruption caused by interaction between outstanding commands and subsequent commands submitted
by that host to another controller.


**Empty Queue**


The queue is Empty when the Head entry pointer equals the Tail entry pointer. Figure 73 defines the Empty
Queue condition.


**Figure 73: Empty Queue Definition**











**Full Queue**


The queue is Full when the Head equals one more than the Tail. The number of entries in a queue when
full is one less than the queue size. Figure 74 defines the Full Queue condition.


Note: Queue wrap conditions shall be taken into account when determining whether a queue is Full.


86


NVM Express [®] Base Specification, Revision 2.2


**Figure 74: Full Queue Definition**















**Message-based Transport Queue Model (Fabrics)**


For NVMe over Fabrics, a queue is a unidirectional communication channel that is used to send capsules
between a host and a controller. A host uses Submission Queues to send command capsules (refer to
section 3.3.2.1.1) to a controller. A controller uses Completion Queues to send response capsules (refer to
section 3.3.2.1.2) to a host. Submission and Completion Queues are created in pairs using the Connect
command (refer to section 3.3.2.2).


The NVMe Transport is responsible for delivering command capsules to the controller and notifying the
controller of capsule arrival in a transport-specific fashion.


Altering a command capsule between host submission to the Submission Queue and transport delivery of
that capsule to the controller results in undefined behavior.


NVMe Transports are not required to provide any additional end-to-end flow control. Specific NVMe
Transports may require low level flow control for congestion avoidance and reliability; any such additional
NVMe Transport flow control is outside the scope of this specification.


Flow control differs for Submission Queues (refer to section 3.3.2.1.1, section 3.3.2.6, and section 3.3.2.7)
and Completion Queues (refer to section 3.3.2.1.2, section 3.3.2.8, and section 3.3.1.2.1).


**Capsules and Data Transfers**


This section describes capsules and data transfer mechanisms necessary to support message-based
transport queues. These mechanisms are used for Fabrics commands, Admin commands, and I/O
commands when using the message-based transport queue model.


A capsule is an NVMe unit of information exchanged between a host and a controller. A capsule may
contain commands, responses, SGLs, and/or data. The data may include user data (e.g., logical block data
and metadata that is transferred as a contiguous part of the logical block) and data structures associated
with the command.


The capsule size for the Admin Queue commands and responses is fixed and defined in the NVMe
Transport binding specification. The controller indicates in the Identify Controller data structure the capsule
command and response sizes that the host shall use with I/O commands.


The controller shall support SGL based data transfers for commands on both the Admin Queue and I/O
Queues. Data may be transferred within the capsule or through memory transactions based on the
underlying NVMe Transport as indicated in the SGL descriptors associated with the command capsule. The
SGL types supported by an NVMe Transport are specified in the NVMe Transport binding specification.


The value of unused and not reserved capsule fields (e.g., the capsule is larger than the command /
response and associated data) is undefined and shall not be interpreted by the recipient.


87


NVM Express [®] Base Specification, Revision 2.2


**3.3.2.1.1** **Command Capsules**


A command capsule is sent from a host to a controller. It contains a submission queue entry (SQE) and
may optionally contain data or SGLs. The SQE is 64 bytes in size and contains the Admin command, I/O
command, or Fabrics command to be executed.


**Figure 75: Command Capsule**


Byte 0 63 64 ( _N_ -1)


Submission Queue Entry Data or SGLs (if present)


Command Capsule of Size N Bytes


The Command Identifier field in the SQE shall be unique among all outstanding commands associated with
that queue. If there is data or additional SGLs to be transferred within the capsule, then the SGL descriptor
in the SQE contains a Data Block, Segment Descriptor, or Last Segment Descriptor specifying an
appropriate Offset address. The definition for the submission queue entry when the command is a Fabrics
command is shown in section 4.1.2. The definition for the submission queue entry when the command is
an Admin command or I/O command is shown in section 4.1.1. Bytes 03:00 share a common format across
commands.


**3.3.2.1.2** **Response Capsules**


A response capsule is sent from the NVM subsystem to the host. It contains a completion queue entry
(CQE) and may optionally contain data. The CQE is the completion queue entry associated with a
previously issued command capsule.


If a command requests data and the SGL in the associated command capsule specifies a Data Block
descriptor with an Offset, the data is included in the response capsule. If the SGL(s) in the command
capsule specify a region in host memory, then data is transferred via memory transactions.


**Figure 76: Response Capsule**


Byte 0 15 16 ( _N_ -1)


Completion Queue Entry Data (if present)


Response Capsule of Size N Bytes


The completion queue entry is 16 bytes in size and contains a two byte status field.


The definition for the completion queue entry for a Fabrics command is shown in section 4.2.2. The
definition for the completion queue entry when the command is an Admin command or I/O command is
defined in section 4.2.1, where the SQ Identifier and Phase Tag fields are reserved because they are not
used in NVMe over Fabrics. Use of the SQHD field depends on whether SQ flow control is disabled for the
queue pair, refer to section 6.3.


**3.3.2.1.3** **Data Transfers**


Data may be transferred within capsules or by memory transfers. SGLs are used to specify the location of
data. Metadata, if transferred, is a contiguous part of the user data with which that metadata is associated.
The SGL descriptor(s) (refer to section 4.3.2) specify whether the command’s data is transferred through


88


NVM Express [®] Base Specification, Revision 2.2


memory or within the capsule. The capsule may contain either SGLs or data (not a mixture of both) following
the SQE. If additional SGLs are required, then the SGLs are included in the capsule immediately after the
SQE. If an invalid offset is specified in an SGL descriptor, then a status code of SGL Offset Invalid shall be
returned.


SGLs shall be supported within a capsule. The NVMe Transport binding specification defines the SGL
Descriptor Types and Sub Types that are supported for the corresponding NVMe Transport. The NVMe
Transport binding specification also specifies if SGLs may be supported in host memory.


**Data and SGL Locations within a Command Capsule**


The submission queue entry within the command capsule includes one SGL entry. If there are additional
SGL entries to be transferred in the command capsule, then those entries shall be contiguous and located
immediately after the submission queue entry.


An NVMe Transport binding specification defines the support for data as part of the command capsule. The
controller indicates the starting location of data within a command capsule via the In Capsule Data Offset
(ICDOFF) field in the Identify Controller data structure.


There are restrictions for SGLs that the host should follow:

  - if the ICDOFF field is a non-zero value, then all SGL descriptors following the submission queue
entry shall not have a total size greater than (ICDOFF * 16);

  - if the SGL descriptors following the submission queue entry have a total size greater than (ICDOFF

    - 16), then the controller shall abort the command with a status code of Invalid Number of SGL
Descriptors;

  - the host shall not place more SGL Data Block or Keyed SGL Data Block descriptors within a
capsule than the maximum indicated in the Identify Controller data structure; and

  - if the host places more SGL Data Block of Keyed SGL Data Block descriptors in a capsule than the
maximum indicated in the Maximum SGL Data Block Descriptors field in the Identify Controller data
structure, then the controller shall abort the command with a status code of Invalid Number of SGL
Descriptors.


The host shall start data (if present) in command capsules at byte offset (ICDOFF * 16) from the end of the
submission queue entry.


89


NVM Express [®] Base Specification, Revision 2.2


**Figure 77: Data and SGL Locations within a Command Capsule**



Byte 0 63 64


Additional SGLs
Submission Queue Entry

(if present)


Command Capsule of Size N Bytes



( _M_ -1) ( _N_ -1)


Undefined



(ICDOFF * 16) + 64



Command Capsule of Size N Bytes


**Data Transfer Examples**





The data transfer examples in Figure 78 and Figure 79 show SGL examples for a Write command where
data is transferred via a memory transaction or within the capsule. The SGL may use a key as part of the
data transfer depending on the requirements of the NVMe Transport used.


The first example shows an 8KiB write where all of the data is transferred via memory transactions. In this
case, there is one SGL descriptor that is contained within the submission queue entry at CMD.SGL1. The
SGL descriptor is a Keyed SGL Data Block descriptor. If more SGLs are required to complete the command,
the additional SGLs are contained in the command capsule.


**Figure 78: SGL Example Using Memory Transactions**







through memory







90


NVM Express [®] Base Specification, Revision 2.2


The second example shows an 8KiB write where all of the data is transferred within the capsule. In this
case, the SGL descriptor is an SGL Data Block descriptor specifying an Offset of 20h based on an ICDOFF
value of 2h.


**Figure 79: SGL Example Using In Capsule Data Transfer**



Byte 0



63 64 96 ( _N_ -1)





















**Queue Creation**


Message-based controllers use the Connect command (refer to section 6.3) to create Admin Queues or I/O
Queues. The creation of an Admin Queue establishes an association between a host and the corresponding
controller. The message-based transport queue model does not support the Admin Submission Queue
Base Address (ASQ), Admin Completion Queue Base Address (ACQ), and Admin Queue Attributes (AQA)
properties as all information necessary to establish an Admin Queue is contained in the Connect command.
The message-based transport queue model does not support the Admin commands associated with I/O
Queue creation and deletion (i.e., Create I/O Completion Queue, Create I/O Submission Queue, Delete I/O
Completion Queue, Delete I/O Submission Queue).


An NVMe Transport connection is established between a host and an NVM subsystem prior to the transfer
of any capsules or data. The mechanism used to establish an NVMe Transport connection is NVMe
Transport specific and defined by the corresponding NVMe Transport binding specification. The NVMe
Transport may require a separate NVMe Transport connection for each Admin Queue or I/O Queue or may
utilize the same NVMe Transport connection for all Admin and I/O Queues associated with a particular
controller. An NVMe Transport may also require that NVMe layer information be passed between the host
and controller in the process of establishing an NVMe Transport connection (e.g., exchange queue size to
appropriately size send and receive buffers).


The Connect command specifies the Queue ID and type (Admin or I/O), the size of the Submission and
Completion Queues, queue attributes, Host NQN, NVM Subsystem NQN, and Host Identifier. The Connect
command may specify a particular controller if the NVM subsystem supports a static controller model. The
Connect response indicates whether the connection was successfully established as well as whether NVMe
in-band authentication is required.


The Connect command is submitted to the same Admin Queue or I/O Queue that the Connect command
creates. The underlying NVMe Transport connection that is used for that queue is created first and the
Connect command and response capsules are sent over that NVMe Transport connection. The Connect
command shall be sent once to a queue.


When a Connect command successfully completes, the corresponding Submission and Completion
Queues are created. If NVMe in-band authentication is required as indicated in the Connect response, then


91


NVM Express [®] Base Specification, Revision 2.2


NVMe in-band authentication shall be performed before the queues may be used to perform other Fabrics
commands, Admin commands, or I/O commands.


Once a Connect command for an Admin Queue has completed successfully (and NVMe in-band
authentication, if required, has succeeded), only Fabrics commands may be submitted until the controller
is ready (CSTS.RDY = 1). Both Fabrics commands and Admin commands may be submitted to the Admin
Queue while the controller is ready. A Connect command for an I/O Queue may be submitted after the
controller is ready. Once a Connect command for an I/O Queue has completed successfully (and NVMe inband authentication, if required, has succeeded), I/O commands may be submitted to the queue.


The Connect response contains the controller ID allocated to the host.


After an Admin Queue is created on a controller, all subsequent Connect commands sent from the same
host to that controller, to create an I/O Queue, are required to:

  - utilize the same NVMe Transport;

  - have the same Host NQN;

  - have the same NVM Subsystem NQN; and

  - either have the:

`o` same Host Identifier value; or

`o` a Host Identifier value of 0h, if supported (refer to section 5.1.12.3.1).


**Queue Initialization and Queue State**


When a Connect command successfully completes, the corresponding Admin Submission and Completion
Queue or I/O Submission and Completion Queues are created. If the host sends a Connect command
specifying the Queue ID of a queue which already exists, then the controller shall abort the command with
a status code of Command Sequence Error.


The Authentication Requirements (AUTHREQ) field in the Connect response indicates if NVMe in-band
authentication is required. If AUTHREQ is cleared to 0h, the created queue is ready for use after the
Connect command completes successfully. If AUTHREQ is set to a non-zero value, the created queue is
ready for use after NVMe in-band authentication has been performed successfully using the Authentication
Send and Authentication Receive Fabrics commands.


If a controller requires or is undergoing NVMe in-band authentication for a queue pair, then a controller
shall abort all commands received on that queue other than authentication commands with a status code
of Authentication Required. After the NVMe in-band authentication has been performed successfully on a
queue, then a controller shall abort all authentication commands on that queue with a status code of
Command Sequence Error.


When an Admin Queue is first created, the associated controller is disabled (i.e., CC.EN is initialized to ‘0’).
A disabled controller shall abort all commands other than Fabrics commands on the Admin Queue with a
status code of Command Sequence Error. After the controller is enabled, it shall accept all supported Admin
commands in addition to Fabrics commands.


A created I/O queue shall abort all commands with a status code of Command Sequence Error if the
associated controller is disabled.


**I/O Queue Deletion**


NVMe over Fabrics deletes an individual I/O Queue and may delete the associated NVMe Transport
connection as a result of:

  - the exchange of a Disconnect command and response (refer to section 6.4) between a host and
controller; or

  - the detection and processing of a transport error on an NVMe Transport connection.


The host indicates support for the deletion of an individual I/O Queue by setting the Individual I/O Queue
Deletion Support (INDIVIOQDELS) bit to ‘1’ in the CATTR field in the Connect command (refer to Figure
546) used to create the Admin Queue. The controller indicates support for the deletion of an individual I/O


92


NVM Express [®] Base Specification, Revision 2.2


Queue by setting the Disconnect Command Support (DCS) bit to ‘1’ in the OFCS field of the Identify
Controller data structure (refer to Figure 313).


If both the host and the controller support deletion of an individual I/O Queue, then the termination of an
individual I/O Queue impacts only that I/O Queue (i.e., the association and all other I/O Queues and their
associated NVMe Transport connections are not impacted). If either the host or the controller does not
support deletion of an individual I/O Queue, then the deletion of an individual I/O Queue or the termination
of an NVMe Transport connection causes the association to be terminated.


NVMe over Fabrics uses the Disconnect command to delete an Individual I/O Queue. This command is
sent on the I/O Submission Queue to be deleted and affects only that I/O Submission Queue and its
associated I/O Completion Queue (i.e., other I/O Queues are not affected). To delete an I/O Queue, the
NVMe Transport connection for that I/O Queue is used. If all Queues associated with an NVMe Transport
connection are deleted, then the NVMe Transport connection may be deleted after completion of the
Disconnect command. Actions necessary to delete the NVMe Transport connection are transport specific.
The association between the host and the controller is not affected.


If a Disconnect command returns a status code other than success, the host may delete an I/O Queue
using other methods including:

  - waiting a vendor specific amount of time and retry the Disconnect command;

  - deleting the NVMe Transport connection (note: this may impact other I/O Queues);

  - performing a Controller Level Reset (note: this impacts other I/O Queues); or

  - ending the host to controller association.


If the transport requires a separate NVMe Transport connection for each Admin and I/O Queue (refer to
section 3.3.2.2), then the host should not delete an NVMe Transport connection until after:

  - a Disconnect command has been submitted to the I/O Submission Queue; and

  - the response for that Disconnect command has been received by the host on the corresponding
I/O Completion Queue or a vendor specific timeout (refer to section 3.9) has occurred while waiting
for that response.


If the transport requires a separate NVMe Transport connection for each Admin and I/O Queue, then the
controller should not delete an NVMe Transport connection until after:

  - a Disconnect command has been received on the I/O Submission Queue and processed by the
controller;

  - the responses for commands received by the controller on that I/O Submission Queue prior to
receiving the Disconnect command have been sent to the host on the corresponding I/O
Completion Queue; and

  - the resulting response for that Disconnect command has been sent to the host on the
corresponding I/O Completion queue (i.e., this response is the last response sent). It is
recommended that the controller delay destroying the NVMe Transport connection to allow time for
the Disconnect command response to be received by the host (e.g., a transport specific event
occurs or a transport specific time period elapses).


If the transport utilizes the same NVMe Transport connection for all Admin and I/O Queues associated with
a particular controller (refer to section 3.3.2.2), then the deletion of an individual I/O Queue has no impact
on the NVMe Transport connection.


A Disconnect command is the last I/O Submission Queue entry processed by the controller for an I/O
Queue. Controller processing of the Disconnect command completes or aborts all commands on the I/O
Queue on which the Disconnect command was received. The controller determines whether to complete
or abort each of those commands. Until the controller sends a successful completion for a Disconnect
command, outstanding commands may continue being processed by the controller. The controller ensures
that there is no further processing of any command sent on that I/O Queue after posting the completion
queue entry for the Disconnect command as described in section 6.4.


93


NVM Express [®] Base Specification, Revision 2.2


The response to the Disconnect command is the last I/O Completion Queue entry processed by the host
for an I/O Queue. To avoid command aborts, the host should wait for all outstanding commands on an I/O
Queue to complete before sending the Disconnect command.


If the controller terminates an NVMe Transport connection or detects an NVMe Transport connection loss,
then the controller shall stop processing all commands received on I/O Queues associated with that NVMe
Transport connection within the time reported in the CQT field (refer to Figure 313), if non-zero.


If the host terminates an NVMe Transport connection or detects an NVMe Transport connection loss before
the responses are received for all outstanding commands submitted to the associated I/O Queue (refer to
section 3.4.5), then it is strongly recommended that the host take the steps described in section 9.6 to avoid
possible data corruption caused by interaction between outstanding commands and subsequent
commands submitted by that host to another controller.


**Submission Queue Flow Control Negotiation**


Use of Submission Queue (SQ) flow control is negotiated for each queue pair by the Connect command
and the controller response to the Connect command. SQ flow control shall be used unless it is disabled
as a result of that negotiation. If SQ flow control is disabled, then the Submission Queue Head Pointer
(SQHD) field is reserved in all Fabrics response capsules for that queue pair after the response to the
Connect command (i.e., in all subsequent response capsules for that queue pair, the controller shall clear
the SQHD field to 0h and the host should ignore the SQHD field).


If the host requests that SQ flow control be disabled for a queue pair, then the host should size each
Submission Queue to support the maximum number of commands that the host could have outstanding at
one time for that Submission Queue.


The maximum size of the Admin Submission Queue is specified in the Admin Max SQ Size (ASQSZ) field
of the Discovery Log Page Entry for the NVM subsystem (refer to section 5.1.12.3.1).


The maximum size of an I/O Submission Queue is specified in the Maximum Queue Entries Supported
(MQES) field of the Controller Capabilities (CAP) property for the controller (refer to section 3.1.4.1).


The value of the Maximum Outstanding Commands (MAXCMD) field in the Identify Controller data structure
indicates the maximum number of commands that the controller processes at one time for a particular I/O
Queue. The host may use this value to size I/O Submission Queues and optimize the number of commands
submitted at one time per queue to achieve the best performance.


If SQ flow control is disabled, then the host should limit the number of outstanding commands for a queue
pair to be less than the size of the Submission Queue. If the controller detects that the number of
outstanding commands for a queue pair is greater than or equal to the size of the Submission Queue, then
the controller shall:


a) stop processing commands and set the Controller Fatal Status (CSTS.CFS) bit to ‘1’ (refer to

section 9.5); and
b) terminate the NVMe Transport connection and end the association between the host and the

controller.


**Submission Queue Flow Control**


This section applies only to Submission Queues that use SQ flow control.


The Submission Queue has a Head entry pointer and a Tail entry pointer that are used to manage the
queue and determine the number of Submission Queue capsules available to the host for new submissions.
The Head and Tail entry pointers are initialized to 0h when a queue is created. All arithmetic operations
and comparisons on entry pointers are performed modulo the queue size with queue wrap conditions taken
into account. The host increments the Tail entry pointer when the host adds a capsule to a queue. The
controller increments the Head entry pointer when that controller removes a capsule from the queue.


The Submission Queue Head entry pointer is maintained by the controller and is communicated to the host
in the SQHD field of completion queue entries. The host uses the received SQHD values for Submission
Queue management (e.g., to determine whether the Submission Queue is full).


94


NVM Express [®] Base Specification, Revision 2.2


The Submission Queue Tail entry pointer is local to the host and is not communicated to the controller.


The Submission Queue is full when the Head entry pointer equals one more than the Tail entry pointer (i.e.,
incrementing the Tail entry pointer has caused it to wrap around to just behind the Head entry pointer). A
full Submission Queue contains one less capsule than the queue size. A host may continue to submit
commands to a Submission Queue as long as the queue is not full.


If the controller detects that the host has submitted a command capsule to a full Submission Queue, then
the controller shall:


a) stop processing commands and set the Controller Fatal Status (CSTS.CFS) bit to ‘1’ (refer to

section 9.5); and
b) terminate the NVMe Transport connection and end the association between the host and the

controller.


The Submission Queue is empty when the Head entry pointer equals the Tail entry pointer.


**Submission Queue Head Pointer Update Optimization**


Submission Queue Head Pointer update optimization does not apply to queue pairs for which Submission
Queue (SQ) flow control is disabled, as the SQHD field is reserved if SQ flow control is disabled, refer to
section 3.3.2.5 and to section 6.3.


The NVMe Transport may omit transmission of the SQHD value for a response capsule that:


a) contains a Generic Command status (i.e., Status Code Type 0h) indicating successful completion

of a command (i.e., Status Code 00h);
b) is not a Connect response capsule; and
c) is not a Disconnect response capsule.


If a new SQHD value is not received in a response capsule, the host continues to use its previous SQHD
value. Thus, at the NVMe layer there is a logical progression of SQHD values despite the fact that the
NVMe Transport may not actually transfer the SQHD value in each response capsule.


The NVMe Transport may deliver response capsules that do not contain an SQHD value to the host in any
order. The applicable NVMe Transport binding specification defines how presence versus absence of an
SQHD value in a response capsule is indicated by the NVMe Transport.


Periodic SQHD updates at the host are required to avoid Submission Queue (SQ) starvation as SQHD
value transmission in responses is the only means of releasing SQ slots for host reuse.


An NVMe Transport may transmit an SQHD value in every response capsule. If an NVMe Transport does
not transmit an SQHD value in every response capsule, then an SQHD value should be transmitted
periodically (e.g., in at least one of every n response capsules on a CQ, where n is 10% of the size of the
associated SQ) or more often. An SQHD value should always be transmitted if 90% or more of the slots in
the associated SQ are occupied at the subsystem.


**Completion Queue Considerations**


Completion Queue flow control (refer to section 3.3.1.2.1) is not used in the message-based transport
queue model. Message-based transport Completion Queues do not use either Head entry pointers or Tail
entry pointers.


The host should size each Completion Queue to support the maximum number of commands that the host
could have outstanding at one time for a particular Submission Queue. The Completion Queue size may
be larger than the size of the corresponding Submission Queue to accommodate responses for commands
that are being processed by the controller in addition to responses for commands that are still in the
Submission Queue.


If the size of a Completion Queue is too small for the number of outstanding commands and the controller
submits a response capsule to a full Completion Queue, then the results are undefined.


95


NVM Express [®] Base Specification, Revision 2.2


The value of the Maximum Outstanding Commands (MAXCMD) field in the Identify Controller data structure
indicates the maximum number of commands that the controller processes at one time for a particular I/O
Queue. The host may use this value to size I/O Completion Queues and optimize the number of commands
submitted at one time per queue to achieve the best performance.


Altering a response capsule between controller submission to the Completion Queue and transport delivery
of that capsule to the host results in undefined behavior.


**Transport Requirements**


This section defines requirements that all NVMe Transports that support an NVMe over Fabrics
implementation shall meet.


The NVMe Transport may support NVMe Transport error detection and report errors to the NVMe layer in
command status values. The controller may record NVMe Transport specific errors in the Error Information
log page (refer to section 5.1.12.1.2). Transport errors that cause loss of a message or loss of data in a
way that the low-level NVMe Transport cannot replay or recover should cause:

  - the deletion of the individual I/O Queues (refer to section 3.3.2.4) and the associated NVMe
Transport connection on which that NVMe Transport level error occurred; or

  - termination of the NVMe Transport connection and the association between the host and controller.


The NVMe Transport shall provide reliable delivery of capsules between a host and NVM subsystem (and
allocated controller) over each connection. The NVMe Transport may deliver command capsules in any
order on each queue except for I/O commands that are part of fused operations (refer to section 3.4.2).


For command capsules that are part of fused operations for I/O commands, the NVMe Transport:


1. shall deliver the first and second command capsules for each fused operation to the queue inorder; and
2. shall not deliver any other command capsule for the same Submission Queue between delivery of
the two command capsules for a fused operation.


The NVMe Transport shall provide reliable delivery of response capsules from an NVMe subsystem to a
host over each connection. The NVMe Transport shall deliver response capsules that include an SQ Head
Pointer (SQHD) value to the host in-order; this includes all Connect response capsules and all Disconnect
response capsules.


**Queueing Attributes**


**Queue Size**


The Queue Size is indicated in a 16-bit 0’s based field that indicates the number of slots in the queue. The
minimum size for a queue is two slots. The maximum size for either an I/O Submission Queue or an I/O
Completion Queue is defined as 65,536 slots, limited by the maximum queue size supported by the
controller that is reported in the CAP.MQES field. The maximum size for the Admin Submission Queue and
Admin Completion Queue is defined as 4,096 slots. One slot in each queue is not available for use due to
Head and Tail entry pointer definition.


For Message-based controllers, the maximum size for the Admin Submission Queue is limited by the value
indicated in the ASQSZ field in the Discovery Log Page Entry data structure (refer to Figure 295).


**Queue Identifier**


Each queue is identified through a 16-bit ID value that is assigned to the queue when it is created. Both I/O
Submission Queue identifiers and I/O Completion Queue identifiers are a value from 1 to 65,535.


**Queue Priority**


If the weighted round robin with urgent priority class arbitration mechanism is supported, then host software
may assign a queue priority service class of Urgent, High, Medium, or Low. If the weighted round robin with


96


NVM Express [®] Base Specification, Revision 2.2


urgent priority class arbitration mechanism is not supported, then the priority setting is not used and is
ignored by the controller.


**Queue Coordination**


There is one Admin Queue pair associated with multiple I/O queue pairs. The Admin Submission Queue
and Completion Queue are used to carry out functions that impact the entire controller. An I/O Submission
Queue and Completion Queue may be used to carry out I/O (read/write) operations and may be distributed
across CPU cores and threads.


An Admin command may impact one or more I/O queue pairs. The host should ensure that Admin actions
are coordinated with threads that are responsible for the I/O queue pairs to avoid unnecessary error
conditions. The details of this coordination are outside the scope of this specification.


**3.4** **Command Processing**


This section describes the command issue and completion mechanism. It also describes how commands
are built by host software and command completion processing.


Commands shall only be submitted by the host when the controller is ready as indicated in the Controller
Status property (CSTS.RDY) and after appropriate I/O Submission Queue(s) and I/O Completion Queue(s)
have been created.


**Command Ordering Requirements**


Commands which are not part of a fused operation (refer to section 3.4.2) and which comply with atomic
operations requirements (refer to section 3.4.3), are processed as independent entities without reference
to other commands submitted to the same I/O Submission Queue or to commands submitted to other I/O
Submission Queues. For example, the controller is not responsible for checking the LBA of an NVM
Command Set Read command or Write command to ensure any type of ordering between commands. If a
Read command is submitted for LBA _x_ and there is a Write command also submitted for LBA _x_, there is no
guarantee of the order of completion for those commands (the Read command may finish first or the Write
command may finish first). If there are ordering requirements between these commands, host software or
the associated application is required to enforce that ordering above the level of the controller.


**Fused Operations**


Fused operations enable a more complex command by “fusing” together two simpler commands. This
feature is optional; support for this feature is indicated in the FUSES field in the Identify Controller data
structure in Figure 313.


Whether a command is part of a fused operation is specified by the Fused Operation (FUSE) field of
Command Dword 0 shown in Figure 91. The FUSE field also specifies whether the command is the first
command in the fused operation or the second command in the fused operation. If the FUSE field is set to
a non-zero value and the controller does not support the requested fused operation, then the controller
should abort the command with a status code of Invalid Field in Command.


In a fused operation, the requirements are:

  - The commands shall be executed in sequence as an atomic unit. The controller shall behave as if
no other operations have been executed between these two commands;

  - The operation ends at the point an error is encountered in either command. If the first command in
the sequence failed, then the second command in the sequence shall be aborted. If the second
command in the sequence failed, then the completion status of the first command is sequence
specific and is defined within the Fused Operation section of the applicable I/O Command Set
specification;

  - The commands shall be inserted next to each other in the same Submission Queue. If the controller
processes a command violating this condition (e.g., a command with the FUSE field cleared to 00b
(i.e., Normal operation) is inserted immediately after a command specifying the FUSE field set to
01b (i.e., Fused operation, first command), or is inserted immediately before a command specifying


97


NVM Express [®] Base Specification, Revision 2.2


the FUSE field set to 10b (i.e., Fused operation, second command)), then the controller shall abort
the command specifying non-zero values of the FUSE field with a status code of Command Aborted
due to Missing Fused Command. If the first command is in the last slot in the Submission Queue,
then the second command shall be in the first slot in the Submission Queue as part of wrapping
around. In the memory-based transport queue model, the Submission Queue Tail doorbell pointer
update shall indicate both commands as part of one doorbell update. In the message-based
transport queue model, the command capsules shall be submitted in-order;

  - To abort the fused operation, the host submits an Abort command separately for each of the
commands; and

  - A completion queue entry is posted by the controller for each of the commands.


Refer to each I/O Command Set specification for applicability and additional details, if any.


**Atomic Operations**


The definition for atomic operations is command set specific. Refer to each I/O Command Set specification
for applicability and additional details, if any.


**Command Arbitration**


After a command has been submitted to the controller (refer to section 1.5.19), the controller transfers
submitted commands into the controller for subsequent processing using a vendor specific algorithm.


A command is being processed when the controller and/or namespace state is being accessed or modified
by the command such as:

  - a Feature setting is being accessed;

  - a Feature setting is being modified;

  - user data (e.g., a logical block as defined by the NVM Command Set Specification) is being
accessed; or

  - user data is being modified.


A command is completed when a completion queue entry for the command has been posted to the
corresponding Completion Queue. Upon completion, all controller state and/or namespace state
modifications made by that command are globally visible to all subsequently submitted commands.


A candidate command is a submitted command which has been transferred into the controller that the
controller deems ready for processing. The controller selects command(s) for processing from the pool of
submitted commands for each Submission Queue. The commands that comprise a fused operation shall
be processed together and in order by the controller. The controller may select candidate commands for
processing in any order. The order in which commands are selected for processing does not imply the order
in which commands are completed.


Arbitration is the method used to determine the Submission Queue from which the controller starts
processing the next candidate command(s). Once a Submission Queue is selected using arbitration, the
Arbitration Burst setting determines the maximum number of commands that the controller may start
processing from that Submission Queue before arbitration shall again take place. A fused operation may
be considered as one or two commands by the controller.


All controllers shall support the round robin command arbitration mechanism. A controller may optionally
implement weighted round robin with urgent priority class and/or a vendor specific arbitration mechanism.
The Arbitration Mechanism Supported field in the Controller Capabilities property (CC.AMS) indicates
optional arbitration mechanisms supported by the controller.


In order to make efficient use of the non-volatile memory, it is often advantageous to execute multiple
commands from a Submission Queue in parallel. For Submission Queues that are using weighted round
robin with urgent priority class or round robin arbitration, host software may configure an Arbitration Burst
setting. The Arbitration Burst setting indicates the maximum number of commands that the controller may
launch at one time from a particular Submission Queue. It is recommended that host software configure
the Arbitration Burst setting as close to the recommended value by the controller as possible (specified in


98


NVM Express [®] Base Specification, Revision 2.2


the Recommended Arbitration Burst field of the Identify Controller data structure in Figure 313), taking into
consideration any latency requirements. Refer to section 5.1.25.1.1.


**Round Robin Arbitration**


If the round robin arbitration mechanism is selected, the controller shall implement round robin command
arbitration amongst all Submission Queues, including the Admin Submission Queue. In this case, all
Submission Queues are treated with equal priority. The controller may select multiple candidate commands
for processing from each Submission Queue per round based on the Arbitration Burst setting.


**Figure 80: Round Robin Arbitration**


ASQ


SQ



SQ


SQ





**Weighted Round Robin with Urgent Priority Class Arbitration**


In this arbitration mechanism, there are three strict priority classes and three weighted round robin priority
levels. If Submission Queue A is of higher strict priority than Submission Queue B, then all candidate
commands in Submission Queue A shall start processing before candidate commands from Submission
Queue B start processing.


The highest strict priority class is the Admin class that includes any command submitted to the Admin
Submission Queue. This class has the highest strict priority above commands submitted to any other
Submission Queue.


The next highest strict priority class is the Urgent class. Any I/O Submission Queue assigned to the Urgent
priority class is serviced next after commands submitted to the Admin Submission Queue, and before any
commands submitted to a weighted round robin priority level. Host software should use care in assigning
any Submission Queue to the Urgent priority class since there is the potential to starve I/O Submission
Queues in the weighted round robin priority levels as there is no fairness protocol between Urgent and non
Urgent I/O Submission Queues.


The lowest strict priority class is the Weighted Round Robin class. This class consists of the three weighted
round robin priority levels (High, Medium, and Low) that share the remaining bandwidth using weighted
round robin arbitration. Host software controls the weights for the High, Medium, and Low service classes
via the Set Features command. Round robin is used to arbitrate within multiple Submission Queues
assigned to the same weighted round robin level. The number of candidate commands that may start
processing from each Submission Queue per round is either the Arbitration Burst setting or the remaining
weighted round robin credits, whichever is smaller.


99


Admin



NVM Express [®] Base Specification, Revision 2.2


**Figure 81: Weighted Round Robin with Urgent Priority Class Arbitration**


ASQ



SQ





SQ



High
Priority


Medium

Priority


Low
Priority



SQ


SQ


SQ


SQ


SQ


SQ


SQ


SQ


SQ














|Col1|Col2|Col3|
|---|---|---|
|RR|Weig|ht(Medium)|
|RR|||
|RR|||



In Figure 81, the Priority decision point selects the highest priority candidate command selected next to
start processing.


**Vendor Specific Arbitration**


A vendor may choose to implement a vendor specific arbitration mechanism. The mechanism(s) are outside
the scope of this specification.


**Outstanding Commands**


A command is outstanding if:

  - the host has submitted that command to the controller;

  - the host has not received a completion for that command; and

  - as described in this section:


`o` the host has not performed an action that causes that command to no longer be outstanding;
and

`o` the host has not otherwise determined that that command is no longer outstanding.


A submitted command is no longer outstanding after the host:

  - receives a completion for that command;


100


NVM Express [®] Base Specification, Revision 2.2


  - receives a successful completion with Immediate Abort Not Performed bit cleared to ‘0’ in Dword 0
of the completion queue entry for an Abort command specifying that outstanding command (refer
to section 5.1.1);

  - receives a successful completion with the Commands Aborted field set to 1h for a Cancel command
with an Action Code of Single Command Cancel and specifying that outstanding command (refer
to section 7.1);

  - reads a CSTS.RDY bit value that indicates a controller is not able to process commands except for
Fabrics commands (i.e., a value of ‘0’), if that outstanding command is not a Fabrics command
(refer to section 3.7.2);

  - reads a CSTS.SHST field value that indicates that the controller shutdown is complete (i.e., a value
of 10b), if that outstanding command is not a Fabrics command (refer to section 3.6.1 for memorybased transports and section 3.6.2 for message-based transports);

  - if using a memory-based transport, receives a successful completion for a Delete I/O Submission
Queue command if that outstanding command was sent on the deleted I/O Submission queue
(refer to section 3.3.1.3); or

  - if using a message-based transport:


`o` receives a successful completion for a Disconnect command if that outstanding command was
sent on the same I/O queue as the Disconnect command (refer to section 3.3.2.4); or

`o` restores communication to the same controller after losing communication to that controller
(refer to section 3.9.5).


If an outstanding command ceases to be outstanding for one of these reasons, then further controller
processing of that command is no longer possible.


**3.5** **Controller Initialization**


This section describes the recommended procedure for initializing a controller.


**Memory-based Controller Initialization (PCIe)**


Upon completion of the transport-specific controller initialization steps defined within the relevant NVMe
Transport binding specification, the host should perform the following sequence of actions to initialize the
controller to begin executing commands:


1. The host waits for the controller to indicate that any previous reset is complete by waiting for

CSTS.RDY to become ‘0’;
2. The host configures the Admin Queue by setting the Admin Queue Attributes (AQA), Admin

Submission Queue Base Address (ASQ), and Admin Completion Queue Base Address (ACQ) to
appropriate values;
3. The host determines the supported I/O Command Sets by checking the state of CAP.CSS and

appropriately initializing CC.CSS as follows:


a. If the CAP.CSS.NOIOCSS bit is set to ‘1’, then the CC.CSS field should be set to 111b;
b. If the CAP.CSS.IOCSS bit is set to ‘1’, then the CC.CSS field should be set to 110b; and
c. If the CAP.CSS.IOCSS bit is cleared to ‘0’ and the CAP.CSS.NCSS bit is set to ‘1’, then the

CC.CSS field should be set to 000b;


4. The controller settings should be configured. Specifically:


a. The arbitration mechanism should be selected in CC.AMS; and
b. The memory page size should be initialized in CC.MPS;


5. The host enables the controller by setting CC.EN to ‘1’;
6. The host waits for the controller to indicate that the controller is ready to process commands. The

controller is ready to process commands when CSTS.RDY is set to ‘1’;
7. The host determines the configuration of the controller by issuing the Identify command specifying

the Identify Controller data structure (i.e., CNS 01h);


101


NVM Express [®] Base Specification, Revision 2.2


8. The host determines any I/O Command Set specific configuration information as follows:


a. If the CAP.CSS.IOCSS bit is set to ‘1’, then the host does the following:


i. Issue the Identify command specifying the Identify I/O Command Set data structure (CNS
1Ch); and
ii. Issue the Set Features command with the I/O Command Set Profile Feature Identifier (FID
19h) specifying the index of the I/O Command Set Combination (refer to Figure 328) to be
enabled;


and


b. For each I/O Command Set that is enabled (Note: the NVM Command Set is enabled if the

CC.CSS field is set to 000b):


i. Issue the Identify command specifying the I/O Command Set specific Active Namespace
ID list (CNS 07h) with the appropriate Command Set Identifier (CSI) value of that I/O
Command Set; and
ii. For each NSID that is returned:


1. If the enabled I/O Command Set is the NVM Command Set or an I/O Command Set

based on the NVM Command Set (e.g., the Zoned Namespace Command Set) issue
the Identify command specifying the Identify Namespace data structure (CNS 00h);
and
2. Issue the Identify command specifying each of the following data structures (refer to

Figure 311): the I/O Command Set specific Identify Namespace data structure, the I/O
Command Set specific Identify Controller data structure, and the I/O Command Set
independent Identify Namespace data structure;


9. If the controller implements I/O queues, then the host should determine the number of I/O

Submission Queues and I/O Completion Queues supported using the Set Features command with
the Number of Queues feature identifier. After determining the number of I/O Queues, the NVMe
Transport specific interrupt registers (e.g., MSI and/or MSI-X registers) should be configured;
10. If the controller implements I/O queues, then the host should allocate the appropriate number of

I/O Completion Queues based on the number required for the system configuration and the number
supported by the controller. The I/O Completion Queues are allocated using the Create I/O
Completion Queue command;
11. If the controller implements I/O queues, then the host should allocate the appropriate number of

I/O Submission Queues based on the number required for the system configuration and the number
supported by the controller. The I/O Submission Queues are allocated using the Create I/O
Submission Queue command; and
12. To enable asynchronous notification of optional events, the host should issue a Set Features

command specifying the events to enable. To enable asynchronous notification of events, the host
should submit an appropriate number of Asynchronous Event Request commands. This step may
be done at any point after the controller signals that the controller is ready (i.e., CSTS.RDY is set
to ‘1’).


After performing these steps, the controller shall be ready to process Admin or I/O commands issued by
the host.


For exit of the D3 power state (refer to the PCI Express Base Specification), the initialization steps outlined
should be followed.


**Message-based Controller Initialization (Fabrics)**


The host selects the NVM subsystem with which to create a host to controller association. The host first
establishes an NVMe Transport connection with the NVM subsystem. Next the host forms an association
with a controller and creates the Admin Queue using the Fabrics Connect command. Finally, the host
configures the controller and creates I/O Queues. Figure 82 is a ladder diagram that describes the queue
creation process for an Admin Queue or an I/O Queue.


102


NVM Express [®] Base Specification, Revision 2.2


**Figure 82: Queue Creation Flow**


Controller ID and
AUTHREQ returned





If AUTHREQ  0


The controller initialization steps after an association is established are described below. For determining
capabilities or configuring properties, the host uses the Property Get command and Property Set command,
respectively.


1. NVMe in-band authentication is performed if required (refer to section 8.3.4.2);
2. The host determines the controller capabilities;
3. The host determines the supported I/O Command Sets by checking the state of CAP.CSS and

appropriately initializing CC.CSS as follows:


a. If the CAP.CSS.NOIOCSS bit is set to ‘1’, then the CC.CSS field should be set to 111b;
b. If the CAP.CSS.IOCSS bit is set to ‘1’, then the CC.CSS field should be set to 110b; and
c. If the CAP.CSS.IOCSS bit is cleared to ‘0’ and the CAP.CSS.NCSS bit is set to ‘1’, then the

CC.CSS field should be set to 000b;


4. The host configures controller settings. Specific settings include:


a. The arbitration mechanism should be selected in CC.AMS; and
b. The memory page size should be initialized in CC.MPS;


5. The controller should be enabled by setting CC.EN to ‘1’;
6. The host should wait for the controller to indicate the controller is ready to process commands. The

controller is ready to process commands when CSTS.RDY is set to ‘1’;
7. The host determines the configuration of the controller by issuing the Identify command specifying

the Identify Controller data structure (i.e., CNS 01h);
8. The host determines any I/O Command Set specific configuration information as follows:


a. If the CAP.CSS.IOCSS bit is set to ‘1’, then the host does the following:


i. Issue the Identify command specifying the Identify I/O Command Set data structure (CNS
1Ch); and


103


NVM Express [®] Base Specification, Revision 2.2


ii. Issue the Set Features command with the I/O Command Set Profile Feature Identifier (FID
19h) specifying the index of the I/O Command Set Combination (refer to Figure 328) to be
enabled;


and


b. For each I/O Command Set that is enabled (Note: the NVM Command Set is enabled if the

CC.CSS field is set to 000b):


i. Issue the Identify command specifying the I/O Command Set specific Active Namespace
ID list (CNS 07h) with the appropriate Command Set Identifier (CSI) value of that I/O
Command Set; and
ii. For each NSID that is returned:


1. If the enabled I/O Command Set is the NVM Command Set or an I/O Command Set

based on the NVM Command Set (e.g., the Zoned Namespace Command Set) issue
the Identify command specifying the Identify Namespace data structure (CNS 00h);
and
2. Issue the Identify command specifying each of the following data structures (refer to

Figure 311: the I/O Command Set specific Identify Namespace data structure, the I/O
Command Set specific Identify Controller data structure, and the I/O Command Set
independent Identify Namespace data structure;


9. The host should determine:


a. the maximum I/O Queue size using CAP.MQES; and
b. the number of I/O Submission Queues and I/O Completion Queues supported using the

response from the Set Features command with the Number of Queues feature identifier;


10. The host should use the Connect command (refer to section 6.3) to create I/O Submission and

Completion Queue pairs; and
11. To enable asynchronous notification of optional events, the host should issue a Set Features

command specifying the events to enable. The host may submit one or more Asynchronous Event
Request commands to be notified of asynchronous events as described by section 5.1.2. This step
may be done at any point after the controller signals that the controller is ready (i.e., CSTS.RDY is
set to ‘1’).


The association may be removed if step 5 (i.e., setting CC.EN to ‘1’) is not completed within 2 minutes after
establishing the association.


**Discovery Controller Initialization**


The initialization process for Discovery controllers is described in Figure 83.


104


NVM Express [®] Base Specification, Revision 2.2


**Figure 83: Discovery Controller Initialization process flow**








|Discovery Controller receives<br>1<br>Connect Command from<br>Host|Col2|
|---|---|
|||







































After the Connect command completes with a status of Successful Completion, the host performs the
following steps:


1. NVMe authentication is performed if required (refer to section 8.3.4.2);
2. The host determines the controller’s capabilities by reading the Controller Capabilities property;
3. The host configures the controller’s settings by writing the Controller Configuration property,

including setting CC.EN to ‘1’ to enable command processing;
4. The host waits for the controller to indicate that the controller is ready to process commands. The

controller is ready to process commands when CSTS.RDY is set to ‘1’ in the Controller Status
property; and
5. The host determines the features and capabilities of the controller by issuing an Identify command,

specifying each applicable Controller data structure.


After initializing the Discovery controller, the host reads the Discovery log page. Refer to section 5.1.12.3.1.


**Controller Ready Modes During Initialization**


There are two controller ready modes:

  - **Controller Ready With Media:** By the time the controller becomes ready (i.e., by the time that
CSTS.RDY transitions from ‘0’ to ‘1’) after the controller is enabled (i.e., CC.EN transitions from ‘0’
to ‘1’), then:


a) the controller shall be able to process all commands without error as described in section

3.5.4.1; and


105


NVM Express [®] Base Specification, Revision 2.2


b) all namespaces attached to the controller and all media required to process Admin

commands shall be ready (i.e., commands are not permitted to be aborted with a status
code of Namespace Not Ready with the Do Not Retry bit cleared to ‘0’ or Admin Command
Media Not Ready with the Do Not Retry bit cleared to ‘0’).

  - **Controller Ready Independent of Media:** After the controller is enabled, all namespaces attached
to the controller and media required to process Admin commands may or may not become ready
by the time the controller becomes ready. Any Admin command or I/O command that specifies one
or more namespaces attached to the controller is permitted to be aborted with a status code of
Namespace Not Ready with the Do Not Retry bit cleared to ‘0’ until CRTO.CRWMT amount of time
after the controller is enabled.


Admin commands that require access to the media are permitted to be aborted with a status code
of Admin Command Media Not Ready with the Do Not Retry bit cleared to ‘0’ until CRTO.CRWMT
amount of time after the controller is enabled. Refer to Figure 84 for a list of Admin commands that
are permitted to be aborted with a status code of Admin Command Media Not Ready.


The controller shall be able to process without error as described in section 3.5.4.1:


a) all Admin commands not listed in Figure 84 by the time the controller is ready;
b) all Admin commands listed in Figure 84 no later than CRTO.CRWMT amount of time after

the controller is enabled; and
c) all I/O commands no later than CRTO.CRWMT amount of time after the controller is

enabled.


**Figure 84: Admin Commands Permitted to Return a Status Code of Admin Command Media Not**

**Ready**

|Admin Command|Additional Restrictions|
|---|---|
|Capacity Management||
|Device Self-test|If the Device Self-Test would result in testing one or more namespaces, then returning<br>a status code of Admin Command Media Not Ready is permitted. If the Device Self-<br>Test would not result in testing any namespaces, then returning a status code of Admin<br>Command Media Not Ready is not permitted.|
|Firmware Commit||
|Firmware Image Download||
|Get LBA Status||
|Get Log Page|Get Log Page is only permitted to return a status code of Admin Command Media Not<br>Ready for the following log pages:<br>• <br>Device Self-test<br>• <br>Firmware Slot Information<br>• <br>Telemetry Controller-Initiated<br>• <br>Telemetry Host-Initiated<br>• <br>Predictable Latency Per NVM Set<br>• <br>Predictable Latency Event Aggregate<br>• <br>Persistent Event Log<br>• <br>LBA Status Information<br>• <br>Endurance Group Event Aggregate<br>• <br>Media Unit Status<br>• <br>Supported Capacity Configuration List<br>• <br>Boot Partition<br>• <br>Reservation Notification<br>• <br>Rotational Media Information<br>• <br>Vendor Specific|
|Namespace Attachment||
|Namespace Management||
|Format NVM||
|Sanitize||
|Security Receive1||



106


NVM Express [®] Base Specification, Revision 2.2


**Figure 84: Admin Commands Permitted to Return a Status Code of Admin Command Media Not**

**Ready**

|Admin Command|Additional Restrictions|
|---|---|
|Security Send1||
|Vendor Specific||
|Notes:<br>1.<br>A host may require discovery operations performed via Security Send/Receive (e.g., TCG Level 0 Discovery) to<br>be processed prior to media being ready. Therefore, it is recommended that controllers not return Admin<br>Command Media Not Ready for such discovery operations.|Notes:<br>1.<br>A host may require discovery operations performed via Security Send/Receive (e.g., TCG Level 0 Discovery) to<br>be processed prior to media being ready. Therefore, it is recommended that controllers not return Admin<br>Command Media Not Ready for such discovery operations.|



The Controller Ready Modes Supported (CAP.CRMS) field (refer to Figure 36) indicates which controller
ready modes are supported. The CAP.CRMS field consists of two bits:

  - the Controller Ready With Media Support (CAP.CRMS.CRWMS) bit; and

  - the Controller Ready Independent of Media Support (CAP.CRMS.CRIMS) bit.


Controllers shall set the CAP.CRMS.CRWMS bit to ‘1’ (i.e., set the CAP.CRMS field to 01b or 11b). The
CAP.CRMS.CRWMS bit was not defined prior to NVM Express Base Specification, Revision 2.0.
Controllers compliant with revisions earlier than NVM Express Base Specification, Revision 2.0 may clear
the CAP.CRMS field to 00b.


The Controller Ready Independent of Media Enable (CC.CRIME) bit (refer to Figure 41) controls the
controller ready mode based on the value of the CAP.CRMS field as follows:


a) If the CAP.CRMS field is cleared to 00b, the controller ready mode is not able to be selected. In

this case, the read-only CC.CRIME bit shall be cleared to ‘0’ and should be ignored by host
software;
b) If the CAP.CRMS field is set to 01b (i.e., the CAP.CRMS.CRIMS bit is cleared to ‘0’ and the

CAP.CRMS.CRWMS bit is set to ‘1’), then the controller is in Controller Ready With Media mode
and the read-only CC.CRIME bit shall be cleared to ‘0’; and
c) If the CAP.CRMS field is set to 11b, then both controller ready modes are supported, and the host

may select the controller ready mode by modifying the value of the CC.CRIME bit. In this situation,
the host should set the controller ready mode by writing to the CC.CRIME bit before the controller
is enabled (e.g., as part of the initialization sequence of actions described in section 3.5).


**Controller Ready Timeouts During Initialization**


The CAP.CRMS field was not defined prior to NVM Express Base Specification, Revision 2.0. Controllers
compliant with revisions earlier than NVM Express Base Specification, Revision 2.0 may clear the
CAP.CRMS field to 00b. This section is applicable to controllers that clear the CAP.CRMS field to 00b and
controllers that set CAP.CRMS to a non-zero value.


There are three controller ready timeout fields:


1. CAP.TO (refer to Figure 36);
2. CRTO.CRWMT (refer to Figure 57); and
3. CRTO.CRIMT (refer to Figure 57).


The details regarding these timeouts during controller initialization are as follows:


a) The CAP.TO field shall be set as described in Figure 36;
b) If the CAP.CRMS field is cleared to 00b’, then the worst-case time the host should wait after the

controller is enabled (i.e., CC.EN transitions from ‘0’ to ‘1’) for the controller to become ready
(CSTS.RDY transitions from ‘0’ to ‘1’) is indicated by CAP.TO;
c) If the controller is in Controller Ready With Media mode (i.e., the CC.CRIME bit is cleared to ‘0’),

then:


i. the Controller Ready Independent of Media Timeout (CRTO.CRIMT) field is not applicable;
and


107


NVM Express [®] Base Specification, Revision 2.2


ii. the Controller Ready With Media Timeout (CRTO.CRWMT) indicates the worst-case time
the host should wait after the controller is enabled for:


1. the controller to become ready and be able to process all commands without error

as described in section 3.5.4.1; and
2. all attached namespaces and media required to process Admin commands to

become ready;


and


d) If the controller is in Controller Ready Independent of Media mode (i.e., the CC.CRIME bit is set to

‘1’), then


i. the Controller Ready With Media Timeout (CRTO.CRWMT) field indicates the worst-case
time that host software should wait for all attached namespaces and media required to
process Admin commands to become ready after the controller is enabled; and
ii. the Controller Ready Independent of Media Timeout (CRTO.CRIMT) field indicates the
worst-case time the host should wait after the controller is enabled for the controller to
become ready and be able to process:


1. all commands that do not access attached namespaces; and
2. Admin commands that do not require access to media,


without error as described in section 3.5.4.1.


Changes to the value of the CC.CRIME bit shall have no effect on the values of the CRTO.CRWMT and
CRTO.CRIMT fields. Changes to the value of the CC.CRIME bit may have an effect on the value of the
CAP.TO field (refer to Figure 36).


**Handling Errors During Initialization**


If the CAP.CRMS field is non-zero and the controller has been enabled by transitioning CC.EN from ‘0’ to
‘1’ and the controller encounters a failure that prevents:


a) at least one:

      - command that does not access attached namespaces; or

      - Admin command that does not require access to media (refer to Figure 84),


from being able to be processed without error by the amount of time indicated by the:

      - Controller Ready Independent of Media Timeout (CRTO.CRIMT) field since the controller
was enabled if the controller is in Controller Ready Independent of Media mode (i.e., the
CC.CRIME bit is set to ‘1’); or

      - Controller Ready With Media Timeout (CRTO.CRWMT) field since the controller was
enabled if the controller is in Controller Ready With Media mode (i.e., the CC.CRIME bit is
cleared to ‘0’);


b) at least one namespace attached to the controller from becoming ready by the amount of time

indicated by the Controller Ready With Media Timeout (CRTO.CRWMT) field since the controller
was enabled; or
c) media required by at least one Admin command from becoming ready by the amount of time

indicated by the Controller Ready With Media Timeout (CRTO.CRWMT) field since the controller
was enabled,


then:


a) if the controller has not become ready, then the controller shall become ready (i.e., set CSTS.RDY

to ‘1’) no later than CRTO.CRWMT amount of time after the controller was enabled; and
b) if the Persistent Event log page is supported, then the controller shall record an NVM Subsystem

Hardware Error Event with the NVM Subsystem Hardware Error Event code set to a value of
Controller Ready Timeout Exceeded in the Persistent Event log page (refer to Figure 237).


108


NVM Express [®] Base Specification, Revision 2.2


**3.6** **Shutdown Processing**


This section describes the recommended procedure for shutdown processing prior to a power-off condition.


There are two shutdown processing mechanisms, controller shutdown (refer to sections 3.6.1 and 3.6.2)
and NVM Subsystem Shutdown (refer to section 3.6.3). The CSTS.ST bit indicates the shutdown
mechanism that is in progress, if any (refer to Figure 42). A host requests a controller shutdown by modifying
the CC.SHN field (refer to Figure 41). A host requests an NVM Subsystem Shutdown by modifying the
NSSD property (refer to section 3.1.4.20) or by issuing an NVMe-MI Shutdown command to a Management
Endpoint (refer to the NVM Express Management Interface Specification).


At most one shutdown processing mechanism is able to be in progress for a controller at any time. If an
NVM Subsystem Shutdown is requested while a controller shutdown is in progress, then the NVM
Subsystem Shutdown overrides the controller shutdown. The progress and completion of shutdown
processing is indicated by the CSTS.SHST field (refer to Figure 42).


NVM Subsystem Shutdown should not be supported by any NVM subsystem that does not support more
than one controller, without counting virtual controllers (e.g., NVM Subsystem Shutdown should not be
supported by an NVM subsystem that supports one primary controller and multiple secondary controllers)
(refer to section 8.2.6).


Figure 85 describes the interactions of the shutdown processing state indicated by the CSTS.SHST field
with the state of the controller indicated by the CC.EN bit (refer to Figure 41) and by the CSTS.RDY bit
(refer to Figure 42). The four possible media states in Figure 85 are: shutdown, shutdown in progress,
usable, and initialization in progress.


**Figure 85: Shutdown Processing Interactions**

























|CC.EN|CSTS.RDY|CSTS.SHST|Controller able to<br>process Admin and I/O<br>commands4|Media state|Controller ready to<br>be powered off|
|---|---|---|---|---|---|
|0|0|00b|no|any|implementation<br>specific1|
|0|0|01b|no3|shutdown in<br>progress|no|
|0|0|10b|no|shutdown|yes|
|1|1|00b|yes|initialization in<br>progress or<br>usable2|no|
|1|1|01b|no3|shutdown in<br>progress|no|
|1|1|10b|no|shutdown|yes|
|Notes:<br>1.<br>In some cases (e.g., following initial application of power, or following a Controller Level Reset that occurred<br>while shutdown processing was reported as complete), the controller is permitted to initialize the media and<br>cease being ready to be powered off as a consequence.<br>2.<br>If the CC.CRIME bit is cleared to ‘0’, then the media is usable. If the CC.CRIME bit is set to ‘1’, then either<br>media initialization is in progress or the media is usable (refer to Figure 41).<br>3.<br>While shutdown processing is in progress, the controller may abort any command with a status code of<br>Commands Aborted due to Power Loss Notification.<br>4.<br>I/O commands are only able to be processed by a controller that supports I/O commands. Fabrics commands<br>are always able to be processed by a controller that supports Fabrics commands.|Notes:<br>1.<br>In some cases (e.g., following initial application of power, or following a Controller Level Reset that occurred<br>while shutdown processing was reported as complete), the controller is permitted to initialize the media and<br>cease being ready to be powered off as a consequence.<br>2.<br>If the CC.CRIME bit is cleared to ‘0’, then the media is usable. If the CC.CRIME bit is set to ‘1’, then either<br>media initialization is in progress or the media is usable (refer to Figure 41).<br>3.<br>While shutdown processing is in progress, the controller may abort any command with a status code of<br>Commands Aborted due to Power Loss Notification.<br>4.<br>I/O commands are only able to be processed by a controller that supports I/O commands. Fabrics commands<br>are always able to be processed by a controller that supports Fabrics commands.|Notes:<br>1.<br>In some cases (e.g., following initial application of power, or following a Controller Level Reset that occurred<br>while shutdown processing was reported as complete), the controller is permitted to initialize the media and<br>cease being ready to be powered off as a consequence.<br>2.<br>If the CC.CRIME bit is cleared to ‘0’, then the media is usable. If the CC.CRIME bit is set to ‘1’, then either<br>media initialization is in progress or the media is usable (refer to Figure 41).<br>3.<br>While shutdown processing is in progress, the controller may abort any command with a status code of<br>Commands Aborted due to Power Loss Notification.<br>4.<br>I/O commands are only able to be processed by a controller that supports I/O commands. Fabrics commands<br>are always able to be processed by a controller that supports Fabrics commands.|Notes:<br>1.<br>In some cases (e.g., following initial application of power, or following a Controller Level Reset that occurred<br>while shutdown processing was reported as complete), the controller is permitted to initialize the media and<br>cease being ready to be powered off as a consequence.<br>2.<br>If the CC.CRIME bit is cleared to ‘0’, then the media is usable. If the CC.CRIME bit is set to ‘1’, then either<br>media initialization is in progress or the media is usable (refer to Figure 41).<br>3.<br>While shutdown processing is in progress, the controller may abort any command with a status code of<br>Commands Aborted due to Power Loss Notification.<br>4.<br>I/O commands are only able to be processed by a controller that supports I/O commands. Fabrics commands<br>are always able to be processed by a controller that supports Fabrics commands.|Notes:<br>1.<br>In some cases (e.g., following initial application of power, or following a Controller Level Reset that occurred<br>while shutdown processing was reported as complete), the controller is permitted to initialize the media and<br>cease being ready to be powered off as a consequence.<br>2.<br>If the CC.CRIME bit is cleared to ‘0’, then the media is usable. If the CC.CRIME bit is set to ‘1’, then either<br>media initialization is in progress or the media is usable (refer to Figure 41).<br>3.<br>While shutdown processing is in progress, the controller may abort any command with a status code of<br>Commands Aborted due to Power Loss Notification.<br>4.<br>I/O commands are only able to be processed by a controller that supports I/O commands. Fabrics commands<br>are always able to be processed by a controller that supports Fabrics commands.|Notes:<br>1.<br>In some cases (e.g., following initial application of power, or following a Controller Level Reset that occurred<br>while shutdown processing was reported as complete), the controller is permitted to initialize the media and<br>cease being ready to be powered off as a consequence.<br>2.<br>If the CC.CRIME bit is cleared to ‘0’, then the media is usable. If the CC.CRIME bit is set to ‘1’, then either<br>media initialization is in progress or the media is usable (refer to Figure 41).<br>3.<br>While shutdown processing is in progress, the controller may abort any command with a status code of<br>Commands Aborted due to Power Loss Notification.<br>4.<br>I/O commands are only able to be processed by a controller that supports I/O commands. Fabrics commands<br>are always able to be processed by a controller that supports Fabrics commands.|


Figure 85 does not include transition conditions for a controller that is becoming ready or is undergoing
reset. During these transitions, the CC.EN bit and the CSTS.RDY bit have different values (refer to Figure
41 and Figure 42). The media may or may not be usable during these transitions.


109


NVM Express [®] Base Specification, Revision 2.2


Figure 85 does not include the NVMe-MI effects of processing an Admin command that requires access to
the media (refer to Figure 84) and specifies the Ignore Shutdown bit set to ‘1’ is processed by the controller
via the out-of-band mechanism (refer to the NVM Express Management Interface Specification). Processing
of such a command causes the media to become usable, after which the media may or may not be returned
to its previous condition.


**Memory-based Controller Shutdown (PCIe)**


It is recommended that the host perform an orderly shutdown of the controller by following the procedure
in this section when a power-off or shutdown condition is imminent.


The host should perform the following actions in sequence for a normal controller shutdown:


1. If the controller is enabled (i.e., CC.EN (refer to Figure 41) is set to ‘1’):


a. Stop submitting any new I/O commands to the controller and allow any outstanding

commands to complete;
b. If the controller implements I/O queues, then the host should delete all I/O Submission

Queues, using the Delete I/O Submission Queue command (refer to section 5.2.4). A result
of the successful completion of the Delete I/O Submission Queue command is that any
remaining commands outstanding are aborted;
c. If the controller implements I/O queues, then the host should delete all I/O Completion

Queues, using the Delete I/O Completion Queue command (refer to section 5.2.3);


and


2. The host should set the Shutdown Notification (CC.SHN) field (refer to Figure 41) to 01b to indicate

a normal controller shutdown operation. The controller indicates when shutdown processing is
completed by updating the Shutdown Status (CSTS.SHST) field to 10b and the Shutdown Type
(CSTS.ST) field (refer to Figure 42) is cleared to ‘0’.


The host should perform the following actions in sequence for an abrupt shutdown:


1. If the controller is enabled (i.e., CC.EN is set to ‘1’), then stop submitting any new I/O commands

to the controller; and
2. The host should set the Shutdown Notification (CC.SHN) field (refer to Figure 41) to 10b to indicate

an abrupt shutdown operation. The controller indicates when shutdown processing is completed
by updating the Shutdown Status (CSTS.SHST) field (refer to Figure 42) to 10b and CSTS.ST
(refer to Figure 42) is cleared to ‘0’.


For entry to the D3 power state (refer to the PCI Express Base Specification), the shutdown steps outlined
for a normal controller shutdown should be followed.


It is recommended that the host wait a minimum of the RTD3 Entry Latency reported in the Identify
Controller data structure (refer to Figure 313) for the shutdown operations to complete; if the value reported
in RTD3 Entry Latency is 0h, then the host should wait for a minimum of one second. While shutdown
processing is in progress on a controller, it is not recommended to disable that controller via the CC.EN bit.
This causes a Controller Reset which may impact the time required to complete shutdown processing.
While shutdown processing is in progress on a controller, that controller may abort any command with a
status code of Commands Aborted due to Power Loss Notification.


The controller is ready to be powered off (e.g., the media is in the shutdown state (refer to Figure 85)) when
the CSTS.ST bit is cleared to ‘0’, and the CSTS.SHST field indicates that controller shutdown processing
is complete (i.e., the CSTS.SHST field is set to 10b), regardless of the value of the CC.EN bit. The controller
remains ready to be powered off (e.g., the media remains in the shutdown state) until:


A. the controller is enabled (i.e., the CC.EN bit transitions from ‘0’ to ‘1’);
B. the controller is reset by a Controller Level Reset; or
C. an Admin command that requires access to the media (refer to Figure 84) and specifies the Ignore

Shutdown bit set to ‘1’ is processed by the controller via the out-of-band mechanism (refer to the
NVM Express Management Interface Specification).


110


NVM Express [®] Base Specification, Revision 2.2


If a Controller Level Reset occurs while controller shutdown processing is reported as complete (i.e., the
CSTS.ST bit is cleared to ‘0’ and the CSTS.SHST field is set to 10b), then the controller may remain ready
to be powered off (e.g., the media remains in the shutdown state) or the controller may cease being ready
to be powered off (e.g., because the controller is preparing the media for use (refer to section 3.7.2)).


If the power scope for the controller includes multiple controllers (e.g., the CAP.CPS field is set to 10b or is
set to 11b), and any controller included in that power scope is not ready to be powered off, then the portion
of the NVM subsystem included in that power scope is not ready to be powered off.


To start executing commands on the controller after that controller reports controller shutdown processing
complete (i.e., the CSTS.ST bit is cleared to ‘0’ and the CSTS.SHST field is set to 10b) utilizing the CC.EN
bit:

  - if the CC.EN bit is set to ‘1’, then a Controller Level Reset is required to clear the CC.EN bit to ‘0’
on that controller and the CC.EN bit is subsequently required to be set to ‘1’ as part of the
initialization sequence (refer to section 3.5); and

  - if the CC.EN bit is cleared to ‘0’, then:


`o` a Controller Level Reset is required and the CC.EN bit is subsequently required to be set
to ‘1’ as part of the initialization sequence (refer to section 3.5); or

`o` the CC.EN bit is required to be set to ‘1’ and the CC.SHN field is required to be cleared to
00b with the same write to the CC property (refer to Figure 41). The controller clears the
CSTS.SHST field to 00b in response to that write.


The initialization sequence (refer to section 3.5) should then be executed on that controller.


It is an implementation choice whether the host aborts all outstanding commands to the Admin Queue prior
to the controller shutdown. The only commands that should be outstanding to the Admin Queue when the
controller reports shutdown processing complete are Asynchronous Event Request commands.


If the host is no longer able to communicate with the controller before that host receives either:

  - completions for all outstanding commands submitted to that controller (refer to section 3.4.5); or

  - a CSTS.SHST field value that indicates that the controller shutdown is complete,


then it is strongly recommended that the host take the steps described in section 9.6 to avoid possible data
corruption caused by interaction between outstanding commands and subsequent commands submitted
by that host to another controller.


**Message-based Controller Shutdown (Fabrics)**


To initiate a shutdown of a controller, the host should use the Property Set command (refer to section 6.6)
to set the Shutdown Notification (CC.SHN) field to:

   - 01b to initiate a normal shutdown operation; or

   - 10b to initiate an abrupt shutdown operation.


After the host initiates a controller shutdown, the host may either disconnect at the NVMe Transport level
or the host may choose to poll CSTS.SHST to determine when the controller shutdown is complete (i.e.,
the controller should not initiate a disconnect at the NVMe Transport level). It is an implementation choice
whether the host aborts all outstanding commands prior to initiating the shutdown.


If the host is no longer able to communicate with the controller before that host receives either:

  - completions for all outstanding commands submitted to that controller (refer to section 3.4.5); or

  - a CSTS.SHST field value that indicates that the controller shutdown is complete,


then it is strongly recommended that the host take the steps described in section 9.6 to avoid possible data
corruption caused by interaction between outstanding commands and subsequent commands submitted
by that host to another controller.


The CC.EN field is not used to shutdown the controller (i.e., it is used for Controller Reset).


From the time a controller shutdown is initiated until:


111


NVM Express [®] Base Specification, Revision 2.2


  - a Controller Level Reset occurs; or

  - the controller, if dynamic, is removed from the NVM subsystem,


the controller shall:

  - process only Fabrics commands (refer to Figure 541); and

  - disable the Keep Alive timer, if supported.


After the CC.EN bit transitions to ‘0’ (i.e., due to Controller Level Reset), the association between the host
and controller shall be preserved for at least 2 minutes. After this time, the association may be removed if
the controller has not been re-enabled.


To start executing commands on the controller after that controller reports controller shutdown processing
complete (i.e., the CSTS.ST bit is cleared to ‘0’ and the CSTS.SHST field is set to 10b) utilizing the CC.EN
bit:

  - if the CC.EN bit is set to ‘1’, then a Controller Level Reset is required to clear the CC.EN bit to ‘0’
on that controller and the CC.EN bit is subsequently required to be set to ‘1’ as part of the
initialization sequence (refer to section 3.5); and

  - if the CC.EN bit is cleared to ‘0’, then:


`o` a Controller Level Reset is required and the CC.EN bit is subsequently required to be set
to ‘1’ as part of the initialization sequence (refer to section 3.5); or

`o` the CC.EN bit is required to be set to ‘1’ and the CC.SHN field is required to be cleared to
00b with a single Property Set command (refer to section 6.6) that changes the CC property
(refer to Figure 41). The controller clears the CSTS.SHST field to 00b in response to that
write.


The initialization sequence (refer to section 3.5) should then be executed on that controller.


**NVM Subsystem Shutdown**


An NVM Subsystem Shutdown initiates a shutdown of all controllers in a domain or NVM subsystem from
a single controller.


Interactions between NVM Subsystem Shutdown and Power Loss Signaling processing are described in
section 8.2.5.


A controller indicates support for the NVM Subsystem Shutdown Feature by setting the CAP.NSSS bit to
‘1’ (refer to Figure 36).


The NVM Subsystem Shutdown Feature defined in this revision of the NVM Express Base Specification
includes some functionality that differs from the functionality of the NVM Subsystem Shutdown Feature
defined in revision 2.0 of the NVM Express Base Specification. A controller indicates support for these
functionality differences by setting the NVM Subsystem Shutdown Enhancements Supported
(CAP.NSSES) bit to ‘1’ (refer to Figure 36).


If a controller sets the CAP.NSSES bit to ‘1’, then while an NVM Subsystem Shutdown is reported as in
progress or is reported as complete (i.e., while the CSTS.ST bit is set to ‘1’ and the CSTS.SHST field is set
to 01b or is set to 10b):


a. a Controller Reset initiates a Controller Level Reset (CLR) (refer to section 3.7.2); and
b. the values of both the CSTS.ST bit and the CSTS.SHST field (refer to Figure 40) are not changed

by a CLR initiated by any method other than an NVM Subsystem Reset.


If a controller clears the CAP.NSSES bit to ‘0’, then, as defined in revision 2.0 of the NVM Express Base
Specification:


a. while an NVM Subsystem Shutdown is reported as in progress or is reported as complete, a

Controller Reset does not initiate a CLR (i.e., Controller Reset is disabled); and
b. while an NVM Subsystem Shutdown is reported as complete, any CLR initiated by any transport
specific reset type may clear the value of the CSTS.ST bit to ‘0’ and may clear the value of the
CSTS.SHST field to 00b.


112


NVM Express [®] Base Specification, Revision 2.2


A host is able to support NVM Subsystem Shutdown functionality both on controllers that set the
CAP.NSSES bit to ‘1’ and on controllers that clear the CAP.NSSES bit to ‘0’ by ensuring that any NVM
Subsystem Shutdown is followed by an NVM Subsystem Reset regardless of the value of the CSTS.ST bit
and the value of the CSTS.SHST field.


**NVM Subsystem Shutdown in a Single Domain NVM Subsystem**


A normal shutdown on all controllers within the NVM subsystem (i.e., normal NVM Subsystem Shutdown)
is initiated by:

   - a host writing the value 4E726D6Ch ("Nrml") to NSSD.NSSC when CAP.CPS is set to 11b; or

   - issuing an NVMe-MI Shutdown command to a Management Endpoint (refer to the NVM Express
Management Interface Specification) specifying a normal shutdown.


For each controller in the NVM subsystem for this normal NVM Subsystem Shutdown, if:

   - CSTS.SHST is set to 00b; and

   - An outstanding Asynchronous Event Request command exists,


then the controller shall issue a Normal NVM Subsystem Shutdown event prior to shutting down the
controller.


An abrupt shutdown on all controllers within the NVM subsystem (i.e., abrupt NVM Subsystem Shutdown)
is initiated by:

   - a host writing the value 41627074h ("Abpt") to NSSD.NSSC when CAP.CPS is set to 11b; or

   - issuing an NVMe-MI Shutdown command to a Management Endpoint (refer to the NVM Express
Management Interface Specification) specifying an abrupt shutdown.


While NVM Subsystem Shutdown processing is in progress, any controller in the NVM subsystem may
abort any command with a status code of Commands Aborted due to Power Loss Notification.


It is recommended that the host wait a minimum of the NVM Subsystem Shutdown Latency reported in the
Identify Controller data structure (refer to Figure 313) for NVM Subsystem Shutdown processing to
complete; if the reported NVM Subsystem Shutdown Latency value is 0h, then the host should wait for a
minimum of 30 seconds. While an NVM Subsystem Shutdown is reported as in progress, it is not
recommended to reset the NVM subsystem via an NVM Subsystem Reset or a power cycle (which causes
an NVM Subsystem Reset). This aborts the NVM Subsystem Shutdown which may impact the subsequent
time required for the NVM subsystem to become ready to perform I/O (e.g., after power is reapplied
following a power cycle).


For either a normal or an abrupt NVM Subsystem Shutdown, the NVM subsystem is ready to be powered
off (e.g., the media is in the shutdown state (refer to Figure 85)) when the CSTS.ST bit is set to ‘1’ and the
CSTS.SHST field indicates that shutdown processing is complete (i.e., the CSTS.SHST field is set to 10b)
on any controller in the NVM subsystem. The NVM subsystem shall not set the CSTS.SHST field to 10b on
any controller in the NVM subsystem until the entire NVM subsystem is ready to be powered off. The NVM
Subsystem shall indicate that NVM Subsystem Shutdown processing is complete by setting the
CSTS.SHST field to 10b on all controllers in the NVM subsystem. The NVM subsystem remains ready to
be powered off (e.g., the media remains in the shutdown state) until:


A. an NVM Subsystem Reset; or
B. an Admin command that requires access to the media (refer to Figure 84) and specifies the Ignore

Shutdown bit set to ‘1’ is processed by any controller via the out-of-band mechanism (refer to the
NVM Express Management Interface Specification).


If a normal or an abrupt NVM Subsystem Shutdown is reported as in progress or is reported as complete
within the NVM subsystem (i.e., the CSTS.ST bit is set to ‘1’ and the CSTS.SHST field is set to either 01b
or 10b on all controllers in the NVM subsystem, indicating that an NVM Subsystem Reset has not occurred
since initiation of that NVM Subsystem Shutdown), then:

  - an NVM Subsystem Reset:


113


NVM Express [®] Base Specification, Revision 2.2


`o` shall abort any in progress NVM Subsystem Shutdown;

`o` clears the CSTS.SHST field to 00b in all controllers in the NVM subsystem; and

`o` clears the CSTS.ST bit to ‘0’ in all controllers in the NVM subsystem;


and

  - a Controller Level Reset of any controller in the NVM subsystem that is initiated by any other
method (refer to section 3.7.2):


`o` shall not abort any in progress NVM Subsystem Shutdown;

`o` does not change the values of the CSTS.ST bit and the CSTS.SHST field, as described in
Figure 42; and

`o` shall not cause that NVM subsystem to cease being ready to be powered off (e.g., shall
not transition the media out of the shutdown state) if that NVM Subsystem was ready to be
powered off when that Controller Level Reset was initiated.


To start executing commands on the controller after that controller reports NVM Subsystem Shutdown
processing complete (i.e., the CSTS.ST bit is set to ‘1’ and the CSTS.SHST field is set to 10b):

  - regardless of the value of the CC.EN bit, an NVM Subsystem Reset is required; and

  - the CC.EN bit is subsequently required to be set to ‘1’ as part of the initialization sequence (refer
to section 3.5).


The initialization sequence (refer to section 3.5) should then be executed on that controller.


**Domain Shutdown in a Multiple Domain NVM Subsystem**


A normal NVM Subsystem Shutdown on this controller and all controllers within the associated domain is
initiated by:

   - a host writing the value 4E726D6Ch ("Nrml") to NSSD.NSSC when CAP.CPS is set to 10b; or

   - issuing an NVMe-MI Shutdown command to a Management Endpoint (refer to the NVM Express
Management Interface Specification) specifying a normal shutdown.


For each controller in the domain for this normal NVM subsystem shutdown, if:

   - CSTS.SHST is cleared to 00b; and

   - An outstanding Asynchronous Event Request command exists,


then the controller shall issue a Normal NVM Subsystem Shutdown event prior to shutting down the
controller.


An abrupt NVM Subsystem Shutdown to this controller and all controllers within the associated domain is
initiated by:

   - a host writing the value 41627074h ("Abpt") to NSSD.NSSC when CAP.CPS is set to 10b; or

   - issuing an NVMe-MI Shutdown command to a Management Endpoint (refer to the NVM Express
Management Interface Specification) specifying an abrupt shutdown.


While NVM Subsystem Shutdown processing is in progress, any controller in the domain may abort any
command with a status code of Commands Aborted due to Power Loss Notification.


It is recommended that the host wait a minimum of the NVM Subsystem Shutdown Latency reported in the
Identify Controller data structure (refer to Figure 313) for NVM Subsystem Shutdown processing on a
domain to complete; if the reported NVM Subsystem Shutdown Latency value is 0h, then the host should
wait for a minimum of 30 seconds. While an NVM Subsystem Shutdown is reported as in progress, it is not
recommended to reset the domain via either an NVM Subsystem Reset on the domain or power cycling the
domain (which causes an NVM Subsystem Reset on the domain). This aborts the NVM Subsystem
Shutdown which may impact the subsequent time required for the domain to become ready to perform I/O
(e.g., after power is reapplied following a power cycle).


For either a normal or an abrupt NVM Subsystem Shutdown on the domain, the domain is ready to be
powered off (e.g., the media is in the shutdown state (refer to Figure 85)) when the CSTS.ST bit is set to


114


NVM Express [®] Base Specification, Revision 2.2


‘1’ and the CSTS.SHST field indicates that shutdown processing is complete (i.e., the CSTS.SHST field is
set to 10b) on any controller in the domain. The NVM subsystem shall not set the CSTS.SHST field to 10b
on any controller in the domain until the entire domain is ready to be powered off. The NVM Subsystem
shall indicate that NVM Subsystem Shutdown processing is complete by setting the CSTS.SHST field to
10b on all controllers in the domain. The domain remains ready to be powered off (e.g., the media remains
in the shutdown state) until:


A. an NVM Subsystem Reset occurs on that domain; or
B. an Admin command that requires access to the media (refer to Figure 84) and specifies the Ignore

Shutdown bit set to ‘1’ is processed by any controller in the domain via the out-of-band mechanism
(refer to the NVM Express Management Interface Specification).


If a normal or an abrupt NVM Subsystem Shutdown is reported as in progress or is reported as complete
within a domain (i.e., the CSTS.ST bit is set to ‘1’ and the CSTS.SHST field is set to either 01b or 10b on
all controllers in the domain, indicating that an NVM Subsystem Reset on the domain has not occurred
since initiation of that NVM Subsystem Shutdown), then:

  - an NVM Subsystem Reset on the domain:


`o` shall abort any in progress NVM Subsystem Shutdown on the domain; and

`o` clears the CSTS.SHST field to 00b in all controllers in the domain; and

`o` clears the CSTS.ST bit to ‘0’ in all controllers in the domain;


and

  - a Controller Level Reset of any controller in the domain that is initiated by any other method (refer
to section 3.7.2)


`o` shall not abort any in progress NVM Subsystem Shutdown on the domain;

`o` does not change the values of the CSTS.ST bit and the CSTS.SHST field, as described in
Figure 42; and

`o` shall not cause the domain to cease being ready to be powered off (e.g., shall not transition
the media out of the shutdown state) if the domain was ready to be powered off when that
Controller Level Reset was initiated.


To start executing commands on the controller after that controller reports NVM Subsystem Shutdown
processing complete (i.e., the CSTS.ST bit is set to ‘1’ and the CSTS.SHST field is set to 10b):

  - regardless of the value of CC.EN, an NVM Subsystem Reset on that domain is required; and

  - the CC.EN bit is subsequently required to be set to ‘1’ as part of the initialization sequence (refer
to section 3.5).


The initialization sequence (refer to section 3.5) should then be executed on that controller.


**3.7** **Resets**


**NVM Subsystem Reset**


Interactions between NVM Subsystem Reset and Power Loss Signaling processing are described in section
8.2.5.


**Single Domain NVM Subsystems**


The scope of an NVM Subsystem Reset depends on whether the NVM subsystem supports multiple
domains. In an NVM subsystem that does not support multiple domains, the scope of the NVM Subsystem
Reset is the entire NVM subsystem.


An NVM Subsystem Reset is initiated when:

  - Main power is applied to the NVM subsystem;

  - A value of 4E564D65h (“NVMe”) is written to the NSSR.NSSRC field;

  - Requested using a method defined in the NVM Express Management Interface Specification; or


115


NVM Express [®] Base Specification, Revision 2.2


  - A vendor specific event occurs.


When an NVM Subsystem Reset occurs, the entire NVM subsystem is reset. This includes the initiation of
a Controller Level Reset on all controllers that make up the NVM subsystem, disabling of the Persistent
Memory Region associated with all controllers that make up the NVM subsystem, and any transport specific
actions defined in the applicable NVMe transport specification.


The occurrence of an NVM Subsystem Reset while power is applied to the NVM subsystem is reported by
the initial value of the CSTS.NSSRO field following the NVM Subsystem Reset. This field may be used by
host software to determine if the sudden loss of communication with a controller was due to an NVM
Subsystem Reset or some other condition.


The ability for host software to initiate an NVM Subsystem Reset by writing to the NSSR.NSSRC field is an
optional capability of a controller indicated by the state of the CAP.NSSRS field. An implementation may
protect the NVM subsystem from an inadvertent NVM Subsystem Reset by not providing this capability to
one or more controllers that make up the NVM subsystem.


The occurrence of a vendor specific event that results in an NVM Subsystem Reset is intended to allow
implementations to recover from a severe NVM subsystem internal error that prevents continued normal
operation (e.g., fatal hardware or firmware error).


**Multiple Domain NVM Subsystems**


The scope of an NVM Subsystem Reset depends on whether the NVM subsystem supports multiple
domains. In an NVM subsystem that supports multiple domains, the scope of the NVM Subsystem Reset
is either the controllers that are in a domain or the entire NVM subsystem.


An NVM Subsystem Reset on a domain is initiated when:

  - Power is applied to that domain;

  - A value of 4E564D65h (i.e., “NVMe”) is written to the NSSR.NSSRC field of one of the controllers
in that domain; or

  - A vendor specific event occurs within that domain.


When an NVM Subsystem Reset occurs the entire domain is reset. This includes the initiation of a Controller
Level Reset on all controllers that are in the domain, disabling of the Persistent Memory Region associated
with all controllers that are in the domain, and any transport specific actions defined in the applicable NVMe
transport specification.


Alternatively, an NVM Subsystem Reset in an NVM subsystem that supports multiple domains may reset
the entire NVM subsystem.


The occurrence of an NVM Subsystem Reset while power is applied to the domain is reported by the initial
value of the CSTS.NSSRO field following the NVM Subsystem Reset. This field may be used by host
software to determine if the sudden loss of communication with a controller was due to an NVM Subsystem
Reset or some other condition.


The ability for host software to initiate an NVM Subsystem Reset by writing to the NSSR.NSSRC field is an
optional capability of a controller indicated by the state of the CAP.NSSRS field. An implementation may
protect the domain from an inadvertent NVM Subsystem Reset by not providing this capability to one or
more controllers that are in the domain.


**Controller Level Reset**


The following methods initiate a Controller Level Reset:

  - NVM Subsystem Reset;

  - Controller Reset (i.e., host clears the CC.EN bit from ‘1’ to ‘0’); and

  - Transport specific reset types (refer to the applicable NVMe Transport binding specification), if any.


A Controller Level Reset consists of the following actions:

  - The controller stops processing any outstanding Admin or I/O commands;


116


NVM Express [®] Base Specification, Revision 2.2


  - All I/O Submission Queues are deleted;

  - All I/O Completion Queues are deleted;

  - The controller is brought to an idle state. When this is complete, the CSTS.RDY bit is cleared to
‘0’; and

  - All NVMe controller properties defined in either section 3.1.4 or the applicable NVMe Transport
binding specification and all internal controller state are reset, with the following exceptions:


`o` for memory-based controllers:


      - the following are not reset as part of a Controller Level Reset caused by a Controller Reset:


            - Admin Queue properties (i.e., AQA, ASQ, and ACQ);

            - Persistent Memory Region properties (i.e., PMRCAP, PMRCTL, PMRSTS, PMREBS,
PMRSWTP, PMRMSCU, and PMRMSCL); and

            - The Controller Memory Buffer Memory Space Control property (CMBMSC) (refer to
the NVM Express NVMe over PCIe Transport Specification);


and


      - the following are not reset as part of a Controller Level Reset caused by a Function Level
Reset:


            - the Controller Memory Buffer Memory Space Control property (CMBMSC);


and


`o` for message-based controllers:


      - there are no exceptions.


In all Controller Level Reset cases except a Controller Reset, the controller properties defined by the
transport (e.g., the PCIe registers defined by the PCIe Base Specification) are reset as defined by the
applicable NVMe Transport binding specification (e.g., the NVM Express NVMe over PCIe Transport
Specification).


In all Controller Level Reset cases, if the media is not usable and an NVM Subsystem Shutdown that
includes the controller is neither reported as in progress nor reported as complete (i.e., the CSTS.ST bit is
cleared to ‘0’ or the CSTS.SHST field is cleared to 00b), then the controller is permitted to initialize the
media for use upon completion of the Controller Level Reset.


To continue after a Controller Level Reset, the host should:

  - update transport specific state and controller property state as appropriate;

  - set the CC.EN bit to ‘1’;

  - wait for the CSTS.RDY bit to be set to ‘1’;

  - configure the controller using Admin commands as needed;

  - create I/O Completion Queues and I/O Submission Queues as needed; and

  - proceed with normal I/O operations.


Note that all Controller Level Reset cases except a Controller Reset result in the controller immediately
losing communication with the host. In all these cases, the controller is unable to indicate any aborts or
update any completion queue entries.


If the host is no longer able to communicate with the controller before that host receives either:

  - completions for all outstanding commands submitted to that controller (refer to section 3.4.5); or

  - a CSTS.RDY bit value cleared to ‘0’,


then it is strongly recommended that the host take the steps described in section 9.6 to avoid possible data
corruption caused by interaction between outstanding commands and subsequent commands submitted
by that host to another controller.


117


NVM Express [®] Base Specification, Revision 2.2


**Queue Level Reset**


The host may reset and/or reconfigure the I/O Submission and I/O Completion Queues by resetting them.
A queue level reset is performed by deleting and then recreating the queue. In this process, the host should
wait for all pending commands to the appropriate I/O Submission Queue(s) to complete.


To perform the queue level reset on a controller using the memory-based transport model, the host submits
the Delete I/O Submission Queue or Delete I/O Completion Queue command to the Admin Queue
specifying the identifier of the queue to be deleted. After successful command completion of the queue
delete operation, the host then recreates the queue by submitting the Create I/O Submission Queue or
Create I/O Completion Queue command. As part of the creation operation, the host may modify the
attributes of the queue. Note that if a queue level reset is performed on an I/O Completion Queue, the I/O
Submission Queues that are utilizing the I/O Completion Queue should be deleted before the I/O
Completion Queue is reset and recreated after the I/O Completion Queue is recreated. The behavior of an
I/O Submission Queue without a corresponding I/O Completion Queue is undefined.


To perform the queue level reset on a controller using the message-based transport model, the host sends
a Disconnect command to the I/O Queue which is to be deleted. After successful command completion of
the Disconnect command, the host then recreates the I/O Submission Queue and I/O Completion Queue
by submitting the Connect command with a QID specified that is not 00h. As part of the Connect command,
the host may modify the attributes of the I/O queues.


The host should ensure that the appropriate I/O Submission Queue or I/O Completion Queue is idle before
deleting that queue. Submitting a queue deletion command causes any pending commands to be aborted
by the controller; this may or may not result in a completion queue entry being posted for the aborted
command(s).


**3.8** **NVM Capacity Model**


**Overview**


NVM subsystems may report capacity-related information for multiple entities within the NVM subsystem.
This capacity reporting model includes capacity reporting for the NVM subsystem, the domain (refer to
section 3.2.5), the Endurance Group (refer to section 3.2.3), the NVM Set (refer to section 3.2.2),
namespaces that contain formatted storage (refer to section 3.2.1), and the Media Unit (refer to section
1.5.54). Some, all, or none of this reporting may be supported by an NVM subsystem.


Figure 14 shows the hierarchical relationships of the entities within an NVM subsystem which are used to
manage NVM capacity.


The capacity in an NVM Set is able to be allocated to one or more namespaces, and each namespace that
contains formatted storage exists entirely in that NVM Set (refer to section 3.2.2). Not all of the capacity in
the NVM Set is required to be allocated to a namespace.


If the controller supports NVM Sets, then the capacity in an Endurance Group is able to be allocated to one
or more NVM Sets and each NVM Set exists entirely in that Endurance Group (refer to section 3.2.3). Not
all of the capacity in an Endurance Group is required to be allocated to an NVM Set.


If the controller supports Endurance Groups and does not indicate support for NVM Sets, then in all data
structures that contain an NVMSETID field, the NVMSETID field shall be cleared to 0h.


If the controller does not support Endurance Groups, then in all data structures that contain an ENDGID
field, the ENDGID field shall be cleared to 0h.


If the controller supports Endurance Groups, then the capacity in a domain is able to be allocated to one or
more Endurance Groups, and each Endurance Group exists entirely in that domain (refer to section 3.2.5).
Not all of the capacity in a domain is required to be allocated to an Endurance Group.


NVM subsystems may report the composition of Endurance Groups and NVM Sets in terms of Media Units.
Each Media Unit is allocated to exactly one Endurance Group. If NVM Sets are supported, each Media Unit
is allocated to exactly one NVM Set. Data is transferred to and from Media Units via Channels. Each Media
Unit is connected to one or more Channels. Each Channel is connected to one or more Media Units.


118


NVM Express [®] Base Specification, Revision 2.2


A host uses Capacity Management (refer to section 8.1.4) to allocate:


a) Domain capacity to Endurance Groups;
b) Endurance Group capacity to NVM Sets;
c) Media Units to Endurance Groups; and
d) Media Units to NVM Sets,


as part of creating those entities.


A host uses the Namespace Management create operation (refer to section 8.1.15) to allocate capacity to
namespaces that contain formatted storage.


**Media Unit Organization Examples**


Allocation of Media Units is used to organize the physical NVM resources in an NVM subsystem to meet
particular performance goals.


The following examples show an NVM subsystem with all resources in a single domain. The domain has
four Channels, with four Media Units attached to each Channel.


**Simple NVM Subsystem**


Figure 86 shows an example of a single domain NVM subsystem where endurance is managed across all
media units. The performance goal is maximum bandwidth, which is achieved by allowing each read or
write operation to simultaneously access all Media Units. All Media Units are in the same Endurance Group
and in the same NVM Set.


**Figure 86: Simple NVM Subsystem**











The Capacity Configuration Descriptor for this example contains one Endurance Group Configuration
Descriptor. The Endurance Group Configuration Descriptor contains one NVM Set Identifier and four
Channel Configuration Descriptors. Each Channel Configuration Descriptor contains four Media Unit
Configuration Descriptors.


119


NVM Express [®] Base Specification, Revision 2.2


**Vertically-Organized NVM Subsystem**


Figure 87 shows an example of a single domain NVM subsystem where the performance goal is isolation
among four NVM Sets at the cost of bandwidth. Endurance is managed separately for each NVM Set.
Media Units sharing a Channel are allocated to the same Endurance Group. All Media Units in an
Endurance Group are allocated to the same NVM Set. The bandwidth for any NVM Set is likely to be less
than or equal to the bandwidth of the Channel of that NVM Set.


**Figure 87: Vertically-Organized NVM Subsystem**


The Capacity Configuration Descriptor for this example contains four Endurance Group Configuration
Descriptors. Each Endurance Group Configuration Descriptor contains one NVM Set Identifier and one
Channel Configuration Descriptor. Each Channel Configuration Descriptor contains four Media Unit
Configuration Descriptors.


**Horizontally-Organized Dual NAND NVM Subsystem**


Figure 88 shows an example of a single domain NVM subsystem where the Media Units are NAND which
is capable of being operated as QLC or at a lower density. The performance goal is for maximum bandwidth
to a small NVM Set operating as SLC and to a larger NVM Set operating as QLC.


120


NVM Express [®] Base Specification, Revision 2.2


**Figure 88: Horizontally-Organized Dual NAND NVM Subsystem**









The Capacity Configuration Descriptor for this example contains two Endurance Group Configuration
Descriptors. The first Endurance Group Configuration Descriptor for this example:

   - indicates a Capacity Adjustment Factor of approximately 400;

   - contains one NVM Set Identifier; and

   - contains four Channel Configuration Descriptors. Each Channel Configuration Descriptor contains
one Media Unit Configuration Descriptor.


The second Endurance Group Configuration Descriptor for this example:

   - indicates a Capacity Adjustment Factor of 100;

   - contains one NVM Set Identifier; and

   - contains four Channel Configuration Descriptors. Each Channel Configuration Descriptor contains
three Media Unit Configuration Descriptors.


**Capacity Reporting**


For an NVM subsystem that does not support multiple domains, the capacity information reported in the
Identify Controller data structure (i.e., the TNVMCAP field and the UNVMCAP field in Figure 313) describes
the capacity for the NVM subsystem. If the MEGCAP field is non-zero, that field indicates the largest entity
(e.g., Endurance Group, NVM Set, namespace that contains formatted storage) that may be created in the
NVM subsystem.


For an NVM subsystem that supports multiple domains, the capacity information reported in the Identify
Controller data structure describes the capacity accessible by the controller processing the Identify
command. The host may use the Identify command to access the Domain List data structure (refer to
section 5.1.13.2.15) to determine the domains that are accessible by the controller and the capacity
information for each of those domains. If the Max Endurance Group Domain Capacity field is non-zero,
then the field describes the largest entity (e.g., Endurance Group, namespace that contains formatted
storage) that may be created by this controller in the domain described by that Domain Attributes Entry.


For an NVM subsystem that supports Endurance Groups (refer to section 3.2.3), the host may use the
Identify command to access the Endurance Group List data structure (refer to section 5.1.13.2.16) to
determine the Endurance Groups that are accessible by the controller. To determine the capacity


121


NVM Express [®] Base Specification, Revision 2.2


information for each Endurance Group, the host uses the Get Log Page command to access the Endurance
Group Information log page (refer to section 5.1.12.1.10).


For an NVM subsystem that supports NVM Sets (refer to section 3.2.2), the host may use the Identify
command to access the NVM Set List data structure (refer to section 5.1.13.2.4) to determine the NVM
Sets that are accessible by the controller and the capacity information for each of those NVM Sets.


For the management of Endurance Groups, NVM Sets, and namespaces that contain formatted storage,
Figure 89 describes the effects of the support of NVM Sets, Endurance Groups, and domains on which
capacity information is used for each management operation.


**Figure 89: Capacity Information Field Usage**




























|Entity being<br>created / deleted|NVM Sets<br>supported|Endurance<br>Groups<br>supported|Domains<br>supported|1<br>Capacity information used|
|---|---|---|---|---|
|Endurance Group 7|n/a|Yes|No|NVM subsystem3|
|Endurance Group 7|n/a|Yes|Yes|Domain4|
|NVM Set 7|Yes|Yes2|n/a|Endurance Group5|
|Namespace that<br>contains formatted<br>storage 8|No|No|No|NVM subsystem3|
|Namespace that<br>contains formatted<br>storage 8|No|No|Yes|Domain4|
|Namespace that<br>contains formatted<br>storage 8|No|Yes|n/a|Endurance Group5|
|Namespace that<br>contains formatted<br>storage 8|Yes|Yes2|n/a|NVM Set6|
|Notes:<br>1.<br>This information described in this column is used by the host for creating the entity (e.g., to determine if there<br>is sufficient available capacity) and this information is altered by the controller as a result of the creation or<br>deletion of the entity (e.g., unallocated capacity decreased as a result of entity creation, or unallocated capacity<br>increased as a result of entity deletion).<br>2.<br>NVM Set support requires support for Endurance Groups as described in section 3.2.2.<br>3.<br>Capacity information in the Identify Controller data structure (i.e., TNVMCAP field, UNVMCAP field, and<br>MEGCAP field (refer to Figure 313)).<br>4.<br>Capacity information in the Domain Attributes Entry (i.e., Total Domain Capacity field, Unallocated Domain<br>Capacity field, and Max Endurance Group Domain Capacity field (refer to Figure 325)).<br>5.<br>Capacity information in the Endurance Group Information log page (i.e., TEGCAP field, UEGCAP field (refer<br>to Figure 219)).<br>6.<br>Capacity information in the NVM Set Attributes Entry (i.e., Total NVM Set Capacity field, and Unallocated NVM<br>Set Capacity field (refer to Figure 319)).<br>7.<br>Endurance Groups and NVM Sets are created and deleted using the Capacity Management command (refer<br>to section 5.1.3)<br>8.<br>Namespaces are created and deleted using the Namespace Management command (refer to section 8.1.15).<br>Namespaces are deleted using the Capacity Management command.|Notes:<br>1.<br>This information described in this column is used by the host for creating the entity (e.g., to determine if there<br>is sufficient available capacity) and this information is altered by the controller as a result of the creation or<br>deletion of the entity (e.g., unallocated capacity decreased as a result of entity creation, or unallocated capacity<br>increased as a result of entity deletion).<br>2.<br>NVM Set support requires support for Endurance Groups as described in section 3.2.2.<br>3.<br>Capacity information in the Identify Controller data structure (i.e., TNVMCAP field, UNVMCAP field, and<br>MEGCAP field (refer to Figure 313)).<br>4.<br>Capacity information in the Domain Attributes Entry (i.e., Total Domain Capacity field, Unallocated Domain<br>Capacity field, and Max Endurance Group Domain Capacity field (refer to Figure 325)).<br>5.<br>Capacity information in the Endurance Group Information log page (i.e., TEGCAP field, UEGCAP field (refer<br>to Figure 219)).<br>6.<br>Capacity information in the NVM Set Attributes Entry (i.e., Total NVM Set Capacity field, and Unallocated NVM<br>Set Capacity field (refer to Figure 319)).<br>7.<br>Endurance Groups and NVM Sets are created and deleted using the Capacity Management command (refer<br>to section 5.1.3)<br>8.<br>Namespaces are created and deleted using the Namespace Management command (refer to section 8.1.15).<br>Namespaces are deleted using the Capacity Management command.|Notes:<br>1.<br>This information described in this column is used by the host for creating the entity (e.g., to determine if there<br>is sufficient available capacity) and this information is altered by the controller as a result of the creation or<br>deletion of the entity (e.g., unallocated capacity decreased as a result of entity creation, or unallocated capacity<br>increased as a result of entity deletion).<br>2.<br>NVM Set support requires support for Endurance Groups as described in section 3.2.2.<br>3.<br>Capacity information in the Identify Controller data structure (i.e., TNVMCAP field, UNVMCAP field, and<br>MEGCAP field (refer to Figure 313)).<br>4.<br>Capacity information in the Domain Attributes Entry (i.e., Total Domain Capacity field, Unallocated Domain<br>Capacity field, and Max Endurance Group Domain Capacity field (refer to Figure 325)).<br>5.<br>Capacity information in the Endurance Group Information log page (i.e., TEGCAP field, UEGCAP field (refer<br>to Figure 219)).<br>6.<br>Capacity information in the NVM Set Attributes Entry (i.e., Total NVM Set Capacity field, and Unallocated NVM<br>Set Capacity field (refer to Figure 319)).<br>7.<br>Endurance Groups and NVM Sets are created and deleted using the Capacity Management command (refer<br>to section 5.1.3)<br>8.<br>Namespaces are created and deleted using the Namespace Management command (refer to section 8.1.15).<br>Namespaces are deleted using the Capacity Management command.|Notes:<br>1.<br>This information described in this column is used by the host for creating the entity (e.g., to determine if there<br>is sufficient available capacity) and this information is altered by the controller as a result of the creation or<br>deletion of the entity (e.g., unallocated capacity decreased as a result of entity creation, or unallocated capacity<br>increased as a result of entity deletion).<br>2.<br>NVM Set support requires support for Endurance Groups as described in section 3.2.2.<br>3.<br>Capacity information in the Identify Controller data structure (i.e., TNVMCAP field, UNVMCAP field, and<br>MEGCAP field (refer to Figure 313)).<br>4.<br>Capacity information in the Domain Attributes Entry (i.e., Total Domain Capacity field, Unallocated Domain<br>Capacity field, and Max Endurance Group Domain Capacity field (refer to Figure 325)).<br>5.<br>Capacity information in the Endurance Group Information log page (i.e., TEGCAP field, UEGCAP field (refer<br>to Figure 219)).<br>6.<br>Capacity information in the NVM Set Attributes Entry (i.e., Total NVM Set Capacity field, and Unallocated NVM<br>Set Capacity field (refer to Figure 319)).<br>7.<br>Endurance Groups and NVM Sets are created and deleted using the Capacity Management command (refer<br>to section 5.1.3)<br>8.<br>Namespaces are created and deleted using the Namespace Management command (refer to section 8.1.15).<br>Namespaces are deleted using the Capacity Management command.|Notes:<br>1.<br>This information described in this column is used by the host for creating the entity (e.g., to determine if there<br>is sufficient available capacity) and this information is altered by the controller as a result of the creation or<br>deletion of the entity (e.g., unallocated capacity decreased as a result of entity creation, or unallocated capacity<br>increased as a result of entity deletion).<br>2.<br>NVM Set support requires support for Endurance Groups as described in section 3.2.2.<br>3.<br>Capacity information in the Identify Controller data structure (i.e., TNVMCAP field, UNVMCAP field, and<br>MEGCAP field (refer to Figure 313)).<br>4.<br>Capacity information in the Domain Attributes Entry (i.e., Total Domain Capacity field, Unallocated Domain<br>Capacity field, and Max Endurance Group Domain Capacity field (refer to Figure 325)).<br>5.<br>Capacity information in the Endurance Group Information log page (i.e., TEGCAP field, UEGCAP field (refer<br>to Figure 219)).<br>6.<br>Capacity information in the NVM Set Attributes Entry (i.e., Total NVM Set Capacity field, and Unallocated NVM<br>Set Capacity field (refer to Figure 319)).<br>7.<br>Endurance Groups and NVM Sets are created and deleted using the Capacity Management command (refer<br>to section 5.1.3)<br>8.<br>Namespaces are created and deleted using the Namespace Management command (refer to section 8.1.15).<br>Namespaces are deleted using the Capacity Management command.|



**3.9** **Keep Alive**


The Keep Alive capability uses the Keep Alive Timer on a controller as a watchdog timer to detect
communication failures (e.g., transport failure, host failure, or controller failure) between a host and a
controller. If the Keep Alive Timer feature is supported (i.e., the KAS field is set to a non-zero value (refer
to Figure 313)), the controller shall support the Keep Alive command.


The term Keep Alive Timeout Time (KATT) refers to the time indicated by the value of the Keep Alive
Timeout field on a controller (refer to Figure 398).


The NVMe Transport binding specification for the associated NVMe Transport defines:

  - the minimum Keep Alive Timeout value, if any;

  - the maximum Keep Alive Timeout value, if any; and

  - if the Keep Alive Timer feature is required to be supported and enabled.


122


NVM Express [®] Base Specification, Revision 2.2


NVMe Transports that do not detect a connection loss in a timely manner shall require that the Keep Alive
Timer feature be supported and enabled.


**Keep Alive Timer Configuration**


A host configures the Keep Alive Timer feature by specifying a Keep Alive Timeout value in:

  - the KATO field of a Fabric Connect command (refer to section 6.3); or

  - the KATO field of a Set Features command specifying the Keep Alive Timer feature (refer to section
5.1.25.1.8).


If an NVMe Transport binding specification requires the use of the Keep Alive Timer feature, and a
command attempts to disable the Keep Alive Timer by clearing the Keep Alive Timeout value to 0h, then
the controller shall abort that command with a status code of Keep Alive Timeout Invalid and the Keep Alive
Timeout value at the controller shall not be changed. If a command attempts to set the Keep Alive Timeout
value to a value that exceeds the maximum allowed by the associated NVMe Transport binding
specification, then the controller shall abort that command with a status code of Keep Alive Timeout Invalid
and the Keep Alive Timeout value at the controller shall not be changed. If a command sets the Keep Alive
Timeout value to a non-zero value that is less than the minimum supported by the NVMe Transport or less
than the minimum supported by the specific implementation, then the controller sets the Keep Alive Timeout
value to that minimum value.


As described in section 5.1.25.1.8, the controller rounds any Keep Alive Timeout value set by the host up
to the nearest granularity as reported in the Keep Alive Support (KAS) field (refer to Figure 313). To retrieve
the Keep Alive Timeout value being used by the controller, a host may issue a Get Features command for
the Keep Alive Timer feature.


**Keep Alive Timer Activation**


The Keep Alive Timer is active if:

  - CC.EN is set to ‘1’;

  - CSTS.RDY is set to ‘1’;

  - CC.SHN is cleared to ‘00b’;

  - CSTS.SHST is cleared to ‘00b’; and

  - the Keep Alive Timer feature is enabled as a result of the KATO field being set to a non-zero value
(refer to section 3.9.1).


Otherwise, the Keep Alive Timer is inactive, and a Keep Alive Timeout as described in sections 3.9.3.1 and
3.9.4.1 shall not occur on the controller. Activating an inactive Keep Alive Timer (e.g., a Set Features
command successfully setting the Keep Alive Timeout value to a non-zero value from a value of 0h, or the
host enabling a controller that supports NVMe over Fabrics where the Connect command specified a nonzero Keep Alive Timeout value (refer to Figure 546)) shall initialize the Keep Alive Timer to the Keep Alive
Timeout value.


While the Keep Alive Timer is active, the host should ensure that the Admin Submission Queue has space
for a Keep Alive command.


**Command Based Keep Alive**


For Command Based Keep Alive, the Keep Alive command is sent periodically from the host to the controller
on the Admin Queue. The completion of the Keep Alive command indicates that the host and controller are
able to communicate. For message-based transports, the Keep Alive Timeout is the maximum time an
association remains established without processing a Keep Alive command.


**Command Based Keep Alive on the Controller**


The controller is using Command Based Keep Alive if the controller supports the Keep Alive Timer feature
and the TBKAS bit is cleared to ‘0’ in the Controller Attributes field in the Identify Controller data structure
(refer to Figure 313).


123


NVM Express [®] Base Specification, Revision 2.2


For Command Based Keep Alive:

  - The controller shall start the Keep Alive Timer if the Keep Alive Timer becomes active (refer to
section 3.9.2).

  - The controller shall restart the Keep Alive Timer if the Keep Alive Timer is active, and:


`o` a Keep Alive command completes successfully; or

`o` a Set Features command specifying the Keep Alive Timer feature and a non-zero KATO
field (refer to section 5.1.25.1.8) completes successfully.

  - The controller shall expire the Keep Alive Timer if:


`o` the Keep Alive Timer is active in the controller; and

`o` KATT has elapsed since the Keep Alive Timer was most recently started or restarted.


If the Keep Alive Timer on the controller expires, then the controller shall consider a Keep Alive Timeout to
have occurred. Upon the occurrence of a Keep Alive Timeout, the controller shall perform the cleanup
actions described in section 3.9.5.


**Command Based Keep Alive on the Host**


The host may use Command Based Keep Alive regardless of the Keep Alive mode used by the controller.
To prevent the controller from detecting a Keep Alive Timeout during the use of Command Based Keep
Alive on the host, the host should send Keep Alive commands at KATT/2 to account for delays (e.g.,
transport round-trip times, transport delays, command processing times, and the Keep Alive Timer
granularity) while the Keep Alive Timer is active on the controller. If the host receives a successful
completion to a Set Features command for the Keep Alive feature, then the host should adjust the time at
which the host sends the next Keep Alive command because the controller restarts the Keep Alive Timer.


If a host detects a Keep Alive Timeout and has outstanding commands for which that host has not received
completions (refer to section 3.4.5), then it is strongly recommended that the host take the steps described
in section 9.6 to avoid possible data corruption caused by interaction between outstanding commands and
subsequent commands submitted by that host to another controller.


For an example host implementation of Command Based Keep Alive, the host maintains a Keep Alive Send
Timer for each controller to which the host is connected. The host uses the Keep Alive Send Timer to track
when the host sends a Keep Alive command to the corresponding controller. The host does not know when
the controller fetches the Keep Alive command. Conservatively, the host assumes the controller fetches
the Keep Alive command immediately upon the host sending the Keep Alive command. The host tracks
this time as the last expired timestamp of the Keep Alive Send Timer, for use when starting or restarting
the Keep Alive Send Timer. While the host does restart the Keep Alive Send Timer after a successful Set
Features command for the KATO feature, the host does not change the last expired timestamp when
sending that Set Features command because at that point in time the host does not know the results of that
command.


This example host implementation of Command Based Keep Alive behaves as follows:

  - The host enables the Keep Alive Send Timer if the host requests activation of the Keep Alive Timer
on the controller (e.g., the host enables the controller (refer to section 3.9.2)). The host records the
current time as the last expired timestamp when the Keep Alive Send Timer becomes enabled.

  - The host disables the Keep Alive Send Timer if the host requests deactivation of the Keep Alive
Timer on the controller and the host receives a successful response from the controller (e.g., the
host disables the controller (refer to section 3.9.2)).

  - The host starts a Keep Alive Send Timer if:


`o` the Keep Alive Send Timer becomes enabled; or

`o` a successful Keep Alive command completion is processed by the host.

  - The host restarts a Keep Alive Send Timer if:


`o` the Keep Alive Send Timer is enabled;

`o` a Keep Alive command is not outstanding; and,


124


NVM Express [®] Base Specification, Revision 2.2


`o` a successful Set Features command completion is processed by the host where the
command specified the Keep Alive Timer feature (i.e., Feature Identifier 0Fh) and a nonzero KATO field.

  - If a Keep Alive Send Timer starts or restarts, the host sets the Keep Alive Send Timer to:


`o` KATT/2 minus the time elapsed since the last expired timestamp; or

`o` zero, if the time elapsed since the last expired timestamp is greater than KATT/2.

  - The host stops a Keep Alive Send Timer if the Keep Alive Send Timer becomes disabled.

  - If a Keep Alive Send Timer expires, (i.e., the Keep Alive Send Timer is still enabled and time has
elapsed equal to the value to which the Keep Alive Send Timer was set since the host most recently
started or restarted the Keep Alive Send Timer), then the host records the current time as the last
expired timestamp and sends a Keep Alive command.

  - The host detects a Keep Alive Timeout if the host sends a Keep Alive command and does not
receive a completion for the Keep Alive command before KATT elapses from when the Keep Alive
command was sent.


**Traffic Based Keep Alive**


Traffic Based Keep Alive allows the host and controller to avoid a Keep Alive Timeout in the presence of
Admin or I/O command processing without sending Keep Alive commands.


**Traffic Based Keep Alive on the Controller**


If the controller supports the Keep Alive Timer feature, then support for Traffic Based Keep Alive is indicated
by the TBKAS bit in the Controller Attributes field in the Identify Controller data structure (refer to Figure
313). If the Controller does not support Traffic Based Keep Alive (i.e., the TBKAS bit is cleared to ‘0’), then
the operation of the Keep Alive Timer feature is described in section 3.9.3.


For Traffic Based Keep Alive:

  - The controller shall start a Keep Alive Timeout Interval if the Keep Alive Timer becomes active
(refer to section 3.9.2).

  - The controller shall consider a Keep Alive Timeout to have occurred if:


`o` the Keep Alive Timer is active;

`o` KATT has elapsed since the start of the most recent Keep Alive Timeout Interval; and

`o` no Admin command or I/O command was fetched by the controller during the Keep Alive
Timeout Interval.

  - The controller shall end a Keep Alive Timeout Interval and:


`o` not start a new Keep alive Timeout Interval if:


          - a Keep Alive Timeout occurs; or

          - the Keep Alive Timer becomes inactive (refer to section 3.9.2).


`o` start a new Keep Alive Timeout Interval if the Keep Alive Timer is active, and:


          - a Keep Alive command completes successfully;

          - a Set Features command specifying the Keep Alive Timer feature and a non-zero
KATO field (refer to section 5.1.25.1.8) completes successfully; or

          - KATT has elapsed since the start of the Keep Alive Timeout Interval and a Keep
Alive Timeout did not occur during the Keep Alive Timeout Interval (e.g., an Admin
command or an I/O command was fetched by the controller during the Keep Alive
Timeout Interval).


Upon the occurrence of a Keep Alive Timeout, the controller shall perform the cleanup actions described in
section 3.9.5.


A controller using Traffic Based Keep Alive may require up to 2 * KATT after the controller fetches the most
recent command to detect a Keep Alive Timeout as shown in Figure 90.


125


NVM Express [®] Base Specification, Revision 2.2


**Figure 90: Detecting Timeout Takes up to 2 * KATT**

















Figure 90 shows that periodic check 3, not periodic check 2, detects the Keep Alive Timeout. Therefore,
the time between fetching the most recent command and the check that detects the timeout (i.e., periodic
check 3 in Figure 90) is up to 2 * KATT.


**Traffic Based Keep Alive on the Host**


The host is able to use Traffic Based Keep Alive only if the controller is also using Traffic Based Keep Alive.
The host should not use Traffic Based Keep Alive if the controller is not using Traffic Based Keep Alive
because a controller that uses Command Based Keep Alive detects a Keep Alive Timeout based on the
absence of Keep Alive commands, not the absence of all commands.


Traffic Based Keep Alive on the host is the same as Command Based Keep Alive on the host (refer to
section 3.9.3.2), with two exceptions:

  - The host is not required to submit a Keep Alive command if the host submitted an Admin command
or I/O command and the host processed the completion for that command since the most recent
time the host checked whether sending a Keep Alive command was necessary.

  - To prevent the controller from detecting a Keep Alive Timeout during the use of Traffic Based Keep
Alive on the host, the host should check for sending a Keep Alive command at a rate of KATT/4,
instead of sending a Keep Alive command at a rate of KATT/2, while the Keep Alive Timer is active
on the controller.


Like Command Based Keep Alive, if the host receives a successful completion to a Set Features command
for the Keep Alive feature, then the host should adjust the time at which the host checks for sending the
next Keep Alive command because the controller restarted the Keep Alive Timer.


If a host detects a Keep Alive Timeout and has outstanding commands for which that host has not received
completions (refer to section 3.4.5), then it is strongly recommended that the host take the steps described
in section 9.6 to avoid possible data corruption caused by interaction between outstanding commands and
subsequent commands submitted by that host to another controller.


For an example host implementation of Traffic Based Keep Alive, the host maintains a Keep Alive Send
Timer for each controller to which that host is connected. The host uses the Keep Alive Send Timer to track
when the host checks for sending a Keep Alive command to the corresponding controller. The host does
not know when the controller fetches the Keep Alive command. Conservatively, the host assumes the
controller fetches the Keep Alive command immediately upon the host sending the Keep Alive command.
Whether or not the host sends a Keep Alive command after the Keep Alive Send Timer expires, the host
tracks this time as the last expired timestamp of the Keep Alive Send Timer, for use when starting or
restarting the Keep Alive Send Timer. While the host does restart the Keep Alive Send Timer after a
successful Set Features command for the KATO feature, the host does not change the last expired
timestamp when sending that Set Features command because at that point in time the host does not know
the results of that command.


This example host implementation of Traffic Based Keep Alive behaves as follows:


126


NVM Express [®] Base Specification, Revision 2.2


  - The host enables the Keep Alive Send Timer if the host requests activation of the Keep Alive Timer
on the controller (e.g., the host enables the controller (refer to section 3.9.2)). The host records the
current time as the last expired timestamp when the Keep Alive Send Timer becomes enabled.

  - The host disables the Keep Alive Send Timer if the host requests deactivation of the Keep Alive
Timer on the controller and the host receives a successful response from the controller (e.g., the
host disables the controller (refer to section 3.9.2)).

  - The host starts a Keep Alive Send Timer if:


`o` the Keep Alive Send Timer becomes enabled; or

`o` a successful Keep Alive command completion is processed by the host.

  - The host restarts a Keep Alive Send Timer if:


`o` the Keep Alive Send Timer is enabled;

`o` a Keep Alive command is not outstanding; and

`o` a successful Set Features command completion is processed by the host where the
command specified the Keep Alive Timer feature (i.e., Feature Identifier 0Fh) and a nonzero KATO field.

  - If a Keep Alive Send Timer starts or restarts, the host sets the Keep Alive Send Timer to:


`o` KATT/4 minus the time elapsed since the last expired timestamp; or

`o` zero, if the time elapsed since the last expired timestamp is greater than KATT/4.

  - The host stops a Keep Alive Send Timer if the Keep Alive Send Timer becomes disabled

  - If a Keep Alive Send Timer expires, (i.e., the Keep Alive Send Timer is still enabled and time has
elapsed equal to the value to which the Keep Alive Send Timer was set since the host most recently
started or restarted the Keep Alive Send Timer), then the host records the current time as the last
expired timestamp and the host either:


`o` starts a new Keep Alive Send Timer, if at least one Admin command or I/O command was
submitted to the controller and the completion of that command was processed by the host
since the last Keep Alive Send Timer started (not restarted); or

`o` sends a Keep Alive command.

  - The host detects a Keep Alive Timeout if the host sends a Keep Alive command and does not
receive a completion for that Keep Alive command before KATT elapses from when the Keep Alive
command was submitted.


**Keep Alive Timeout Cleanup**


If a controller detects a Keep Alive Timeout, then the controller shall perform the following actions within
the time specified by the CQT field (refer to Figure 313):

  - record an Error Information Log Entry with the status code Keep Alive Timeout Expired;

  - stop processing commands;

  - set the Controller Fatal Status (CSTS.CFS) bit to ‘1’; and

  - for message-based transports:


`o` terminate the NVMe Transport connections for this association; and

`o` break the host to controller association.


For message-based transports, after completing these steps, a controller may accept a Connect command
(refer to section 6.3) for the Admin Queue from the same or another host in order to form a new association.


If a host detects a Keep Alive Timeout and has outstanding commands for which that host has not received
completions (refer to section 3.4.5), then it is strongly recommended that the host takes steps described in


127


NVM Express [®] Base Specification, Revision 2.2


section 9.6 to avoid possible data corruption caused by interaction between outstanding commands and
subsequent commands submitted by that host to another controller.


**3.10 Privileged Actions**


Privileged actions are actions (e.g., command, property write) that affect or have the potential to affect the
state beyond the controller and attached namespaces.


Examples of privileged actions are:

  - Admin commands including Namespace Management, Namespace Attachment, Virtualization
Management, Format NVM, Set Features with Feature Identifier 17h (i.e., Sanitize Config, refer to
section 5.1.25.1.15), Sanitize, Capacity Management, Controller Data Queue, Migration Receive,
Migration Send, Track Send, and Track Receive;

  - Property Writes including NVM Subsystem Reset; and

  - Some Vendor specific commands and properties.


**3.11 Firmware Update Process**


The process for a firmware update to be activated in a domain (refer to section 3.2.5) by a reset is:


1. The host issues a Firmware Image Download command to download the firmware image to a

controller. There may be multiple portions of the firmware image to download, thus the offset for
each portion of the firmware image being downloaded on that controller is specified in the Firmware
Image Download command. The data provided in the Firmware Image Download command should
conform to the Firmware Update Granularity indicated in the Identify Controller data structure or
the firmware update may fail;
2. After the firmware is downloaded to that controller, the next step is for the host to submit a Firmware

Commit command to that controller. The Firmware Commit command verifies that the last firmware
image downloaded is valid and commits that firmware image to the firmware slot indicated for future
use. A firmware image that does not start at offset zero, contains gaps, or contains overlapping
regions is considered invalid. A controller may employ additional vendor specific means (e.g.,
checksum, CRC, cryptographic hash, or a digital signature) to determine the validity of a firmware
image:


a. The Firmware Commit command may also be used to activate a firmware image associated

with a previously committed firmware slot;


3. The host performs an action that results in a Controller Level Reset (refer to section 3.7.2) on that

controller to cause the firmware image specified in the Firmware Slot field in the Firmware Commit
command to be activated:


a. In some cases, a Conventional Reset (refer to the NVM Express NVMe over PCIe Transport

Specification) or NVM Subsystem Reset is required to activate a firmware image. This
requirement is indicated by Firmware Commit command specific status (refer to section
5.1.8.1);


and


4. After the reset has completed, host software re-initializes the controller. This includes re-allocating

I/O Submission and Completion Queues. Refer to sections 3.5.1 and 3.5.2.


The process for a firmware update to be activated on a domain without a reset is:


1. The host issues a Firmware Image Download command to download the firmware image to a

controller. There may be multiple portions of the firmware image to download, thus the offset for
each portion of the firmware image being downloaded on that controller is specified in the Firmware
Image Download command. The data provided in the Firmware Image Download command should
conform to the Firmware Update Granularity indicated in the Identify Controller data structure or
the firmware update may fail;


128


NVM Express [®] Base Specification, Revision 2.2


2. The host submits a Firmware Commit command on that controller with a Commit Action of 011b

which specifies that the firmware image should be activated immediately without reset. The
downloaded firmware image shall replace the firmware image in the firmware slot. If no firmware
image was downloaded since the last reset or Firmware Commit command, (i.e., the first step was
skipped), then that controller shall verify and activate the firmware image in the specified slot. If
that controller starts to activate the firmware image, any controllers affected by the new firmware
image send a Firmware Activation Starting asynchronous event to the host if Firmware Activation
Notices are enabled (refer to Figure 392):


a. The Firmware Commit command may also be used to activate a firmware image associated

with a previously committed firmware slot;


3. The controller completes the Firmware Commit command. The following actions are taken in

certain error scenarios:


a. If the firmware image is invalid, then the controller aborts the command with an appropriate

status code (e.g., Invalid Firmware Image);
b. If the firmware activation was not successful because a Controller Level Reset is required to

activate this firmware image, then the controller aborts the command with a status code of
Firmware Activation Requires Controller Level Reset and the firmware image is applied at the
next Controller Level Reset;
c. If the firmware activation was not successful because an NVM Subsystem Reset is required to

activate this firmware image, then the controller aborts the command with a status code of
Firmware Activation Requires NVM Subsystem Reset and the firmware image is applied at the
next NVM Subsystem Reset;
d. If the firmware activation was not successful because a Conventional Reset is required to

activate this firmware image, then the controller aborts the command with a status code of
Firmware Activation Requires Conventional Reset and the firmware image is applied at the
next Conventional Reset; and
e. If the firmware activation was not successful because the firmware activation time requires

more time than the time reported by the MTFA field in the Identify Controller data structure,
then the controller aborts the command with a status code of Firmware Activation Requires
Maximum Time Violation. In this case, the firmware image was committed to the specified
firmware slot. To activate that firmware image, the host may issue a Firmware Commit
command that specifies:


i. a Commit Action set to 010b (i.e., activate using a Controller Level Reset); and
ii. the same firmware slot.


If the controller transitions to the D3cold state (refer to the PCI Express Base Specification) after the
submission of a Firmware Commit command that attempts to activate a firmware image and before the
completion of that command, then the controller may resume operation with either the firmware image
active at the time the Firmware Commit command was submitted or the firmware image that was activated
by that command.


If the firmware image is not able to be successfully loaded, then the controller shall revert to the firmware
image present in the most recently activated firmware slot or the baseline read-only firmware image, if
available, and indicate the failure as an asynchronous event with a Firmware Image Load Error. If the
controller changes (e.g., reverts) the firmware image while a sanitize operation is in progress, then that
sanitize operation fails (refer to section 8.1.24.3).


If a host overwrites (i.e., updates) the firmware image in the active firmware slot, then the previously active
firmware image may no longer be available. As a result, any action (e.g., power cycling the controller) that
requires the use of that firmware slot may instead use the firmware image that is currently in that firmware
slot. If the firmware image that is currently in that firmware slot would be activated by such an action
replacing the currently active firmware, then:

  - this is a pending firmware activation with reset; and

  - a controller aborts subsequent Sanitize commands with a status code indicating the appropriate
reset required to activate the pending activation as defined in section 5.1.22.


129


NVM Express [®] Base Specification, Revision 2.2


Host software should not overlap firmware/boot partition image update command sequences (refer to
section 1.5.41). During a firmware image update command sequence, if a Firmware Image Download
command or a Firmware Commit command is submitted for another firmware/boot partition image update
command sequence, the results of both that command and the in-progress firmware image update are
undefined.


Host software should use the same controller or Management Endpoint (refer to the NVM Express
Management Interface Specification) for all commands that are part of a firmware image update command
sequence. If the commands for a single firmware/boot partition image update command sequence are
submitted to more than one controller and/or Management Endpoint, the controller may abort the Firmware
Commit command with Invalid Firmware Image status.


After downloading a firmware image, host software issues a Firmware Commit command before
downloading additional firmware images. Processing of the first Firmware Image Download command after
completion of a Firmware Commit command shall cause the controller to discard remaining portions, if any,
of downloaded images. If a reset occurs between a firmware download and completion of the Firmware
Commit command, then the controller shall discard all portion(s), if any, of downloaded images.


130


