NVM Express [®] Base Specification, Revision 2.2


**Annex A. Sanitize Operation Considerations (Informative)**


**A.1** **Overview**


The Sanitize command starts a sanitize operation that makes all user data previously written to the
sanitization target inaccessible (i.e., all user data has been purged, as defined in IEEE Std 2883-2022). It
is very difficult to prove that the sanitize operation successfully purged all user data. This annex provides
some context and considerations for understanding the result of the operation and the practical limitations
for auditing the result of the sanitize operation.


**A.2** **Hidden Storage (Overprovisioning)**


Sanitize operations purge all physical storage in the sanitization target that is able to hold user data. Many
NVMe SSDs contain more physical storage than is addressable through the interface (e.g.,
overprovisioning). That physical storage is used for vendor specific purposes which may include providing
increasing endurance, improving performance, and providing extra capacity to allow retiring bad or wornout storage without affecting capacity. This excess capacity as well as any retired storage are not accessible
through the interface. Vendor specific innovative use of this extra capacity supports advantages to the end
user, but the lack of observability makes it difficult to ensure that all storage within the sanitization target
was correctly purged. Only the accessible storage is able to be audited for the results of a sanitization
operation.


**A.3** **Integrity checks and No-Deallocate After Sanitize**


Another issue is availability of the data returned through the interface. Some of the sanitize operations (e.g.,
Block Erase) affect the physical devices in such a way that directly reading the accessible storage may
trigger internal integrity checks resulting in error responses instead of returning the contents of the storage.
Other sanitize operations (e.g., Crypto Erase) may scramble the vendor specific internal format of the data,
also resulting in error responses instead of returning the contents of the storage.


To compensate for these issues, a controller may perform additional internal write operations to media that
is able to be allocated for user data (i.e., additional media modification, refer to section 8.1.24.1) so that all
media that is allocated for user data is readable without error. However, this has the side effect of potentially
significant additional wear on the media as well as the side effect of obscuring the results of the initial
sanitize operation (i.e., the writes destroy the ability to forensically audit the result of the initial sanitize
operation). Given this side effect, process audits of sanitize behavior only provide effective results when
the No-Deallocate After Sanitize bit is set the same way (e.g., set to ‘1’) for both process audits and the
individual forensic device audits.


The Sanitize command introduced in NVM Express Base Specification, Revision 1.3 included a mechanism
to specify that sanitized media allocated for user data not be deallocated, thereby allowing observations of
the results of the sanitization operation. However, some architectures and products (e.g., integrity checking
circuitry) interact with this capability in such a way as to defeat the sanitize result observability purpose.
New features were added to NVM Express Base Specification, Revision 1.4 that include extended
information about the sanitization capabilities of devices, a new asynchronous event, and configuration of
the response to No-Deallocate After Sanitize requests. These features are intended to both support new
systems that understand the new capabilities, as well to help manage legacy systems that do not
understand the new capabilities without losing the ability to sanitize as requested.


These issues in returning the contents of accessible storage do not apply if the sanitization target is in the
Media Verification state (refer to section 8.1.24.3.6). In that state, failure of internal integrity checks do not
cause error responses to Read commands (refer to the Media Verification section of the NVM Command
Set Specification). Because the Sanitize command that caused entry to the Media Verification state
specified the Enter Media Verification State (EMVS) bit set to ‘1’, the controller does not perform the
additional media modification described in this section.


669


NVM Express [®] Base Specification, Revision 2.2


**A.4** **Bad Media and Vendor Specific NAND Use**


Another audit capability that is not supported by NVM Express is checking that any media that could not be
sanitized (e.g., bad physical blocks) has been removed from the pool of storage that is able to be used as
addressable storage.


An approach that is performed under some circumstances is removing the physical storage components
from the NVM Express device after a sanitize operation and reading the contents in laboratory conditions.
However, this approach also has multiple difficulties. When physical storage components are removed from
an NVM Express device, much context is lost. This includes:


a) any encoding for zero’s/one’s balance;
b) identification of which components contain device firmware or other non-data information; and
c) which media has been retired and cannot be sanitized.


670


NVM Express [®] Base Specification, Revision 2.2


**Annex B. Host Considerations (Informative)**


**B.1** **Basic Steps when Building a Command**


When host software builds a command for the controller to execute, it first checks to make sure that the
appropriate Submission Queue (SQ) is not full. The Submission Queue is full when the number of entries
in the queue is one less than the queue size. Once an empty slot (pFreeSlot) is available:


1. Host software builds a command at SQ[pFreeSlot] with:


a. CDW0.OPC is set to the appropriate command to be executed by the controller;
b. CDW0.FUSE is set to the appropriate value, depending on whether the command is a

fused operation;
c. CDW0.CID is set to a unique identifier for the command when combined with the

Submission Queue identifier;
d. The Namespace Identifier, NSID field, is set to the namespace the command applies to;
e. MPTR shall be filled in with the offset to the beginning of the Metadata Region, if there is

a data transfer and the namespace format contains metadata as a separate buffer;
f. PRP1 and/or PRP2 (or SGL Entry 1 if SGLs are used) are set to the source/destination of
data transfer, if there is a data transfer; and
g. CDW10 – CDW15 are set to any command specific information;


2. Host software then completes a transport specific action in order to submit the command for

processing.


**B.2** **Creating an I/O Submission Queue**


This example describes how host software creates an I/O Submission Queue that utilizes non-contiguous
PRP entries. Creating an I/O Submission Queue that utilizes a PRP List is only valid if the controller
supports non-contiguous queues as indicated in CAP.CQR.


Prior to creating an I/O Submission Queue, host software shall create the I/O Completion Queue that the
SQ uses with the Create I/O Completion Queue command.


To create an I/O Submission Queue, host software builds a Create I/O Submission Queue command for
the Admin Submission Queue. Host software builds the Create I/O Submission Queue command in the
next free Admin Submission Queue command location. The attributes of the command are:

  - CDW0.OPC is set to 01h;

  - CDW0.FUSE is cleared to 00b indicating that this is not a fused operation;

  - CDW0.CID is set to a free command identifier;

  - The NSID field is cleared to 0h; Submission Queues are not specific to a namespace;

  - MPTR is cleared to 0h; metadata is not used for this command;

  - PRP1 is set to the physical address of the PRP List. The PRP List is shown in Figure 758 for a
PRP List with three entries;

  - PRP2 is cleared to 0h; PRP Entry 2 is not used for this command;

  - CDW10.QSIZE is set to the size of queue to create. In this case, the value is set to 191, indicating
a queue size of 192 entries. The queue size shall not exceed the maximum queue entries
supported, indicated in the CAP.MQES field;

  - CDW10.QID is set to the Submission Queue identifier;

  - CDW11.CQID is set to the I/O Completion Queue identifier where command completions are
posted;

  - CDW11.QPRIO is set to 10b, indicating a Medium priority queue; and

  - CDW11.PC is cleared to ‘0’ indicating that the data buffer indicated by PRP1 is not physically
contiguously.


Host software then completes a transport specific action in order to submit the command for processing.
Host software shall maintain the PRP List unmodified in host memory until the Submission Queue is
deleted.


671


NVM Express [®] Base Specification, Revision 2.2


**Figure 758: PRP List Describing I/O Submission Queue**


**B.3** **Executing a Fused Operation**


This example describes how host software creates and executes a fused command, specifically Compare
and Write for a total of 16 KiB of data. In this case, there are two commands that are created. The first
command is the Compare, referred to as CMD0. The second command is the Write, referred to as CMD1.
In this case, end-to-end data protection is not enabled and the size of each logical block is 4 KiB.


To build commands for a fused operation, host software utilizes two available adjacent command locations
in the appropriate I/O Submission Queue as is described in section 3.4.2.


The attributes of the Compare command are:

  - CMD0.CDW0.OPC is set to 05h for Compare;

  - CMD0.CDW0.FUSE is set to 01b indicating that this is the first command of a fused operation;

  - CMD0.CDW0.CID is set to a free command identifier;

  - CMD0.NSID is set to identify the appropriate namespace;


672


NVM Express [®] Base Specification, Revision 2.2


  - If metadata is being used in a separate buffer, then the location of that buffer is specified in the
CMD0.MPTR field;

  - The physical address of the first page of the data to compare:


`o` If PRPs are used, CMD0.PRP1 is set to the physical address of the first page of the data
to compare and CMD0.PRP2 is set to the physical address of the PRP List. The PRP List
is shown in Figure 759 for a PRP List with three entries; or

`o` If the command uses SGLs, CMD0.SGL1 is set to an appropriate SGL segment descriptor
depending on whether more than one descriptor is needed;

  - CMD0.CDW10.SLBA is set to the first LBA to compare against. Note that this field also spans
Command Dword 11;

  - CMD0.CDW12.LR is cleared to ‘0’ to indicate that the controller should apply all available error
recovery means to retrieve the data for comparison;

  - CMD0.CDW12.FUA is cleared to ‘0’, indicating that the data may be read from any location,
including a volatile cache, in the NVM subsystem;

  - CMD0.CDW12.PRINFO is cleared to 0h since end-to-end protection is not enabled;

  - CMD0.CDW12.NLB is set to 3h, indicating that four logical blocks of a size of 4 KiB each are to be
compared against;

  - CMD0.CDW14 is cleared to 0h since end-to-end protection is not enabled; and

  - CMD0.CDW15 is cleared to 0h since end-to-end protection is not enabled.


**Figure 759: PRP List Describing Data to Compare**


The attributes of the Write command are:

  - CMD1.CDW0.OPC is set to 01h for Write;

  - CMD1.CDW0.FUSE is set to 10b indicating that this is the second command of a fused operation;

  - CMD1.CDW0.CID is set to a free command identifier;


673


NVM Express [®] Base Specification, Revision 2.2


  - CMD1.NSID is set to identify the appropriate namespace. This value shall be the same as
CMD0.NSID;

  - If metadata is being used in a separate buffer, then the location of that buffer is specified in the
CMD1.MPTR field;

  - The physical address of the first page of data to write is identified:


`o` If the command uses PRPs, then CMD1.PRP1 is set to the physical address of the first
page of the data to write and CMD1.PRP2 is set to the physical address of the PRP List.
The PRP List includes three entries; or

`o` If the command uses SGLs, CMD1.SGL1 is set to an appropriate SGL segment descriptor
depending on whether more than one descriptor is needed;

  - CMD1.CDW10.SLBA is set to the first LBA to write. Note that this field also spans Command Dword
11. This value shall be the same as CMD0.CDW10.SLBA;

  - CMD1.CDW12.LR is cleared to ‘0’ to indicate that the controller should apply all available error
recovery means to write the data to the NVM;

  - CMD1.CDW12.FUA is cleared to ‘0’, indicating that the data may be written to any location,
including a volatile cache, in the NVM subsystem;

  - CMD1.CDW12.PRINFO is cleared to 0h since end-to-end protection is not enabled;

  - CMD1.CDW12.NLB is set to 3h, indicating that four logical blocks of a size of 4 KiB each are to be
compared against. This value shall be the same as CMD0.CDW12.NLB;

  - CMD1.CDW14 is cleared to 0h since end-to-end protection is not enabled; and

  - CMD1.CDW15 is cleared to 0h since end-to-end protection is not enabled.


Host software then completes a transport specific action in order to submit the command for processing.
Note that the transport specific submit action shall indicate both commands have been submitted at one
time.


**B.4** **Asynchronous Event Request Host Software Recommendations**


This section describes the recommended host software procedure for Asynchronous Event Requests.


The host sends _n_ Asynchronous Event Request commands (refer to section 3.5.1, step 12). When an
Asynchronous Event Request completes (providing Event Type, Event Information, and Log Page details):

  - If the event(s) in the reported Log Page may be disabled with the Asynchronous Event
Configuration feature (refer to section 5.1.25.1.5), then host software issues a Set Features
command for the Asynchronous Event Configuration feature specifying to disable reporting of all
events that utilize the Log Page reported. Host software should wait for the Set Features command
to complete;

  - Host software issues a Get Log Page command requesting the Log Page reported as part of the
Asynchronous Event Command completion. Host software should wait for the Get Log Page
command to complete;

  - Host software parses the returned Log Page. If the condition is not persistent, then host software
should re-enable all asynchronous events that utilize the Log Page. If the condition is persistent,
then host software should re-enable all asynchronous events that utilize the Log Page except for
the one(s) reported in the Log Page. The host re-enables events by issuing a Set Features
command for the Asynchronous Event Configuration feature;

  - Host software should issue an Asynchronous Event Request command to the controller (restoring
to _n_ the number of these commands outstanding); and

  - If the reporting of event(s) was disabled, host software should enable reporting of the event(s) using
the Asynchronous Event Configuration feature. If the condition reported may persist, host software
should continue to monitor the event (e.g., spare below threshold) to determine if reporting of the
event should be re-enabled.


674


NVM Express [®] Base Specification, Revision 2.2


**B.5** **Updating Controller Doorbell Properties using a Shadow Doorbell Buffer**


**B.5.1. Shadow Doorbell Buffer Overview**


Controllers that support the Doorbell Buffer Config command are typically emulated controllers where this
feature is used to enhance the performance of host software running in Virtual Machines. If supported by
the controller, host software may enable Shadow Doorbell buffers by submitting the Doorbell Buffer Config
command (refer to section 5.2.5).


After the completion of the Doorbell Buffer Config command, host software shall submit commands by
updating the appropriate entry in the Shadow Doorbell buffer instead of updating the controller's
corresponding doorbell property. If updating an entry in the Shadow Doorbell buffer changes the value from
being less than or equal to the value of the corresponding EventIdx buffer entry to being greater than that
value, then the host shall also update the controller's corresponding doorbell property to match the value
of that entry in the Shadow Doorbell buffer. Queue wrap conditions shall be taken into account in all
comparisons in this paragraph.


The controller may read from the Shadow Doorbell buffer and update the EventIdx buffer at any time (e.g.,
before the host writes to the controller's doorbell property).


**B.5.2. Example Algorithm for Controller Doorbell Property Updates**


Host software may use modular arithmetic where the modulus is the queue depth to decide if the controller
doorbell property should be updated, specifically:

  - Compute _X_ as the new doorbell value minus the corresponding EventIdx value, modulo queue
depth; and

  - Compute _Y_ as the new doorbell value minus the old doorbell value in the shadow doorbell buffer,
also modulo queue depth.


If _X_ is less than or equal to _Y_, the controller doorbell property should be updated with the new doorbell
value.


**B.6** **Examples of Incorrect Command Retry Handling After Communication Loss**


Section 9.6.3 describes requirements for host retry of outstanding commands after communication loss. In
this situation, the response of a command is unknown and hence the host has no information about the
extent, if any, to which the controller has processed that command. Many commands are not safe to
unconditionally retry if they have been processed in part or completely. This annex describes examples of
problematic situations caused by retrying an outstanding command without regard to the consequences of
that retry.


**B.6.1. Write after Write**


In the example shown in Figure 760, the host loses communication with Controller 1 and does not receive
a response from Controller 1 for an idempotent command that changes user data at location X to A (e.g.,
an NVM Command Set Write command). The following events occur:

  - The host retries that command on Controller 2 (Retry: Write A at Location X), and the retry succeeds
quickly.

  - The completion of that retry leads to the host subsequently submitting a command that changes
the user data at the same location to B (Write B at Location X).

  - During this time, Controller 1 has been processing the original outstanding command (Write A at
Location X), and that command’s change of user data at location X to A finally takes effect after the
user data at location X has already been changed to B.


The final outcome is that the user data at location X is A, which is incorrect and an example of data
corruption.


For an idempotent command that changes user data or NVM subsystem state, this example shows why
the host should not report the results of that command, including any retry of that command, to higher-level


675


NVM Express [®] Base Specification, Revision 2.2


software until the host is able to determine that no further controller processing of that command and any
retry of that command is possible (refer to section 9.6.2).


**Figure 760: Write after Write**















**B.6.2. Non-Idempotent Command**


In the example shown in Figure 761, the host loses communication with Controller 1 and does not receive
a response from Controller 1 for a Namespace Management command that creates a namespace (refer to
section 5.1.21). The host ensures that no further controller processing of that command is possible (refer
to section 9.6.2), and then retries that command on Controller 2, which creates a second namespace.


This example shows why higher-level software (e.g., an associated application, filesystem or database)
should take steps to determine that a retry of a non-idempotent command does not cause unintended
changes to NVM subsystem state (e.g., number of namespaces).


676


NVM Express [®] Base Specification, Revision 2.2


**Figure 761: Non-Idempotent Command**















**B.6.3. Retried Command Does Not Succeed**


In the example shown in Figure 762, the host loses communication with Controller 1 and does not receive
a response to a Reservation Register command that unregisters the host (refer to section 7.6). The host
ensures that no further controller processing of that command is possible (refer to section 9.6.2), and then
retries that command on Controller 2. As a result of the original command unregistering the host, the host
is no longer a registrant, and for that reason, the controller returns a status code of Reservation Conflict
(refer to section 8.1.22.4).


**Figure 762: Retried Command Does Not Succeed**









Command does not complete successfully!





This example shows why an error status code is able to be returned if a non-idempotent command is retried
after the original command has been processed. An analogous example is possible for the Compare and
Write fused operation (refer to the Fused Operation section of the NVM Command Set Specification)
because that fused operation is not idempotent


677


NVM Express [®] Base Specification, Revision 2.2


**B.6.4. Retried Command Affects Another Host**


In the example shown in Figure 763, two hosts use Location X in a namespace for coordination. Writing the
value A to Location X indicates that step A in a processing sequence has been completed, and writing the
value B indicates that step B in the processing sequence has been completed, where higher-level software
requires that step B follow step A.


Host 1 indicates completion of step A by writing the value A to Location X, but loss of communication
prevents Host 1 from receiving the completion of that command. Host 2 observes that step A is complete,
quickly performs step B, and indicates completion of step B by writing the value B to Location X.


In the absence of receiving a completion for the original command, Host 1 retries writing the value A to
Location X, overwriting the completion of step B reported by Host 2. This example shows that retry of
commands that are able to affect the behavior of other hosts is problematic. In this example, higher-level
software needs a mechanism to indicate that the writes to Location X are not safe to retry after a delay.


**Figure 763: Retried Command Affects Another Host**













Location X is A not B!







This sort of higher-level software usage of ordinary NVMe commands (e.g., NVM Command Set Write
commands) for coordination and synchronization among multiple hosts is strongly discouraged because
retry of these commands after communication loss is problematic. Higher-level software should instead use
mechanisms intended for coordination among multiple hosts. Two examples of such mechanisms are:

  - Reservations (refer to section 8.1.22); and

  - Compare and Write fused operations (refer to the Fused Operation section of the NVM Command
Set Specification).


In addition, command retries that modify NVM subsystem state (e.g., a Set Features command that modifies
a feature that has any scope that is visible to other hosts as described in Figure 386) are able to affect the
behavior of other hosts. Use of commands that modify NVM subsystem state for coordination and
synchronization among multiple hosts is likewise strongly discouraged.


678


NVM Express [®] Base Specification, Revision 2.2


**Annex C. Power Management and Consumption (Informative)**


NVM Express power management capabilities allow the host to manage power for a controller. Power
management includes both control and reporting mechanisms.


For information on transport power management (e.g., PCIe, RDMA), refer to the applicable NVM Express
transport specification.


The scope of NVM Express power management is the controller (refer to section 5.1.25.1.2).


NVM Express power management uses the following functionality:


a) Features:

    - Power Management (refer to section 5.1.25.1.2 and section 8.1.17);

    - Autonomous Power State Transition (refer to section 5.1.25.1.6 and section 8.1.17.2);

    - Non-Operational Power State Configuration (refer to section 5.1.25.1.10 and section 8.1.17.1);
and

    - Spinup Control (refer to section 5.1.25.1.18);


b) NVM subsystem workloads (refer to 8.1.17.3); and
c) Runtime D3 transitions (refer to section 8.1.17.4).


Controller thermal management may cause a transition to a lower power state, interacting with these
Features:


a) Temperature Threshold (refer to section 5.1.25.1.3);
b) Host Controlled Thermal Management (refer to section 5.1.25.1.9 and section 8.1.17.5); and
c) access to host memory buffer (refer to section 5.1.25.2.4) may be prohibited in non-operational

power state.


NVM Express power management uses these reporting mechanisms:


a) properties:


    - Controller Power Scope (CAP.CPS) (refer to Figure 36);


b) fields in the Identify Controller data structure (refer to Figure 313):

    - RTD3 Resume Latency (RTD3R);

    - RTD3 Entry Latency (RTD3E);

    - Non-Operational Power State Permissive Mode;

    - Number of Power States Support (NPSS);

    - Autonomous Power State Transition Attributes (APSTA); and

    - Power State 0 Descriptor (PSD0) through Power State 31 Descriptor (PSD31) (refer to Figure
314);


c) Features:

    - Power Management (refer to section 5.1.25.1.2);

    - Temperature Threshold (refer to section 5.1.25.1.3);

    - Autonomous Power State Transition (refer to section 5.1.25.1.6 and section 8.1.17.2);

    - Non-Operational Power State Configuration (refer to section 5.1.25.1.10 and section 8.1.17.1);

    - Host Controlled Thermal Management (refer to section 5.1.25.1.9 and section 8.1.17.5);

    - Host Memory Buffer (refer to section5.1.25.2.4); and

    - Spinup Control (refer to section 5.1.25.1.18);


and


d) log pages:


    - SMART / Health Information log page fields (refer to section 5.1.12.1.3):


`o` Thermal Management Temperature [1-2] Transition Count; and


679


NVM Express [®] Base Specification, Revision 2.2


`o` Total Time For Thermal Management Temperature [1-2];


and


- Persistent Event Log fields (refer to section 5.1.12.1.14):


`o` Power On Hours (POH) (refer to Figure 227);

`o` Power Cycle Count (refer to Figure 227);

`o` Controller Power Cycle (refer to Figure 235); and

`o` Power on milliseconds (refer to Figure 235).


680


