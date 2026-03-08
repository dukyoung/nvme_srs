NVM Express [®] Base Specification, Revision 2.2


**8 Extended Capabilities**


This section describes extended capabilities that are optional. Section 8.1 describes extended capabilities
that are common to all transport models. Section 8.2 describes extended capabilities that are specific to
the Memory-based transport model. Section 8.3 describes extended capabilities that are specific to the
Message-based transport model.


**8.1** **Common Extended Capabilities**


This section describes extended capabilities that are common to all transport models.


**Asymmetric Namespace Access Reporting**


**Asymmetric Namespace Access Reporting Overview**


Asymmetric Namespace Access (ANA) occurs in environments where namespace access characteristics
(e.g., performance or ability to access the media) may vary based on:

  - the controller used to access the namespace (e.g., Fabrics); and

  - the internal configuration of the NVM subsystem. Asymmetric Namespace Access Reporting is
used to indicate to the host information about those access characteristics.


Shared namespaces may be accessed through controllers via multiple PCIe ports or fabric ports (refer to
section 2.4.1). The controllers that provide access to a shared namespace may provide identical access
characteristics through all controllers (i.e., symmetric access), or may provide different access
characteristics through some controllers (i.e., asymmetric access).


Private namespaces are accessed by only one controller at a time. The access characteristics of the
namespace through that controller may be impacted as a result of changes to the internal configuration of
the NVM subsystem. If the access characteristics of the namespace through that controller are impacted
by the internal configuration of the NVM subsystem, then asymmetric access occurs.


Symmetric access to a namespace occurs when:

  - the access characteristics using one controller are identical to the access characteristics when
using a different controller; and

  - changes to the internal configuration of the NVM subsystem do not impact the access
characteristics.


Asymmetric access to a namespace occurs when:

  - the access characteristics using one controller may differ from the access characteristics when
using a different controller; or

  - changes to the internal configuration of the NVM subsystem may impact the access characteristics.


While commands may be sent to a shared namespace through any attached controller with asymmetric
access, the characteristics (e.g., performance or ability to access the media) may differ based on which
controller is used; as a result, the host should consider those characteristics when selecting which controller
to use for each command that accesses the namespace. The NVM subsystem may perform autonomous
internal reconfiguration that results in a change to the access characteristics.


If an NVM subsystem supports Asymmetric Namespace Access Reporting, then all controllers in that NVM
subsystem shall:

  - set the Asymmetric Namespace Access Reporting Support (ANARS) bit to ‘1’ in the Controller
Multi-path I/O and Namespace Sharing Capabilities (CMIC) field in the Identify Controller data
structure (refer to Figure 313) to indicate support for Asymmetric Namespace Access Reporting;

  - set the Report ANA Optimized State (RANAOS) bit to ‘1’ in the Asymmetric Namespace Access
Capabilities (ANACAP) field in the Identify Controller data structure to indicate that the ANA
Optimized state is able to be reported;


471


NVM Express [®] Base Specification, Revision 2.2


  - set the Report ANA Non-Optimized State (RANANOS) bit to ‘1’ in the ANACAP field in the Identify
Controller data structure if ANA Non-Optimized state is able to be reported;

  - set the Report ANA Inaccessible State (RANAIS) bit to ‘1’ in the ANACAP field in the Identify
Controller data structure if ANA Inaccessible state is able to be reported;

  - set the Report ANA Persistent Loss State (RANAPLS) bit to ‘1’ in the ANACAP field in the Identify
Controller data structure if ANA Persistent Loss state is able to be reported;

  - set the Report ANA Change State (RANACS) bit to ‘1’ in the ANACAP field in the Identify Controller
data structure if ANA Change state is able to be reported;

  - support Asymmetric Namespace Access Change Notices (refer to section 5.1.25.1.5); and

  - support the Asymmetric Namespace Access log page (refer to section 5.1.12.1.13).


Namespaces attached to a controller that supports Asymmetric Namespace Access Reporting shall:

  - be members of an ANA Group; and

  - supply a valid ANA Group Identifier in the ANA Group Identifier (ANAGRPID) field in the Identify
Namespace data structure (refer to the applicable I/O Command Set specification).


A controller that supports Asymmetric Namespace Access Reporting may also support multiple domains
(refer to section 3.2.5).


Figure 586 shows an example of an NVM subsystem where access characteristics vary as a result of the
presence of two independent domains. In this example, the non-volatile storage media for namespace B
and for namespace C are contained within the same domain that contains controller 2. As a result, controller
2 provides optimized access to namespace B and to namespace C while controller 1 does not provide
optimized access to namespace B or to namespace C. In an NVM subsystem that supports multiple
domains (refer to section 3.2.5), the Media Access Boundary shown in Figure 586 may be a Communication
boundary as shown in Figure 71 and Figure 72.


**Figure 586: Namespace B and C optimized through Controller 2**


Port _x_ NVM Port _y_













To provide optimized access to namespace B through controller 1, the NVM subsystem may be
administratively reconfigured, or may perform autonomous internal reconfiguration actions that change the
access characteristics of namespace B when accessed through controller 1 and controller 2 as shown in
Figure 587. Controller 2 provides optimized access to namespace C while controller 1 provides optimized
access to namespace B. In an NVM subsystem that supports multiple domains (refer to section 3.2.5), the
Media Access Boundary shown in Figure 587 may be a Communication boundary as shown in Figure 71
and Figure 72.


472


NVM Express [®] Base Specification, Revision 2.2


**Figure 587: Namespace B optimized through Controller 1**


Port _x_ NVM Port _y_















**ANA Groups**


Namespaces that are members of the same ANA Group perform identical asymmetric namespace access
state transitions. The ANA Group maintains the same asymmetric namespace access state for all
namespaces that are members of that ANA Group (i.e., a change in the asymmetric namespace access
state of one namespace only occurs as part of a change in the asymmetric namespace access state of all
namespaces that are members of that ANA Group). Namespaces that are members of the same ANA
Group shall be members of the same domain (refer to section 2.3.1). The method for assigning namespaces
to ANA Groups is outside the scope of this specification.


An ANA Group may contain zero or more namespaces, zero or more NVM Sets, or zero or more Endurance
Groups. The mapping of namespaces, NVM Sets, and Endurance Groups to ANA Groups is vendor
specific.


A valid ANA Group Identifier is a non-zero value that is less than or equal to ANAGRPMAX (refer to Figure
313).


The ANA Group Identifier (ANAGRPID) for each ANA Group shall be unique within the NVM subsystem. If
the ANA Group ID Change Support (ANAGIDCS) bit in the ANACAP field in the Identify Controller data
structure is set to ‘1’, then the ANA Group Identifier shall not change while the namespace is attached to
any controller in the NVM subsystem. If the ANAGIDCS bit is cleared to ‘0’, then the ANA Group Identifier
may change while the namespace is attached to any controller in the NVM subsystem. If the ANA Group
Identifier changes, the controller shall issue the Asymmetric Namespace Access Change Notice as
described in 8.1.1.9.


If two or more participating NVM subsystems provide access to a dispersed namespace, and that dispersed
namespace is a member of an ANA Group on any participating NVM subsystem, then each participating
NVM subsystem shall contain an ANA Group whose members include that dispersed namespace. The
ANAGRPID for a dispersed namespace may or may not be the same on each participating NVM subsystem.


Figure 588 shows the following four namespaces:

  - the private namespace A in a first ANA Group;

  - namespace B and namespace D, that are in the same second ANA Group; and

  - namespace C that is in a third ANA Group.


473


NVM Express [®] Base Specification, Revision 2.2


**Figure 588: Multiple Namespace groups**



Port _x_ NVM Port _y_



Port z































**Asymmetric Namespace Access states**


The Asymmetric Namespace Access State indicates information about the characteristics of the
relationship between a controller and an ANA Group. The following asymmetric namespace access states
are defined:

  - ANA Optimized (refer to section 8.1.1.4);

  - ANA Non-Optimized (refer to section 8.1.1.5);

  - ANA Inaccessible (refer to section 8.1.1.6);

  - ANA Persistent Loss (refer to section 8.1.1.7); and

  - ANA Change (refer to section 8.1.1.8).


**ANA Optimized state**


While the relationship between the controller and an ANA group is in this state, the characteristic of that
relationship to each namespace in that group is optimized. Commands processed by a controller that
reports this state for an ANA Group provide optimized access characteristics to any namespace in that ANA
Group. A controller that supports ANA Reporting shall support reporting this state.


While in this state, all commands, functions, and operations supported by the namespace shall perform as
described in this specification.


**ANA Non-Optimized state**


While the relationship between the controller and an ANA group is in this state, the characteristic of that
relationship to each namespace in that group is non-optimized. Commands processed by a controller that
reports this state for an ANA Group provide non-optimized access characteristics (e.g., the processing of
some commands, especially those involving data transfer, may operate with lower performance or may use
NVM subsystem resources less effectively than if a controller is used that reports the optimized state) to
any namespace in that ANA Group. Support for reporting this state is optional.


While in this state, all commands, functions, and operations supported by the namespace shall perform as
described in this specification.


474


NVM Express [®] Base Specification, Revision 2.2


**ANA Inaccessible state**


While the relationship between the controller and an ANA group is in this state, the characteristic of that
relationship to each namespace in that group is inaccessible. Commands processed by a controller that
reports this state for an ANA Group are not able to access user data of namespaces in that ANA Group.
The namespaces may become accessible through the controller reporting this state at a future time (i.e., a
subsequent ANA state transition may occur). Support for reporting this state is optional.


While in this state, accurate namespace related capacity information may not be available. As a result,
some namespace capacity information returned in the Identify Namespace data structure (e.g., the NUSE
field and the NVMCAP field), are cleared to 0h. For that namespace capacity information, hosts should use
the Identify Namespace data structure returned from a controller that reports the relationship between the
controller and the namespace to be in the ANA Optimized state or in the ANA Non-Optimized state.


A controller shall abort commands, other than those described in section 8.1.1.10, with a status code of
Asymmetric Access Inaccessible if those commands are submitted while the relationship between the
specified namespace and the controller processing the command is in this state.


While ANA Inaccessible state is reported by a controller for the namespace, the host should retry the
command on a different controller that is reporting ANA Optimized state or ANA Non-Optimized state. If no
controllers are reporting ANA Optimized state or ANA Non-Optimized state, then a transition may be
occurring such that a controller reporting the Inaccessible state may become accessible and the host should
retry the command on the controller reporting Inaccessible state for at least ANATT seconds (refer to Figure
313). Refer to section 8.1.2.2.


**ANA Persistent Loss state**


While the relationship between the controller and an ANA group is in this state, the characteristic of that
relationship to each namespace in that group is persistently inaccessible. Commands processed by a
controller that reports this state for an ANA Group are persistently not able to access user data of
namespaces in that ANA Group. The relationship between a controller and an ANA Group in this state shall
not transition to any other ANA state. Support for reporting this state is optional.


While in this state, accurate namespace related capacity information may not be available. As a result,
some namespace capacity information returned in the Identify Namespace data structure (e.g., the NUSE
field and the NVMCAP field), are cleared to 0h. For that namespace capacity information, hosts should use
the Identify Namespace data structure returned from a controller that reports the relationship between the
controller and the namespace to be in the ANA Optimized state or in the ANA Non-Optimized state.


A controller shall abort commands, other than those described in section 8.1.1.10, with a status code of
Asymmetric Access Persistent Loss if those commands are submitted while the relationship between the
specified namespace and the controller processing the command is in this state.


While ANA Persistent Loss state is reported by a controller for the namespace, the host should retry the
command on a different controller that is reporting ANA Optimized state or ANA Non-Optimized state. If no
controllers are reporting ANA Optimized state or ANA Non-Optimized state, then a transition may be
occurring such that a controller reporting the Inaccessible state may become accessible and the host should
retry the command on the controller reporting Inaccessible state for at least ANATT seconds (refer to Figure
313).


**ANA Change state**


The change from one asymmetric namespace access state to another asymmetric namespace access state
is called a transition. Transitions may occur in such a way that the ANA Change state is not visible to the
host (i.e., the ANA Change state may or may not be reported in the Asymmetric Namespace Access State
field in the Asymmetric Namespace Access log page (refer to section 5.1.12.1.13)). Support for reporting
this state is optional.


A controller shall abort commands, other than those described in 8.1.1.10, with a status code of Asymmetric
Access Transition if those commands are submitted while the relationship between the specified
namespace and the controller processing the command is in this state.


475


NVM Express [®] Base Specification, Revision 2.2


While ANA Change state is reported by a controller for the namespace, the host should:


a) after a short delay, retry the command on the same controller for at least ANATT (refer to Figure

313) seconds (e.g., if ANATT is 30, perform 3 retries at 10 s intervals, or 10 retries at 3 s intervals);
or
b) retry the command on a different controller that is reporting ANA Optimized state or ANA Non
Optimized state.


**Asymmetric Namespace Access Change Notifications**


If Asymmetric Namespace Access Change Notices are enabled on a controller, then an Asymmetric
Namespace Access Change Notice shall be sent as described in section 5.1.25.1.5 by the controllers where
the change occurred:


a) if an ANA Group Identifier (refer to Figure 313) changes;
b) if an asymmetric namespace access state transition fails (e.g., a transition begins, but does not

complete and the controller returns to the state that existed before the transition began); or
c) upon entry to the following ANA states, unless the state entry is a result of a namespace

attachment:

    - ANA Optimized State;

    - ANA Non-Optimized State;

    - ANA Inaccessible State; and

    - ANA Persistent Loss State.


**Asymmetric Namespace Access States Command Processing Effects**


Processing of Admin commands that:

  - are not NVM Command Set specific commands; and

  - do not use the Namespace Identifier (i.e., Figure 142 – “Namespace Identifier Used” column
indicates “No”),


are not affected by ANA states, except as specified in Figure 589.


Figure 589 describes Asymmetric Namespace Access effects on command processing.


**Figure 589: ANA effects on Command Processing**



|Command|ANA State|Effects on command processing|
|---|---|---|
|Get Features|ANA Inaccessible, ANA<br>Persistent Loss, or ANA<br>Change|The following feature identifiers are not available1: <br>a)<br>Reservation Notification Mask (i.e., 82h);<br>b)<br>Reservation Persistence (i.e., 83h); and<br>c)<br>I/O Command Set specific feature identifiers2.|
|Get Log Page|ANA Inaccessible, ANA<br>Persistent Loss, or ANA<br>Change|The following log pages are affected:<br>a)<br>Error Information (i.e., 01h): The log page is not required<br>to contain entries for namespaces whose relationship to<br>the controller processing the command is in the:<br>a.<br>ANA Inaccessible state (refer to section 8.1.1.6);<br>b.<br>the ANA Persistent Loss state (refer to section<br>8.1.1.7); or<br>c.<br>the ANA Change state (refer to section 8.1.1.8).<br>The following log pages are not available1: <br>a)<br>Media Unit Status log page (refer to section 5.1.12.1.16);<br>and<br>b)<br>Supported Capacity Configuration List log page (refer to<br>section 5.1.12.1.17).|


476






NVM Express [®] Base Specification, Revision 2.2


**Figure 589: ANA effects on Command Processing**







|Command|ANA State|Effects on command processing|
|---|---|---|
|Identify|ANA Inaccessible or<br>ANA Persistent Loss|Capacity fields in the Identify Namespace data structure (refer to<br>the applicable I/O Command Set specification) information are<br>cleared to 0h.|
|Set Features|ANA Inaccessible|The saving of features shall not be supported and the following<br>feature identifiers are not available1: <br>a)<br>Reservation Notification Mask (i.e., 82h);<br>b)<br>Reservation Persistence (i.e., 83h); and<br>I/O Command Set specific feature identifiers2. <br>If the NSID is set to FFFFFFFFh, then the command shall abort3 <br>with a status code of Asymmetric Access Inaccessible (refer to<br>section 8.1.1.6).|
|Set Features|ANA Change|The saving of features shall not be supported and the following<br>feature identifiers are not available1: <br>a)<br>Reservation Notification Mask (i.e., 82h);<br>b)<br>Reservation Persistence (i.e., 83h); and<br>c)<br>I/O Command Set specific feature identifiers2. <br>If the NSID is set to FFFFFFFFh, then the command shall abort3 <br>with a status code of Asymmetric Access Transition (refer to section<br>8.1.1.8).|
|Set Features|ANA Persistent Loss|The command shall abort with a status code of Asymmetric Access<br>Persistent Loss (refer to section 8.1.1.7).|
|Notes:<br>1.<br>If the ANA state is ANA Inaccessible State, then commands that use feature identifiers or log pages that are not<br>available shall abort with a status code of Asymmetric Access Inaccessible. If the ANA state is ANA Persistent<br>Loss State, then commands that use feature identifiers or log pages that are not available shall abort with a<br>status code of Asymmetric Access Persistent Loss. If the ANA state is ANA Change State, then commands that<br>use feature identifiers or log pages that are not available shall abort with a status code of Asymmetric Access<br>Transition.<br>2.<br>I/O Command Set specific definition. Refer to each I/O Command Set specification for applicability and additional<br>details, if any.<br>3.<br>If any namespace that is attached to the controller is in an ANA Group that is in the ANA Inaccessible state, the<br>ANA Persistent Loss state, or the ANA Change state, then the command shall abort with the indicated status.<br>Depending on the ANA state of the ANA Group that contains a namespace (e.g., an ANA state changes during<br>the processing of the command), the specified feature identifier may be altered for some attached namespaces<br>and not altered for other attached namespaces.|Notes:<br>1.<br>If the ANA state is ANA Inaccessible State, then commands that use feature identifiers or log pages that are not<br>available shall abort with a status code of Asymmetric Access Inaccessible. If the ANA state is ANA Persistent<br>Loss State, then commands that use feature identifiers or log pages that are not available shall abort with a<br>status code of Asymmetric Access Persistent Loss. If the ANA state is ANA Change State, then commands that<br>use feature identifiers or log pages that are not available shall abort with a status code of Asymmetric Access<br>Transition.<br>2.<br>I/O Command Set specific definition. Refer to each I/O Command Set specification for applicability and additional<br>details, if any.<br>3.<br>If any namespace that is attached to the controller is in an ANA Group that is in the ANA Inaccessible state, the<br>ANA Persistent Loss state, or the ANA Change state, then the command shall abort with the indicated status.<br>Depending on the ANA state of the ANA Group that contains a namespace (e.g., an ANA state changes during<br>the processing of the command), the specified feature identifier may be altered for some attached namespaces<br>and not altered for other attached namespaces.|Notes:<br>1.<br>If the ANA state is ANA Inaccessible State, then commands that use feature identifiers or log pages that are not<br>available shall abort with a status code of Asymmetric Access Inaccessible. If the ANA state is ANA Persistent<br>Loss State, then commands that use feature identifiers or log pages that are not available shall abort with a<br>status code of Asymmetric Access Persistent Loss. If the ANA state is ANA Change State, then commands that<br>use feature identifiers or log pages that are not available shall abort with a status code of Asymmetric Access<br>Transition.<br>2.<br>I/O Command Set specific definition. Refer to each I/O Command Set specification for applicability and additional<br>details, if any.<br>3.<br>If any namespace that is attached to the controller is in an ANA Group that is in the ANA Inaccessible state, the<br>ANA Persistent Loss state, or the ANA Change state, then the command shall abort with the indicated status.<br>Depending on the ANA state of the ANA Group that contains a namespace (e.g., an ANA state changes during<br>the processing of the command), the specified feature identifier may be altered for some attached namespaces<br>and not altered for other attached namespaces.|


**Asymmetric Namespace Access Reporting – Host Considerations (Informative)**


**Host ANA Normal Operation**


The host determines if ANA is supported by examining the Asymmetric Namespace Access Reporting
Support (ANARS) bit in the CMIC field in the Identify Controller data structure (refer to Figure 313). The
NSID or identifier (refer to section 4.5) is used to determine when multiple paths to the same namespace
that is not a dispersed namespace are available. For dispersed namespaces, globally unique namespace
identifiers (refer to section 8.1.9.2) are used to determine when multiple paths are available to the same
namespace, as described in section 8.1.9.5. The host examines the ANA log page (refer to section
5.1.12.1.13) for each controller to determine the ANA state of each group of namespaces attached to that
controller.


To send a command to a namespace, the host should select a controller that reports the ANA Optimized
State (refer to section 8.1.1.4) and send the command to that controller. If more than one controller that


477


NVM Express [®] Base Specification, Revision 2.2


reports the ANA Optimized state for a namespace are found, then the host may use all of those controllers
to send commands.


If there are no controllers that report the ANA Optimized state for a namespace, then the host should select
a controller that reports ANA Non-Optimized State (refer to section 8.1.1.5) for that namespace and send
the command to that controller. If more than one controller that reports ANA Non-Optimized state for a
namespace are found, then the host may use all of those controllers to send commands.


If multiple controllers are being used, then the algorithm for determining which controller to use next is
outside the scope of this specification (e.g., the host may select a simple round robin algorithm, a queue
depth weighted algorithm, a transfer length weighted algorithm, or any other algorithm).


If there are no controllers that report the ANA Optimized state for a namespace and there are no controllers
that report the ANA Non-Optimized state for that namespace, then the host should examine controllers that
report the ANA Inaccessible state as described in section 8.1.2.2.


**Host ANA Inaccessible Operation**


If the ANA log page reports an ANA state of ANA Inaccessible State for an ANA Group or a command
returns a status code of Asymmetric Access Inaccessible, then the host should:

  - not use that controller to send commands to any namespace in that ANA Group; and

  - select a different controller for sending commands to all namespaces in that ANA Group.


If there are no controllers that report the ANA Optimized state for a namespace and there are no controllers
that report the ANA Non-Optimized state, then a transition may be occurring that also impacts controllers
that are reporting the ANA Inaccessible state. As a result, the host should use the methods described for
Host ANA Transition operation (refer to section 8.1.2.5) to determine if the controller reporting ANA
Inaccessible state transitions during the ANATT time interval to an ANA state that enables commands to
be processed by that controller.


**Host ANA Persistent Loss Operation**


If the ANA log page reports an ANA state of ANA Persistent Loss State for an ANA Group or a command
returns a status code of Asymmetric Access Persistent Loss, then the host should not use that controller to
send commands to any namespace in that ANA Group, and select a different controller for sending
commands to any namespace in that ANA Group. If the controller supports the Namespace Management
capability (refer to section 8.1.15), then the namespaces in an ANA Group reporting this state should be
detached.


**Host ANA Change Notice Operation**


If the ANA log page reports an ANA state of ANA Change State for an ANA Group or a command returns
a status code of Asymmetric Access Transition, then the host should temporarily not use that controller to
send commands to any namespace in that ANA Group. If only controllers reporting ANA Inaccessible State
are available, then the host should follow these procedures to determine which controller to use. To use a
controller, the host may:


a) if Asymmetric Namespace Access Change Notices are enabled (refer to section 5.1.25.1.5) on the

controller, wait for an Asymmetric Namespace Access Change Notice from that controller. Upon
receipt of that notice, the host should examine the ANA log page to determine the new ANA state
and resume sending commands based on the new ANA state. Such notice should occur within the
ANATT time (refer to Figure 313); or
b) delay and retry the command during the ANATT time interval. The host should not immediately

retry, but rather, divide the ANATT time into equal intervals for command retry purposes (e.g., if
ANATT is 30, perform 3 retries at 10 s intervals, or 10 retries at 3 s intervals). During or upon
completion of the ANATT time interval, the new ANA state of the ANA Group should be known
(e.g., one of the command retries returned a different status that indicates completion of the
transition to a new ANA state). If the retried command did not complete without error, the ANA log


478


NVM Express [®] Base Specification, Revision 2.2


page should be examined on each controller that provides access to the namespace and the host
should resume sending commands based on the new ANA state.


If the ANATT time interval expires, then the host should use a different controller for sending commands to
the namespaces in that ANA Group. The ANATT interval reported by the controller should prevent this type
of timer expiration from occurring.


**Host ANA Transition Operation**


Receipt of an Asymmetric Namespace Access Change Notice from a controller may indicate:


a) that the ANA state reported in one or more ANA Group Descriptors has changed;
b) a new NSID has been added to one or more of the ANA Group Descriptors;
c) an NSID has been removed from one or more of the ANA Group Descriptors; and/or
d) the NSID of a namespace has moved from one ANA Group Descriptor to a different ANA Group

Descriptor (i.e., the ANAGRPID field in the Identify Namespace data structure for that namespace
has changed), if the ANA Group ID Change Support (ANAGIDCS) bit in the ANACAP field is cleared
to ‘0’ in the Identify Controller data structure (refer to Figure 313).


As a result of receiving an Asymmetric Namespace Access Change Notice, the host should read the ANA
log page (refer to section 5.1.12.1.13) to check for each of those possible changes.


**All Paths Down Condition**


An all paths down condition occurs when there are no paths available on the host to access the namespaces
in an ANA Group (i.e., the NVM media). To determine whether an all paths down condition has occurred,
the host may examine the ANA log page on each controller that provides access to the namespaces in a
particular ANA Group. All paths that are not in the ANA Persistent Loss state should be checked. If no paths
to the namespaces in that ANA Group become available (i.e., transition to the ANA Optimized state or the
ANA Non-Optimized state) for the duration of an ANATT time interval, then an all paths down condition has
occurred for the namespaces in that ANA Group.


**Boot Partitions**


Boot Partitions provide an optional area of NVM storage that may be read by the host without the host
initializing queues or enabling the controller. The simplified interface to access Boot Partitions may be used
for platform initialization code (e.g., a bootloader that is executed from host ROM) to boot to a pre-OS
environment (e.g., UEFI) instead of storing the image on another non-volatile storage medium (e.g., SPI
flash). Refer to section 8.1.3.1 for the procedure to read the contents of a Boot Partition.


A controller that supports Boot Partitions has two Boot Partitions of equal size using Boot Partition identifiers
0h and 1h. The two Boot Partitions allow the host to update one and verify the contents before marking the
Boot Partition active. Controllers in the NVM subsystem may share the same Boot Partitions.


The contents of Boot Partitions are only modified using the Firmware Image Download and Firmware
Commit commands (refer to section 8.1.3.2) and may be secured using either the Boot Partition Write
Protection Config feature or the Replay Protected Memory Block to prevent unauthorized modifications
(refer to section 8.1.3.3).


**Reading from a Boot Partition**


A Boot Partition is a continuous block of data as shown in Figure 590, that the host may read via NVMe
properties.


479


NVM Express [®] Base Specification, Revision 2.2


**Figure 590: Boot Partition Overview**


To read the contents of a Boot Partition using NVMe properties, the host allocates a Boot Partition Memory
Buffer in host memory for the controller to copy contents from a Boot Partition. The host initializes the Boot
Partition Memory Buffer Base Address. The host sets the Boot Partition ID, Boot Partition Read Size, and
Boot Partition Read Offset to initiate the Boot Partition read operation. The host may continue reading from
the Boot Partition until the entire Boot Partition has been read.


A portion of the Boot Partition may be read by the host any time the NVM subsystem is powered (i.e.,
whether or not CC.EN is set to ‘1’). The host shall not modify transport specific properties (described in the
applicable NVMe Transport binding specification), reset, or shutdown the controller while a Boot Partition
read is in progress.


To read data from a Boot Partition, the host follows these steps:


1. Initialize the transport (e.g., PCIe link), if necessary;
2. Determine if Boot Partitions are supported by the controller (CAP.BPS);
3. Determine which Boot Partition is active (BPINFO.ABPID) and the size of the Boot Partition

(BPINFO.BPSZ);
4. Allocate a physically contiguous memory buffer in the host to store the contents of a Boot Partition;
5. Initialize the address (BPMBL.BMBBA) into the memory buffer where the contents should be

copied;
6. If no Boot Partition read is in progress (i.e., the Boot Read Status (BPINFO.BRS) field is not set to

01b), then initiate the transfer of data from a Boot Partition by writing to the Boot Partition Read
Select (BPRSEL) property. This includes setting the Boot Partition Identifier (BPRSEL.BPID) field,
the Boot Partition Read Size (BPRSEL.BPRSZ) field, and the Boot Partition Read Offset
(BPRSEL.BPROF) field;
7. Wait for the controller to set the BPINFO.BRS field to 01b while the controller is transferring the

Boot Partition contents to indicate that a Boot Partition read operation is in progress; and
8. Wait for the controller to completely transfer the requested portion of the Boot Partition, indicated

in the status field (BPINFO.BRS). If BPINFO.BRS is set to 10b, the requested Boot Partition data
has been transferred to the Boot Partition Memory Buffer. If BPINFO.BRS is set to 11b, there was
an error transferring the requested Boot Partition data and the host may request the Boot Partition
data again.


In constrained memory environments, the host may read the contents of a Boot Partition with a small Boot
Partition Memory Buffer by reading a small portion of a Boot Partition, moving the data out of the Boot
Memory Buffer to another memory location, and then reading another portion of the Boot Partition until the
entire Boot Partition has been read.


If the Boot Partition log page is supported (refer to section 5.1.12.1.1), then the Boot Partition can be
accessed through the Boot Partition log page (refer to section 5.1.12.1.21).


**Writing to a Boot Partition**


Boot Partition contents may be modified by the host using the Firmware Image Download and Firmware
Commit commands while the controller is enabled (CC.EN set to ‘1’).


480


NVM Express [®] Base Specification, Revision 2.2


The process for updating a Boot Partition is:


1. The host issues a Firmware Image Download command to download the contents of the Boot

Partition to a controller. There may be multiple portions of the Boot Partition to download, thus the
offset for each portion of the Boot Partition being downloaded is specified in the Firmware Image
Download command. A host shall send the Boot Partition image in order starting with the beginning
of the Boot Partition;
2. The host transitions the Boot Partition that is to be updated to the Write Unlocked State (refer to

section 8.1.3.3);
3. The host submits a Firmware Commit command (refer to section 5.1.8) on that controller with a

Commit Action of 110b which specifies that the downloaded image replaces the contents of the
Boot Partition specified in the Boot Partition ID field;
4. The controller completes the Firmware Commit command. The following actions are taken in

certain error scenarios:
a. If the firmware activation was not successful because the Boot Partition could not be written,

then the controller reports an error of Boot Partition Write Prohibited;
5. (Optional) The host reads the contents of the Boot Partition to verify they are correct (refer to section

8.1.3.1). A host updates the active Boot Partition ID by issuing a Firmware Commit command with
a Commit Action of 111b; and
6. The host transitions the Boot Partition to either the Write Locked State or Write Locked Until Power

Cycle State to prevent further modification (refer to section 8.1.3.3).


If an internal error, reset, or power loss condition occurs while committing the downloaded image to a Boot
Partition, the contents of the Boot Partition may contain the old contents, new contents, or a mixture of both.
Host software should verify the contents of a Boot Partition before marking that Boot Partition active to
ensure the active Boot Partition is stable.


Host software should not read the contents of a Boot Partition while writing to the Boot Partition. The
controller may return a combination of new and old data if the host attempts to perform a Boot Partition
read operation while overwriting the contents.


Host software should not overlap firmware/boot partition image update command sequences (refer to
section 1.5.41). During a boot partition image update command sequence, if a Firmware Image Download
command or a Firmware Commit command is submitted for another firmware/boot partition image update
command sequence, the results of both that command and the in-progress firmware image update are
undefined.


Host software should use the same controller or Management Endpoint (refer to the NVM Express
Management Interface Specification) for all commands that are part of a boot partition image update
command sequence. If the commands for a single firmware/boot partition image update command
sequence are submitted to more than one controller and/or Management Endpoint, the controller may abort
the Firmware Commit command with Invalid Firmware Image status.


**Boot Partition Write Protection**


A controller that supports both Boot Partitions and RPMB shall support at least one of the following Boot
Partition write protection mechanisms:

  - Set Features Boot Partition Write Protection (refer to section 8.1.3.3.1); or

  - RPMB Boot Partition Write Protection (refer to section 8.1.3.3.2).


It is not recommended that a controller support both Set Features Boot Partition Write Protection and RPMB
Boot Partition Write Protection.


A controller that supports Boot Partitions and does not support RPMB shall support Set Features Boot
Partition Write Protection.


A host is able to determine whether Set Features Boot Partition Write Protection is supported by checking
the value of the Set Features Boot Partition Write Protection Support bit of the Boot Partition Capabilities
field in the Identify Controller Data Structure (refer to Figure 313).


481


NVM Express [®] Base Specification, Revision 2.2


A host is able to determine whether RPMB Boot Partition Write Protection is supported by checking the
RPMB Boot Partition Write Protection Support field of the Boot Partition Capabilities field in the Identify
Controller data structure (refer to Figure 313). Only controllers compliant with NVM Express Base
Specification, Revision 2.0 and earlier are allowed to report a value of 00b (i.e., support not specified) in
that field. If a controller reports the 00b value, a host is able to determine if RPMB Boot Partition Write
Protection is supported by checking whether the controller supports both Boot Partitions (refer to section
3.1.4.1) and RPMB (refer to section 5.1.13.2.1) because a controller compliant with NVM Express Base
Specification, Revision 2.0 and earlier is required to support RPMB Boot Partition Write Protection when
the controller supports both Boot Partitions and RPMB.


If Set Features Boot Partition Write Protection is supported and either:


1) RPMB Boot Partition Write Protection is not supported; or
2) RPMB Boot Partition Write Protection is not enabled,


then the Boot Partition write protection states are able to be configured via the Boot Partition Write
Protection Config feature. Section 8.1.3.3.1 covers the case when only the Boot Partition Write Protection
Config feature is supported.


If RPMB Boot Partition Write Protection is supported and enabled, then the Boot Partition write protection
states are able to be configured using RPMB (refer to section 8.1.21). Section 8.1.3.3.2 covers the case
where only RPMB Boot Partition Write Protection is supported.


Only one mechanism controls the Boot Partition write protection states at a time. Section 8.1.3.3.3 covers
considerations when both Boot Partition write protection mechanisms are supported.


If any Boot Partition is shared across multiple controllers (refer to section 8.1.3), then the write protection
state of the Boot Partition shall be enforced by all controllers that share that Boot Partition.


**8.1.3.3.1** **Set Features Boot Partition Write Protection**


Figure 591 shows an overview of the Boot Partition write protection states for each Boot Partition when only
Set Features Boot Partition Write Protection is supported.


**Figure 591: Set Features Boot Partition Write Protection State Machine Model**


power up
or
power cycle







Figure 592 defines the write protection states per Boot Partition if Set Features Boot Partition Write
Protection is supported.


482


NVM Express [®] Base Specification, Revision 2.2


**Figure 592: Set Features Boot Partition Write Protection State Definitions**








|State|Definition|Persistent Across|Col4|
|---|---|---|---|
|**State**|**Definition**|**Power Cycles**|**Controller**<br>**Level Resets**|
|Write Unlocked|The Boot Partition is not write locked.|No|Yes|
|Write Locked|The Boot Partition is write locked.|Yes|Yes|
|Write Locked Until<br>Power Cycle|The Boot Partition is write locked until the next<br>power cycle.|No|Yes|



If Set Features Boot Partition Write Protection is supported, then the default state for all Boot Partitions is
the Write Locked state. In this state, a host may read from a Boot Partition but is unable to modify that Boot
Partition. To enable modification of a Boot Partition, a host has to first transition the Boot Partition to the
Write Unlocked state by setting the appropriate Boot Partition Write Protection State to Write Unlocked
using the Boot Partition Write Protection Config feature via the Set Features command.


In the Write Unlocked state, a host may read from and modify a Boot Partition. Any Boot Partition in a Write
Unlocked state transitions to the Write Locked state when the controller undergoes a power cycle.


If Set Features Boot Partition Write Protection is supported, then both Boot Partitions support a Write
Locked Until Power Cycle state. In this state, the Boot Partition can be read from but is prohibited from
being modified. Additionally, once a Boot Partition enters the Write Locked Until Power Cycle state, the
Boot Partition remains in this state until the controller is power cycled.


The Write Locked Until Power Cycle state is prohibited in multi-domain NVM subsystems with Boot
Partitions shared across controllers (e.g., since clearing that state requires simultaneous power cycle of all
controllers that share the Boot Partitions). The result of a command that attempts to use that state in a
multi-domain NVM subsystem is specified in section 5.1.25.1.32.


**8.1.3.3.2** **RPMB Boot Partition Write Protection**


Figure 593 shows an overview of the Boot Partition write protection states for each Boot Partition when only
RPMB Boot Partition Write Protection is supported.


483


NVM Express [®] Base Specification, Revision 2.2


**Figure 593: RPMB Boot Partition Write Protection State Machine Model**













Figure 595 defines the write protection states per Boot Partition if RPMB Boot Partition Write Protection is
supported.


**Figure 594: RPMB Boot Partition Write Protection State Definitions**







|State|Definition|Persistent Across|Col4|
|---|---|---|---|
|**State**|**Definition**|**Power Cycles**|**Controller**<br>**Level Resets**|
|**RPMB Boot Partition Write Protection Disabled**|**RPMB Boot Partition Write Protection Disabled**|**RPMB Boot Partition Write Protection Disabled**|**RPMB Boot Partition Write Protection Disabled**|
|Write Unlocked|The Boot Partition is not write locked.|Yes|Yes|
|**RPMB Boot Partition Write Protection Enabled**|**RPMB Boot Partition Write Protection Enabled**|**RPMB Boot Partition Write Protection Enabled**|**RPMB Boot Partition Write Protection Enabled**|
|Write Unlocked|The Boot Partition is not write locked.|No|No|
|Write Locked|The Boot Partition is write locked.|Yes|Yes|


If Set Features Boot Partition Write Protection is not supported by the controller, then prior to enabling
RPMB Boot Partition Write Protection, the default state for all Boot Partitions is the Write Unlocked state. If
Set Features Boot Partition Write Protection is also supported by the controller, then the default state for
all Boot Partitions is the Write Locked state, regardless of whether RPMB Boot Partition Write Protection
has been enabled or not. Refer to section 8.1.3.3.1 for more details on Boot Partition write protection when
RPMB Boot Partition Write Protection is disabled and section 8.1.3.3.3 for additional considerations when
both Boot Partition write protection capabilities are supported.


If Set Features Boot Partition Write Protection is not supported by the controller, then all Boot Partitions
remain unlocked until RPMB Boot Partition Write Protection is enabled by the host. A host enables RPMB
Boot Partition Write Protection by setting the Boot Partition Write Protection Enabled bit in the RPMB Device
Configuration Block data structure (refer to section 8.1.21). Once RPMB Boot Partition Write Protection is
enabled, the controller shall reject Authenticated Device Configuration Block Writes that attempt to disable
the RPMB Boot Partition Write Protection mechanism (i.e., enabling RPMB Boot Partition Write Protection


484


NVM Express [®] Base Specification, Revision 2.2


is permanent). Once RPMB Boot Partition Write Protection is enabled, Boot Partitions are able to be
modified only after write unlocking the Boot Partition using RPMB.


After enabling RPMB Boot Partition Write Protection:


a) The default state for all Boot Partitions is the Write Locked state. In this state, a host may read a

Boot Partition. In this state, the controller rejects attempts to write to a Boot Partition using the
Firmware Commit command;
b) Each Boot Partition may be locked or unlocked independently using the corresponding bit in the

Device Configuration Block data structure. A Boot Partition may be unlocked in the same command
that enables RPMB Boot Partition Write Protection; and
c) If any Boot Partition has been unlocked, a power cycle or Controller Level Reset event results in

that Boot Partition becoming write locked.


**8.1.3.3.3** **Interactions between Boot Partition Write Protection Mechanism**


Figure 595 shows an overview of the Boot Partition write protection states for each Boot Partition when
both Boot Partition write protection mechanisms are supported. Supporting both Boot Partition write
protection mechanisms is discouraged, as specified in section 8.1.3.3.


485


NVM Express [®] Base Specification, Revision 2.2


**Figure 595: Boot Partition Write Protection State Machine Model**



















If both Boot Partition write protection mechanisms are supported by the controller, only one Boot Partition
write protection mechanism controls the write protection states of the Boot Partitions for the controller at
any time. If RPMB Boot Partition Write Protection is enabled, then RPMB Boot Partition Write Protection
controls the Boot Partition write protection states (refer to section 8.1.3.3.2 and section 8.1.21). If RPMB
Boot Partition Write Protection is disabled, then Set Features Boot Partition Write Protection controls the
Boot Partition write protection states (refer to section 8.1.3.3.1 and section 5.1.25.1.32). Control of the Boot
Partition write protection states transitions from Set Features Boot Partition Write Protection to RPMB Boot
Partition Write Protection by enabling RPMB Boot Partition Write Protection when the Boot Partitions are
in either a Write Unlocked or Write Locked state.


If both Boot Partition write protection capabilities are supported and an RPMB authentication key has not
been programmed for RPMB target 0, there is a possibility of malicious bypass of a Boot Partition’s Write
Locked Until Power Cycle state. In order to prevent malicious bypass of a Boot Partition's Write Locked
Until Power Cycle state, a controller that supports both Boot Partition write protection mechanisms is
required to prevent host attempts to enable RPMB Boot Partition Write Protection when either Boot Partition


486


NVM Express [®] Base Specification, Revision 2.2


is in a Write Locked Until Power Cycle state. Refer to section 8.1.21 for the specific behavior that the
controller exhibits under this condition.


**Capacity Management**


**Overview**


Capacity Management is a capability for organizing physical media into Endurance Groups and NVM Sets.
There are two different forms of Capacity Management, Fixed Capacity Management and Variable Capacity
Management. A controller that supports Capacity Management shall support at least one form.


Capacity Management commands shall not be supported by Exported NVM Subsystems.


The host uses Fixed Capacity Management to create Endurance Groups and NVM Sets by selecting a
configuration which explicitly allocates Media Units (refer to section 8.1.4.2) to Endurance Groups and NVM
Sets.


The host uses Variable Capacity Management to:

    - create a single Endurance Group by specifying the desired capacity;

    - create a single NVM Set by specifying the desired capacity;

    - delete a single Endurance Group; and

    - delete a single NVM Set.


The Capacity Adjustment Factor is the ratio between the capacity consumed by an Endurance Group from
the Unallocated NVM Capacity field in the Identify Controller data structure and the total NVM capacity in
that Endurance Group, i.e.:


𝐶𝑎𝑝𝑎𝑐𝑖𝑡𝑦 𝐶𝑜𝑛𝑠𝑢𝑚𝑒𝑑
𝐶𝑎𝑝𝑎𝑐𝑖𝑡𝑦 𝐴𝑑𝑗𝑢𝑠𝑡𝑚𝑒𝑛𝑡 𝐹𝑎𝑐𝑡𝑜𝑟= 𝐼𝑁𝑇𝐸𝐺𝐸𝑅 ~~(~~
𝐸𝑛𝑑𝑢𝑟𝑎𝑛𝑐𝑒 𝐺𝑟𝑜𝑢𝑝 𝐶𝑎𝑝𝑎𝑐𝑖𝑡𝑦 [∗100)]


(E.g., the value 200 indicates that creation of an Endurance Group with a total NVM capacity of 5 GiB
consumes 10 GiB of the Unallocated NVM Capacity indicated by the controller).


If an Endurance Group is created, then the controller performs the following actions as an atomic operation:


a) the value indicated by the Unallocated NVM Capacity (UNVMCAP) field of the Identify Controller

data structure is changed based on the requested capacity, the Capacity Adjustment Factor of the
created Endurance Group, and the granularity at which the controller allocates NVM capacity; and
b) the Endurance Group Identifier is added to the Endurance Group List.


If an Endurance Group is deleted, then the controller performs the following actions in sequence:


1) the Endurance Group Identifier is removed from the Endurance Group List;
2) if the Media Unit Status log page is supported, then the Endurance Group Identifier field is cleared

to 0h in all Media Unit Status Descriptors, if any, that indicate the deleted Endurance Group;
3) every NVM Set in the Endurance Group is deleted; and
4) the value indicated by the Unallocated NVM Capacity (UNVMCAP) field of the Identify Controller

data structure is increased by the value that was indicated by the Total Endurance Group Capacity
(TEGCAP) field of the Endurance Group Information log page of the deleted Endurance Group.


If any of the entities modified by the above sequence are accessed after the sequence begins and before
it completes, then the results are indeterminate.


If an NVM Set is created, then the controller performs the following actions as an atomic operation:


a) the NVM Set Identifier is added to the NVM Set List; and
b) the Unallocated Endurance Group Capacity indicated by the Endurance Group Information log

page (refer to Figure 219) is decreased by the amount of capacity allocated to the NVM Set; the
controller may allocate NVM capacity in units such that the requested size for an NVM Set may be
rounded up to the next unit boundary.


487


NVM Express [®] Base Specification, Revision 2.2


If an NVM Set is deleted, then the following actions are performed in sequence:


1) the NVM Set Identifier is removed from the NVM Set List;
2) if the Media Unit Status log page is supported, then the NVM Set Identifier field is cleared to 0h in

all Media Unit Status Descriptors, if any, that indicated the deleted NVM Set;
3) for each namespace in the deleted NVM Set:


a. all commands targeting the namespace are handled as described for namespace deletion

in section 8.1.15;
b. the namespace identifier is removed from the Allocated Namespace ID list;
c. the namespace is deleted;
d. for each controller to which the namespace was attached when that namespace was

deleted:


i. the namespace identifier is added to the Changed Attached Namespace List log

page for that controller; and
ii. an Attached Namespace Attribute Changed asynchronous event is generated by

that controller as described in section 8.1.15.2;


e. the namespace identifier is added to the Changed Allocated Namespace List log page for

each controller in the NVM subsystem; and
f. an Allocated Namespace Attribute Changed asynchronous event is generated for each
controller that has Allocated Namespace Attribute Notices enabled as described in section
8.1.15.2;
and


4) the Unallocated Endurance Group Capacity indicated by the Endurance Group Information log

page is increased by the amount of capacity formerly allocated to the NVM Set.


If any of the entities modified by the above sequence are accessed after the sequence begins and before
it completes, then the results are indeterminate.


If an NVM Set is created or deleted, the value indicated by the Unallocated NVM Capacity (UNVMCAP)
field of the Identify Controller data structure is not changed.


**Fixed Capacity Management**


A Media Unit represents a component of the underlying media in a domain. An implementation may choose
to represent each die as a separate Media Unit; however, this is not required. A Media Unit is the smallest
media component for which the controller reports wear information (refer to the Available Spare field and
the Percentage Used field in the Media Unit Status Descriptor, Figure 256).


Two or more I/O operations to a Media Unit at the same time may interfere with each other as they contend
for resources internal to or shared by that Media Unit.


A controller supporting Fixed Capacity Management:


a) shall support the Media Unit Status log page (refer to section 5.1.12.1.16);
b) shall support Endurance Groups (refer to section 3.2.3);
c) may support NVM Sets (refer to section 3.2.2);
d) shall set the Fixed Capacity Management bit to ‘1’ in the CTRATT field of the Identify Controller

data structure (refer to Figure 313);
e) shall support the Supported Capacity Configuration List log page (refer to section 5.1.12.1.17); and
f) shall support the Select Capacity Configuration operation of the Capacity Management command
(refer to section 5.1.3).


Media Units are accessed by way of Channels that represent communication pathways that may be a
source of contention. This information is reported to facilitate the composition of NVM Sets that minimize
interference between independent writers competing for this type of resource.


The host allocates the Media Units in a domain to Endurance Groups and NVM Sets by:


488


NVM Express [®] Base Specification, Revision 2.2


1) reading the Supported Capacity Configuration List log page (refer to Figure 257) and selecting the

desired configuration; and
2) issuing a Capacity Management command specifying the Select Capacity Configuration operation

and the Capacity Configuration Identifier of the desired configuration.


Following successful completion of the command, each Media Unit is allocated to one Endurance Group
and to one NVM Set. The resulting configuration of Media Units is reported by the Media Unit Status log
page (refer to section 5.1.12.1.16).


**Variable Capacity Management**


Variable Capacity Management allows the dynamic creation and deletion of Endurance Groups and NVM
Sets.


A controller supporting Variable Capacity Management:


a) may support the Media Unit Status log page;
b) shall support Endurance Groups;
c) may support NVM Sets;
d) shall set the Variable Capacity Management bit to ‘1’ in the CTRATT field of the Identify Controller

data structure (refer to Figure 313);
e) shall support the Create Endurance Group operation of the Capacity Management command;
f) may support the Delete Endurance Group operation of the Capacity Management command; and
g) if NVM Sets are supported:


a. shall support the Create NVM Set operation of the Capacity Management command;
b. shall report non-zero values in the Total Endurance Group Capacity field and the

Unallocated Endurance Group Capacity field in the Endurance Group Information log page
(refer to Figure 219); and
c. may support the Delete NVM Set operation of the Capacity Management command.


If a controller supports the Delete Endurance Group operation of the Capacity Management command,
then it shall set the Delete Endurance Group bit to ‘1’ in the CTRATT field of the Identify Controller data
structure.


If a controller supports the Delete NVM Set operation of the Capacity Management command, then it shall
set the Delete NVM Set bit to ‘1’ in the CTRATT field of the Identify Controller data structure.


A typical sequence of operations for allocating capacity is:


1) determine the available capacities in each domain (refer to section 3.2.5);
2) create Endurance Group with desired capacity (refer to section 5.1.3);
3) create NVM Set with desired capacity in the Endurance Group (refer to section 5.1.3); and
4) create namespace with desired capacity in the NVM Set (refer to section 5.1.21).


A typical sequence of operations for deallocating capacity is:


1) delete namespace that contains formatted storage, if any, (refer to section 5.1.21);
2) delete NVM Set, if any, (refer to section 5.1.30); and
3) delete Endurance Group (refer to section 5.1.3).


If there is insufficient unallocated capacity in an Endurance Group for the controller to create an NVM Set,
then the host can delete one or more NVM Sets in that Endurance Group and create the new NVM Set
using some or all of the available capacity.


If there is insufficient unallocated capacity in a domain for the controller to create an Endurance Group,
then the host can delete one or more Endurance Groups in that domain and create a new Endurance Group
using some or all of the available capacity.


489


NVM Express [®] Base Specification, Revision 2.2


**Command and Feature Lockdown**


The Command and Feature Lockdown capability is used to prohibit the execution of commands submitted
to NVM Express controllers and/or Management Endpoints in an NVM subsystem. Within this feature,
commands and Feature Identifiers are defined with the following scopes:

   - Admin Command Set commands defined by the Opcode field;

   - Set Features command features defined by the Feature Identifier field;

   - Management Interface Command Set commands defined by the Opcode field (refer to the NVM
Express Management Interface Specification); and

   - PCIe Command Set commands defined by the Opcode field (refer to the NVM Express
Management Interface Specification).


Admin Command Set commands and Feature Identifiers are defined to be prohibitable by this feature,
however it is vendor specific which of the Command Set commands and Feature Identifiers are prohibitable
from execution, including the Lockdown command itself.


The prohibition of commands or Feature Identifiers on an interface is specified in the Interface field of the
Lockdown command (refer to section 5.1.15). The prohibition applies to all applicable:

   - NVM Express controllers; and

   - Management Endpoints,


in the NVM subsystem, as specified in the Interface field.


The Lockdown command is used to specify commands that are prohibited from execution (i.e., locked
down) and may be used further to then again allow that command to be executed.


The prohibiting of execution of a command as part of this feature shall persist until:


a) power cycle of the NVM subsystem; or
b) further being allowed by a follow-on Lockdown command.


If a prohibited Admin Command Set command or Feature Identifier is processed by a controller in the NVM
subsystem, then that command shall be aborted with a status code of Command Prohibited by Command
and Feature Lockdown.


If a prohibited Management Interface Command Set command or PCIe Command Set command is
processed by a management endpoint in the NVM subsystem, then that command shall be aborted and
send a Response Message with an Access Denied Error Response (refer to the NVM Express Management
Interface Specification).


The prohibition or allowance of the execution of a command is based on the interface on which the
command is received (i.e., the Admin Submission Queue, or an out-of-band Management Endpoint). For
example, a command is able to be prohibited if received on an Admin Submission Queue but allowed if
received on an out-of-band Management Endpoint, if supported. The Interface field in the Lockdown
command (refer to 5.1.15) is used to specify this behavior.


A host may use the Command and Feature Lockdown log page (refer to section 5.1.12.1.20) to determine
the commands and Feature Identifiers that are allowed to be prohibited from execution. A Get Log Page
command specifying the Command and Feature Lockdown log page returns a list of Admin command
opcodes or Feature Identifiers depending on the scope specified in the Get Log Page command. The
returned list of opcodes or Feature Identifiers are the opcodes or Feature Identifiers that are:


a) supported as being prohibitable from execution using the Lockdown command;
b) currently prohibited from execution if received on an Admin Submission Queue; or
c) currently prohibited from execution if received out-of-band on a Management Endpoint.


If the Command and Feature Lockdown capability is supported (i.e., the CFLS bit in the OACS field in
Figure 313 is set to ‘1’), then the controller shall support the Lockdown command and the Command and
Feature Lockdown log page.


490


NVM Express [®] Base Specification, Revision 2.2


**Controller Data Queue**


A Controller Data Queue (CDQ) is used to post information from the controller to the host that is specific to
the type of queue being created (refer to Figure 166) by the Controller Data Queue command that specifies
the Create Controller Data Queue management operation (refer to section 5.1.4.1.1). A CDQ is a circular
buffer with a fixed slot size with entries posted by a controller.


A CDQ is deleted:

  - by a Controller Data Queue command that specifies the Delete Controller Data Queue
management operation (refer to section 5.1.4.1.2);

  - on a Controller Level Reset on the controller that processed the Controller Data Queue command
that created the CDQ; or

  - by a Migration Send command that specifies the Suspend management operation and the Delete
User Data Migration Queue (DUDMQ) bit is set to ‘1’ (refer to section 5.1.17.1.1).


On the successful completion of a Controller Data Queue command, a Controller Data Queue Identifier
(CDQID) is returned in the completion queue entry (refer to Figure 169). A CDQID is used to identify the
created Controller Data Queue on the controller that processed the command. The returned value for that
CDQID is any value except the CDQID values for any Controller Data Queue that exists on the controller
that processed the command (i.e., a controller is permitted to return the value of a CDQID value of a
Controller Data Queue that was previously deleted). The scope of a CDQID is per controller.


The CDQ Head pointer is updated by the host by issuing a Set Features command specifying the Controller
Data Queue feature and the Controller Data Queue Identifier (refer to section 5.1.25.1.23) after processing
an entry indicating the last free CDQ slot. A Controller Data Queue Phase Tag (CDQP) bit is defined in the
CDQ entry (refer to the applicable I/O command set specification) to indicate whether an entry has been
newly posted without the host relying on the Controller Data Queue Tail Pointer event (refer to Figure 155).
The Controller Data Queue Phase Tag bit enables the host to determine whether entries are new or not.


**Controller Data Queue Usage**


The controller uses the current Tail entry pointer to identify the next open CDQ slot. The controller
increments the Tail entry pointer after placing the new entry to the next open CDQ slot. If the Tail entry
pointer increment exceeds the CDQ size, then the Tail entry pointer shall roll to zero. The controller may
continue to place entries in free CDQ slots as long as the Full queue condition is not met (refer to section
3.3.1.5). The controller shall take CDQ wrap conditions into account.


The host uses the current Head entry pointer to identify the slot containing the next entry to be consumed.
The host increments the Head entry pointer after consuming the next entry from the CDQ. If the Head entry
pointer increment exceeds the CDQ size, the Head entry pointer shall roll to zero. The host may continue
to consume entries from the CDQ as long as the Empty queue condition is not met (refer to section 3.3.1.4).


Note: The host shall take CDQ wrap conditions into account.


A host issues a Set Features command specifying the Controller Data Queue feature to communicate a
new value of the Head entry pointer to the controller. If the host specifies an invalid value to the Head entry
pointer, then that Set Features command is aborted. This condition may be caused by a host attempting to
remove an entry from an empty CDQ.


A host checks a posted entries Controller Data Queue Phase Tag (CDQP) bits in memory to determine
whether new CDQ entries have been posted (refer to section 8.1.6.2). The CDQ Tail pointer is only used
internally by the controller and is not visible to the host.


An entry is posted to the CDQ when the controller write of that entry to the next free CDQ slot inverts the
Controller Data Queue Phase Tag (CDQP) bit from its previous value in memory (refer to section 8.1.6.2).
The controller generates a Controller Data Queue Tail Pointer event (refer to Figure 155) to the host to
indicate that the CDQ slot specified by the host in the Controller Data Queue feature (refer to section
5.1.25.1.23) has been posted if in the Controller Data Queue feature associated with the CDQ:

  - the Tail pointer value matches the value in the Tail Pointer Trigger (TPT) field; and


491


NVM Express [®] Base Specification, Revision 2.2


  - the Enable Tail Pointer Trigger (ETPT) bit is set to ‘1’.


A CDQ entry has been consumed by the host when the host submits a Set Features command specifying
the Controller Data Queue feature with a new value that indicates that the CDQ Head Pointer has moved
past the slot in which that CDQ entry was placed. A Set Features command specifying the Controller Data
Queue feature may indicate that one or more CDQ entries have been consumed.


Altering a CDQ entry after that entry has been posted but before that entry has been consumed results in
undefined behavior.


Refer to the specific type of CDQ to determine the behavior of a CDQ that has become full.


Refer to section 3.3.1.4 for the definition of an empty CDQ. Refer to section 3.3.1.5 for the definition of a
full CDQ.


If a CQD entry is constructed via multiple writes, the Controller Data Queue Phase Tag (CDQP) bit shall be
updated in the last write of that CDQ entry.


Refer to the applicable I/O Command Set specifications for any specific requirements on the use of CDQs


**Controller Data Queue Phase Tag**


The Controller Data Queue Phase Tag (CDQP) bit indicates whether a CDQ entry is new. The CDQP bit
for each CDQ entry in the CDQ shall be initialized to ‘0’ by the host before creating the CDQ by submitting
a Controller Data Queue command (refer to section 5.1.4) specifying the Create Queue management
operation (refer to section 5.1.4.1.1).


When the controller posts a new CDQ entry to the CDQ, the controller shall invert the CDQP bit in that CDQ
entry (i.e., the inverting of the CDQP bit enables the host to detect the new CDQ entry).


When a CDQ entry is posted to a CDQ slot in the CDQ for the first time after the CDQ is created, the CDQP
bit for that completion queue entry is set to ‘1’.


This continues for each CDQ entry that is posted until the controller posts a CDQ entry to the highest
numbered CDQ slot and wraps to CDQ slot number 0 as described in section 8.1.6.1. When that CDQ wrap
condition occurs, the CDQP bit is then cleared to ‘0’ in each CDQ entry that is posted. This continues until
another CDQ wrap condition occurs. Each time a CDQ wrap condition occurs, the value of the CDQP bit is
inverted (i.e., changes from ‘1’ to ‘0’ or changes from ‘0’ to ‘1’).


**Device Self-test Operations**


A device self-test operation is a diagnostic testing sequence that tests the integrity and functionality of the
controller and may include testing of the media associated with namespaces or refresh operations. The
operation is broken down into a series of segments, where each segment is a set of vendor specific tests
or refresh operations. The segment number in the Self-test Result data structure (refer to section 5.1.12.1.7)
is used for reporting purposes to indicate where a test failed, if any. The test performed in each segment
may be the same for the short device self-test operation and the extended device self-test operation.


A device self-test operation is performed in the background allowing concurrent processing of some
commands and requiring suspension of the device self-test operation to process other commands. Which
commands may be processed concurrently versus require suspension of the device self-test operation is
vendor specific.


If the controller receives any command that requires suspension of the device self-test operation to process
and complete, then the controller shall:


1) suspend the device self-test operation;
2) process and complete that command; and
3) resume the device self-test operation.


During a device self-test operation, the performance of the NVM subsystem may be degraded (e.g.,
controllers not performing the device self-test operation may also experience degraded performance).


The following device self-test operations are defined:


492


NVM Express [®] Base Specification, Revision 2.2


a) short device self-test operation (refer to section 8.1.7.1);
b) extended device self-test operation (refer to section 8.1.7.2); and
c) Host-Initiated Refresh operation (refer to section 8.1.11).


Figure 596 is an informative example of a device self-test operation with the associated segments and tests
performed in each segment.


**Figure 596: Example Device Self-test Operation (Informative)**



















|Segment|Col2|Test Performed|Failure Criteria|
|---|---|---|---|
|1 – RAM Check|1 – RAM Check|Write a test pattern to RAM, followed by a read and compare<br>of the original data.|Any uncorrectable error or<br>data miscompare|
|2 – SMART Check|2 – SMART Check|Check SMART or health status for Critical Warning bits set<br>to ‘1’ in SMART / Health Information Log.|Any Critical Warning bit set to<br>‘1’ fails this segment|
|3 – Volatile memory<br>backup|3 – Volatile memory<br>backup|Validate volatile memory backup solution health (e.g.,<br>measure backup power source charge and/or discharge<br>time).|Significant<br>degradation<br>in<br>backup capability|
|4 – Metadata validation|4 – Metadata validation|Confirm/validate all copies of metadata.|Metadata is corrupt and is not<br>recoverable|
|5 – NVM integrity|5 – NVM integrity|Write/read/compare to reserved areas of each NVM. Ensure<br>also that every read/write channel of the controller is<br>exercised.|Data miscompare|
|Extended only|6 – Data Integrity|Perform background housekeeping tasks, prioritizing<br>actions that enhance the integrity of stored data.<br>Exit this segment in time to complete the remaining<br>segments and meet the timing requirements for extended<br>device self-test operation indicated in the Identify Controller<br>data structure.|Metadata is corrupt and is not<br>recoverable|
|7 – Media Check|7 – Media Check|Perform random reads from every available good physical<br>block.<br>Exit this segment in time to complete the remaining<br>segments. The time to complete is dependent on the type of<br>device self-test operation.|Inability to access a physical<br>block|
|8 – Drive Life|8 – Drive Life|End-of-life condition: Assess the drive’s suitability for<br>continuing write operations.|The Percentage Used is set to<br>255 in the SMART / Health<br>Information Log or an analysis<br>of<br>internal<br>key<br>operating<br>parameters indicates that data<br>is at risk if writing continues|
|9 – SMART Check|9 – SMART Check|Same as 2 – SMART Check|Same as 2 – SMART Check|


**Short Device Self-Test Operation**


A short device self-test operation should complete in two minutes or less. The percentage complete of the
short device self-test operation is indicated in the Current Percentage Complete field in the Device Self-test
log page (refer to section 5.1.12.1.7).


A short device self-test operation:


a) shall be aborted by any Controller Level Reset that affects the controller on which the device self
test is being performed;
b) shall be aborted by a Format NVM command as described in Figure 597;
c) shall be aborted when a sanitize operation is started (refer to section 5.1.22);
d) shall be aborted if a Device Self-test command with the Self-Test Code field set to Fh is processed;

and
e) may be aborted if the specified namespace is removed from the namespace inventory.


493


NVM Express [®] Base Specification, Revision 2.2


**Figure 597: Format NVM command Aborting a Device Self-Test Operation**






























|SES|FNS Bit|SENS Bit|NSID in Format NVM<br>command|NSID in Device Self-test<br>command|Abort Device<br>Self-Test<br>operation?|
|---|---|---|---|---|---|
|000b<br>(i.e.,<br>not a<br>secure<br>erase)|0|N/A|Any allocated NSID value<br>(refer to section 3.2.1.3)|Any active NSID value<br>(refer to section 3.2.1.4)|Yes, if the NSID<br>values are the<br>same|
|000b<br>(i.e.,<br>not a<br>secure<br>erase)|0|0|FFFFFFFFh|Any active NSID value<br>(refer to section 3.2.1.4)|Yes|
|000b<br>(i.e.,<br>not a<br>secure<br>erase)|0|0|Any allocated NSID value<br>(refer to section 3.2.1.3)|FFFFFFFFh|Optional|
|000b<br>(i.e.,<br>not a<br>secure<br>erase)|0|0|FFFFFFFFh|FFFFFFFFh|Yes|
|000b<br>(i.e.,<br>not a<br>secure<br>erase)|1|1|Ignored|Ignored|Yes|
|001b<br>or<br>010b<br>(i.e.,<br>secure<br>erase)|N/A|0|Any allocated NSID value<br>(refer to section 3.2.1.3)|Any active NSID value<br>(refer to section 3.2.1.4|Yes, if the NSID<br>values are the<br>same|
|001b<br>or<br>010b<br>(i.e.,<br>secure<br>erase)|N/A|0|FFFFFFFFh|Any active NSID value<br>(refer to section 3.2.1.4)|Yes|
|001b<br>or<br>010b<br>(i.e.,<br>secure<br>erase)|N/A|0|Any allocated NSID value<br>(refer to section 3.2.1.3|FFFFFFFFh|Optional|
|001b<br>or<br>010b<br>(i.e.,<br>secure<br>erase)|N/A|0|FFFFFFFFh|FFFFFFFFh|Yes|
|001b<br>or<br>010b<br>(i.e.,<br>secure<br>erase)|N/A|1|Ignored|Ignored|Yes|
|Key:<br>Optional = The device self-test operation is not required to be aborted but may be aborted.|Key:<br>Optional = The device self-test operation is not required to be aborted but may be aborted.|Key:<br>Optional = The device self-test operation is not required to be aborted but may be aborted.|Key:<br>Optional = The device self-test operation is not required to be aborted but may be aborted.|Key:<br>Optional = The device self-test operation is not required to be aborted but may be aborted.|Key:<br>Optional = The device self-test operation is not required to be aborted but may be aborted.|



**Extended Device Self-Test Operation**


An extended device self-test operation should complete in the time indicated in the Extended Device Selftest Time field in the Identify Controller data structure or less. The percentage complete of the extended
device self-test operation is indicated in the Current Percentage Complete field in the Device Self-test log
page (refer to section 5.1.12.1.7).


An extended device self-test operation shall persist across any Controller Level Reset and shall resume
after completion of the reset or any restoration of power, if any. The segment where the extended device
self-test operation resumes is vendor specific, but implementations should only have to perform tests again
within the last segment that was being tested prior to the reset.


An extended device self-test operation:


a) shall be aborted by a Format NVM command as described in Figure 597;
b) shall be aborted when a sanitize operation is started (refer to section 5.1.22);
c) shall be aborted if a Device Self-test command with the Self-Test Code field set to Fh is processed;

and
d) may be aborted if the specified namespace is removed from the namespace inventory.


**Directives**


Directives is a mechanism to enable host and NVM subsystem or controller information exchange. The
Directive Receive command (refer to section 5.1.6) is used to transfer data related to a specific Directive
Type from the controller to the host. The Directive Send command (refer to section 5.1.7) is used to transfer
data related to a specific Directive Type from the host to the controller. Other commands may include a
Directive Specific value specific for a given Directive Type (e.g., the Write command in the NVM Command
Set).


Support for Directives is optional and is indicated by the Directives Supported (DIRS) bit in the Optional
Admin Command Support (OACS) field in the Identify Controller data structure (refer to Figure 313).


494


NVM Express [®] Base Specification, Revision 2.2


If a controller supports Directives, then the controller shall:

   - Indicate support for Directives in the Optional Admin Command Support (OACS) field by setting
the DIRS bit to ‘1’ in the Identify Controller data structure;

   - Support the Directive Receive command;

   - Support the Directive Send command; and

   - Support the Identify Directive (i.e., Type 00h).


The Directive Types that may be supported by a controller are defined in Figure 598.


The Directive Specific field and Directive Operation field are dependent on the Directive Type specified in
the command (e.g., Directive Send, Directive Receive, or I/O command).


**Figure 598: Directive Types**

|Directive|Directive Type Value|Reference|I/O Command Directive|
|---|---|---|---|
|Identify|00h|8.1.8.2|No|
|Streams|01h|8.1.8.3|Yes|
|Data Placement|02h|8.1.8.4|Yes|
|Vendor Specific|0Fh||Yes|



If a Directive is not supported or is supported and disabled, then all Directive Send commands and Directive
Receive commands with that Directive Type shall be aborted with a status code of Invalid Field in
Command.


Support for a specific Directive Type is indicated using the Return Parameters operation of the Identify
Directive. A specific Directive may be enabled or disabled using the Enable operation of the Identify
Directive. Before using a specific Directive, the host should determine if that Directive is supported and
should enable that Directive using the Identify Directive.


**Directive Use in I/O Commands**


I/O Command Directives are the subset of Directive Types that may be used as part of I/O commands. For
example, a Write command in the NVM Command Set may specify a Directive Type and an associated
Directive Specific value. I/O Command Directives shall have a Directive Type value that is less than or
equal to 0Fh due to the size of the Directive Type field in I/O commands. When a Directive Type is specified
in an I/O command, the most significant four bits are assumed to be 0h. A Directive Type of 00h in an I/O
command specifies that the I/O command is not using Directives.


In an I/O command, if the Directive Type (DTYPE) field is set to an I/O Command Directive, then the
Directive Specific (DSPEC) field includes additional information for the associated I/O command (refer to
Figure 599).


**Figure 599: Directive Specific Field Interpretation**

|Directive Type Value|Directive Specific Field Definition|
|---|---|
|00h (Directives not in use)|Field not used.|
|01h (Streams)|Specifies the identifier of the stream associated with the data.|
|02h (Data Placement)|Specifies the Placement Identifier used to determine where to write the user data<br>within non-volatile storage (refer to Figure 283 and Figure 284) of the Endurance<br>Group associated with the namespace.|
|03h to 0Eh|Reserved|
|0Fh (Vendor Specific)|Vendor specific|



In an I/O command:

  - if no I/O Command Directive is enabled or the DTYPE field is cleared to 00h, then the DTYPE field
and the DSPEC field are ignored; and


495


NVM Express [®] Base Specification, Revision 2.2


  - if one or more I/O Command Directives is enabled and the DTYPE field is set to a value that is not
supported or not enabled, then the controller shall abort the command with a status code of Invalid
Field in Command **.**


For the Streams Directive (i.e., DTYPE field set to 01h), if the DSPEC field is cleared to 0h in an I/O
command that supports the Streams Directive, then that I/O command shall be processed normally (i.e., as
if DTYPE field is cleared to 00h).


**Identify (Directive Type 00h)**


The Identify Directive is used to determine the Directive Types that the controller supports and to enable
use of the supported Directives. If Directives are supported, then this Directive Type shall be supported.


The Directive operations that shall be supported for the Identify Directive are listed in Figure 600.


**Figure 600: Identify Directive – Directive Operations**

|Directive Command|Directive Operation Name|Directive Operation Value|Reference|
|---|---|---|---|
|Directive Receive|Return Parameters|01h|8.1.8.2.1.1|
|Directive Receive|Reserved|All other values||
|Directive Send|Enable Directive|01h|8.1.8.2.2.1|
|Directive Send|Reserved|All other values||



**8.1.8.2.1** **Directive Receive**


This section defines operations used with the Directive Receive command for the Identify Directive.


**Return Parameters (Directive Operation 01h)**


This operation returns a data structure that contains a bit vector specifying the Directive Types supported
by the controller and a bit vector specifying the Directive Types enabled for the namespace. The data
structure returned is defined in Figure 601. If an NSID value of FFFFFFFFh is specified, then the controller
shall abort the command with a status code of Invalid Field in Command. The DSPEC field in command
Dword 11 is not used for this operation.


**Figure 601: Identify Directive – Return Parameters Data Structure**





|Bytes|Bits|Description|
|---|---|---|
|**Directives Supported**|**Directives Supported**|**Directives Supported**|
|31:00|255:16|Reserved|
|31:00|15|**Vendor Specific Directive (VSDIRS):** This bit is set to ‘1’ if the Vendor Specific Directive<br>is supported. This bit is cleared to ‘0’ if the Vendor Specific Directive is not supported.|
|31:00|14:03|Reserved|
|31:00|02|**Data Placement Directive (DPDIRS):**This bit is set to ‘1’ if the Data Placement Directive<br>is supported. This bit is cleared to ‘0’ if the Data Placement Directive is not supported.|
|31:00|01|**Streams Directive (SDIRS):**This bit is set to ‘1’ if the Streams Directive is supported. This<br>bit is cleared to ‘0’ if the Streams Directive is not supported.|
|31:00|00|**Identify Directive (IDIRS):**This bit shall be set to ‘1’ to indicate that the Identify Directive<br>is supported.|
|**Directives Enabled**|**Directives Enabled**|**Directives Enabled**|
|63:32|255:16|Reserved|
|63:32|15|**Vendor Specific Directive (VSDIRE):** This bit is set to ‘1’ if the Vendor Specific Directive<br>is enabled. This bit is cleared to ‘0’ if the Vendor Specific Directive is not enabled.|
|63:32|14:03|Reserved|
|63:32|02|**Data Placement Directive (DPDIRE):**This bit is set to ‘1’ if the Data Placement Directive<br>is enabled. This bit is cleared to ‘0’ if the Data Placement Directive is not enabled.|
|63:32|01|**Streams Directive (SDIRE):**This bit is set to ‘1’ if the Streams Directive is enabled. This<br>bit is cleared to ‘0’ if the Streams Directive is not enabled.|
|63:32|00|**Identify Directive (IDIRE):**This bit shall be set to ‘1’ to indicate that the Identify Directive<br>is enabled.|


496


NVM Express [®] Base Specification, Revision 2.2


**Figure 601: Identify Directive – Return Parameters Data Structure**















|Bytes|Bits|Description|
|---|---|---|
|**Directive Persistent Across Controller Level Resets**|**Directive Persistent Across Controller Level Resets**|**Directive Persistent Across Controller Level Resets**|
|95:64|255:16|Reserved|
|95:64|15|**Vendor Specific Directive (VSDIRCLR):** If the Vendor Specific Directive is supported,<br>then this bit is:<br>• <br>set to ‘1’ to indicate that the host specified Data Placement Directive state is<br>preserved across Controller Level Resets; or<br>• <br>cleared to ‘0’ to indicate that the host specified Data Placement Directive state is<br>not preserved across Controller Level Resets.<br>If the Vendor Specific Directive is not supported, then this bit shall be cleared to ‘0’.|
|95:64|14:03|Reserved|
|95:64|02|**Data Placement Directive (DPDIRCLR):**If the Data Placement Directive is supported,<br>then this bit shall be set to ‘1’ to indicate that the host specified Data Placement Directive<br>state is preserved across Controller Level Resets. If the Data Placement Directive is not<br>supported, then this bit shall be cleared to ‘0’.|
|95:64|01|**Streams Directive (SDIRCLR):**This bit shall be cleared to ‘0’ to indicate that the Streams<br>Directive state is not preserved across Controller Level Resets.|
|95:64|00|**Identify Directive (IDIRCLR):**This bit shall be set cleared to ‘0’ as the host is not able to<br>change the state of the Identify Directive.|
|4095:96|n/a|Reserved|


**8.1.8.2.2** **Directive Send**


This section defines operations used with the Directive Send command for the Identify Directive.


**Enable Directive (Directive Operation 01h)**


The Enable Directive operation is used to enable a specific Directive for use within a namespace by all
controllers that are associated with the same Host Identifier. The DSPEC field in command Dword 11 is not
used for this operation. The Identify Directive is always enabled. The enable state of each Directive on each
shared namespace attached to enabled controllers associated with the same non-zero Host Identifier is the
same. If the Directive is not the Data Placement Directive and an NSID value of FFFFFFFFh is specified,
then the Enable Directive operation applies to the NVM subsystem (i.e., all namespaces and all controllers
associated with the NVM subsystem). If the Directive is the Data Placement Directive and an NSID value
of FFFFFFFFh is specified, then the controller shall abort the command with a status code of Invalid
Namespace or Format.


On a Controller Level Reset:

  - all Directives other than the Identify Directive that have the Directive Persistent Across Controller
Level Resets bit cleared to ‘0’ are disabled for that controller; and

  - if there is an enabled controller associated with the Host Identifier for the controller that was reset,
then for namespaces attached to enabled controllers associated with that Host Identifier, Directives
are not disabled.


If a host sets the Host Identifier of a controller to the same non-zero Host Identifier as one or more other
controllers in the NVM subsystem, then setting that Host Identifier shall result in each shared namespace
attached to that controller having the same enable state for each Directive as the enable state for each
Directive for that namespace attached to other controllers associated with that Host Identifier.


If a host enables a controller that has the same non-zero Host Identifier as one or more other controllers in
the NVM subsystem, then enabling that controller shall result in each shared namespace attached to that
controller having the same enable state for each Directive as the enable state for each Directive for that
namespace attached to other controllers associated with that Host Identifier.


For all controllers in an NVM subsystem that have the same non-zero Host Identifier, if a host changes the
enable state of any Directive for a shared namespace attached to a controller by a means other than a


497


NVM Express [®] Base Specification, Revision 2.2


Controller Level Reset, then that change shall be made to the enable state of that Directive for that
namespace attached to any other controller associated with that Host Identifier.


If the Host Identifier value is 0h and the Host Identifier is required to be set to a non-zero value before a
host enables a Directive (i.e., the Directive Type is set to Streams and the SRNZID bit in the NVM
subsystem Stream Capability field (refer to Figure 608) is set to ‘1’) then the Directive Send command shall
be aborted with a status code of Host Identifier Not Initialized.


Refer to the sections defining each Directive Type for restrictions on enabling that directive.


**Figure 602: Enable Directive – Command Dword 12**





|Bits|Description|
|---|---|
|31:16|Reserved|
|15:08|**Directive Type (DTYPE):**This field specifies the Directive Type to enable or disable. If this field specifies<br>the Identify Directive (i.e., 00h), then a status code of Invalid Field in Command shall be returned.|
|07:01|Reserved|
|00|**Enable Directive (ENDIR):**If this bit is set to ‘1’ and the Directive Type is supported, then the Directive<br>is enabled, unless otherwise specified. If this bit is cleared to ‘0’, then the Directive is disabled. If this bit<br>is set to ‘1’ for a Directive that is not supported, then a status code of Invalid Field in Command shall be<br>returned.|


**Figure 603: Enable Directive – Command Specific Status Values**



|Value|Definition|
|---|---|
|7Fh|**Stream Resource Allocation Failed:**The controller failed to enable the Streams Directive for the<br>specified namespace and Host Identifier due to insufficient resources.|


**Streams (Directive Type 01h, Optional)**


The Streams Directive enables the host to indicate (i.e., by using the stream identifier) to the controller that
the specified user data in a User Data Out command (e.g., logical blocks in a write command) are part of
one group of associated data. This information may be used by the controller to store related data in
associated locations or for other performance enhancements.


The controller provides information in response to the Return Parameters operation about the configuration
of the controller that indicates Stream Write Size, Stream Granularity Size, and stream resources at the
NVM subsystem and namespace levels.


Data that is aligned to and in multiples of the Stream Write Size (SWS) provides optimal performance of
the write commands to the controller. The SWS unit of granularity is defined independently for each I/O
Command Set. The Stream Granularity Size indicates the size of the media that is prepared as a unit for
future allocation for write commands and is a multiple of the Stream Write Size. The controller may allocate
and group together a stream in Stream Granularity Size (SGS) units. Refer to Figure 604.


**Figure 604: Directive Streams – Stream Alignment and Granularity**



SWS
(first)



SWS
... (last)



Stream Granularity (SGS)

|Col1|SGS (first)|...|SGS (last)|Col5|
|---|---|---|---|---|
||Complete Stream|Complete Stream|Complete Stream|Complete Stream|



One example of this is if the host issues an NVM Command Set Dataset Management command (refer to
the Dataset Management command section of the NVM Command Set Specification) to deallocate logical
blocks that are associated with a stream, that host should specify a starting LBA and length that is aligned


498


NVM Express [®] Base Specification, Revision 2.2


to and in multiples of the Stream Granularity Size. This provides optimal performance and endurance of the
media.


Stream resources are the resources in the NVM subsystem that are necessary to track operations
associated with a specified stream identifier. There are a maximum number of stream resources that are
available in an NVM subsystem as indicated by the Max Stream Limit (MSL) field in the Return Parameters
data structure (refer to Figure 608).


Available NVM subsystem stream resources are stream resources that are not allocated for exclusive use
in any namespace. Available NVM subsystem stream resources are reported in the NVM Subsystem
Streams Available (NSSA) field (refer to Figure 608) and may be used by any host in any namespace that:

  - has the Streams Directive enabled;

  - has not been allocated exclusive stream resources by that host if the Shared Stream Identifiers
(SSID) bit is cleared to ‘0’ in the NSSC field; and

  - has not been allocated exclusive stream resources by any host if the SSID bit is set to ‘1’.


Each time stream resources are allocated for exclusive use in a specified namespace, the available NVM
subsystem stream resources reported in the NSSA field are reduced.


For a given namespace:


a) a host allocates stream resources to that namespace for the exclusive use of that host(s) by issuing

the Allocate Resources operation;
b) other hosts may concurrently allocate stream resources to that namespace for their exclusive use;

and
c) hosts which have not allocated stream resources to that namespace may use available NVM

subsystem stream resources for access to that namespace.


If an NVM subsystem has streams resources allocated to a host with a Host Identifier value of 0h and the
Host Identifier is subsequently changed to a non-zero value, then those streams resources remain
associated with the Host with a Host Identifier value of 0h and are not associated with the host with the
non-zero Host Identifier.


The Directive operations that shall be supported if the Streams Directive is supported are listed in Figure
605. The Directive Specific field in a command is referred to as the Stream Identifier when the Directive
Type field is set to the Streams Directive.


**Figure 605: Streams – Directive Operations**










|Directive<br>Command|Directive Operation<br>Name|Directive Operation<br>Value|Reference|
|---|---|---|---|
|Directive Receive|Return Parameters|01h|8.1.8.3.1.1|
|Directive Receive|Get Status|02h|8.1.8.3.1.2|
|Directive Receive|Allocate Resources|03h|8.1.8.3.1.3|
|Directive Receive|Reserved|All other values||
|Directive Send|Release Identifier|01h|8.1.8.3.2.1|
|Directive Send|Release Resources|02h|8.1.8.3.2.2|
|Directive Send|Reserved|All other values||



Stream identifiers are assigned by the host and may be in the range 0001h to FFFFh. The host may specify
a sparse set of stream identifiers (i.e., there is no requirement for the host to use Stream Identifiers in any
particular order).


The host may access a namespace through multiple controllers in the NVM subsystem. The controllers in
an NVM subsystem indicate in the SSID bit (refer to Figure 608) if a stream identifier is unique based on
the Host Identifier (i.e., the same stream identifier used to access the same namespace by a host that has
registered a different Host Identifier is referencing a different stream), or if a stream identifier may be used
by multiple Host Identifiers (i.e., the same stream identifier used to access the same namespace by a host


499


NVM Express [®] Base Specification, Revision 2.2


that has registered a different Host Identifier is referencing the same stream). All controllers in an NVM
subsystem shall report the same value in the NSSC field.


If multiple controllers receive a registration of a Host Identifier (refer to section 5.1.25.1.28) that has the
same non-zero value, then that value represents a single host that is accessing the namespace through
those controllers and a stream identifier is used across those controllers to access the same stream on the
namespace. If a Host Identifier has a unique non-zero value, then each value represents a unique host that
is accessing the namespace and:

  - if the SSID bit is cleared to ‘0’, then the same stream identifier on controllers with different non-zero
Host Identifiers does not have the same meaning for a particular namespace (i.e., the stream
identifier is not used across controllers with different non-zero Host Identifiers to access the same
stream on the namespace); and

  - if the SSID bit is set to ‘1’, then the same stream identifier on any controller with a non-zero Host
Identifier has the same meaning for a particular namespace (i.e., the stream identifier is used
across controllers to access the same stream on the namespace).


If a Host Identifier is cleared to 0h, then a unique host is accessing the namespace and the stream identifier
does not have the same meaning for a particular namespace.


**Figure 606: Example Multi-Stream and NSSC**





























In the example shown in Figure 606, if the SSID bit is cleared to ‘0’, then there are three streams as follows:

  - Stream ID 1-a and Stream ID 1-b have the same meaning;

  - Stream ID 1-c has a different meaning; and

  - Stream ID 1-d has a different meaning.


In the example shown in Figure 606, if the SSID bit is set to ‘1’, then there is one stream as follows:

  - Stream ID 1-a, Stream ID 1-b, Stream ID 1-c, and Stream ID 1-d have the same meaning.


The controller(s) recognized by the NVM subsystem as being associated with a specific host or hosts and
attached to a specific namespace either:

  - utilizes a number of stream resources allocated for exclusive use of that namespace as returned
in response to an Allocate Resources operation; or


500


NVM Express [®] Base Specification, Revision 2.2


  - utilizes resources from the NVM subsystem stream resources.


The value of Namespace Streams Allocated (NSA) indicates how many resources for individual stream
identifiers have been allocated for exclusive use for the specified namespace by the associated controllers.
This indicates the maximum number of stream identifiers that may be open at any given time in the specified
namespace by the associated controllers. To request a different number of resources than are currently
allocated for exclusive use by the associated controllers for a specific namespace, all currently allocated
resources are first required to be released using the Release Resources operation. There is no mechanism
to incrementally increase or decrease the number of allocated resources for a given namespace.


Streams are opened by the controller when the host issues a Write command that specifies a stream
identifier that is not currently open. While a stream is open the controller maintains context for that stream
(e.g., buffers for associated data). The host may determine the streams that are open using the Get Status
operation.


For a namespace that has a non-zero value of Namespace Streams Allocated (NSA), if the host submits a
Write command specifying a stream identifier not currently in use and stream resources are exhausted,
then an arbitrary stream identifier for that namespace is released by the controller to free the stream
resources associated with that stream identifier for the new stream. The host may ensure the number of
open streams does not exceed the allocated stream resources for the namespace by explicitly releasing
stream identifiers as necessary using the Release Identifier operation.


For a namespace that has zero namespace stream resources allocated, if the host submits an I/O command
specifying a stream identifier not currently in use and:

  - NVM subsystem streams available are exhausted, then an arbitrary stream identifier for an arbitrary
namespace that is using NVM subsystem stream resources is released by the NVM subsystem to
free the stream resources associated with that stream identifier for the new stream; or

  - all NVM subsystem stream resources have been allocated for exclusive use for specific
namespaces, then the Write command is treated as a normal Write command that does not specify
a stream identifier.


The host determines parameters associated with stream resources using the Return Parameters operation.
The host may get a list of open stream identifiers using the Get Status operation.


If the Streams Directive becomes disabled for use by a host within a namespace, then all stream resources
and stream identifiers shall be released for that host for the affected namespace. If the host issues a Format
NVM command, then all stream identifiers for all open streams for affected namespaces shall be released.
If the host deletes a namespace, then all stream resources and all stream identifiers for that namespace
shall be released. If the write protection state of a namespace changes such that the namespace becomes
write protected (refer to section 8.1.16), then the controller shall release all stream resources and stream
identifiers for that namespace.


Streams Directive defines the command specific status values specified in Figure 607.


**Figure 607: Streams Directive – Command Specific Status Values**

|Value|Definition|
|---|---|
|7Fh|**Stream Resource Allocation Failed:**The controller was not able to allocate stream resources for<br>exclusive use of the specified namespace and no NVM subsystem stream resources are available.|



The Streams Directive is not allowed to be enabled in any namespace that is contained in an Endurance
Group with Flexible Data Placement enabled. If the specified namespace is contained in an Endurance
Group that has Flexible Data Placement enabled, then the controller shall not enable the Streams Directive.
If:

  - a Directive Send command specifies the Streams Directive in the DTYPE field and the Directive
Operation field is set to 01h (i.e., Enable Directive); and

  - the namespace specified by the NSID field is contained in an Endurance Group that has Flexible
Data Placement enabled,


501


NVM Express [®] Base Specification, Revision 2.2


then the controller shall:

  - abort that Directive Send command with a status code of Invalid Field in Command; and

  - indicate the Directive Operation field in the Parameter Error Location field (refer to Figure 206) if
an entry is added to the Error Information log page due to aborting that Directive Send command.


**8.1.8.3.1** **Directive Receive**


This section defines operations used with the Directive Receive command for the Streams Directive.


**Return Parameters (Directive Operation 01h)**


The Return Parameter operation returns a data structure that specifies the features and capabilities
supported by the Streams Directive, including namespace specific values. The DSPEC field in command
Dword 11 is not used for this operation. The data structure returned is defined in Figure 608. If an NSID
value of FFFFFFFFh is specified, then the controller:

  - returns the NVM subsystem specific values;

  - may return any namespace specific values that are the same for all namespaces (e.g., SWS); and

  - clears all other namespace specific fields to 0h.


**Figure 608: Streams Directive – Return Parameters Data Structure**












|Bits|Description|
|---|---|
|7:2|Reserved|
|1|**Streams Require Non-Zero Host Identifier (SRNZID):**This bit indicates whether the Host<br>Identifier is required to be set to a non-zero value before the Streams Directive is able to be<br>enabled. If this bit is cleared to ‘0’, then the Host Identifier is not required to be set to a non-<br>zero value before the Streams Directive is able to be enabled. If this bit is set to ‘1’, then the<br>Host Identifier is required to be set to a non-zero value before the Streams Directive is able<br>to be enabled.|
|0|**Shared Stream Identifiers (SSID):**This bit indicates whether stream identifiers may be<br>shared by multiple Host Identifiers, or if a stream identifier is associated with a single Host<br>Identifier. If this bit is cleared to ‘0’, then the stream identifier is associated with a single non-<br>zero Host Identifier. If this bit is set to ‘1’, then the stream identifier may be associated with<br>multiple non-zero Host Identifiers.|





|Bytes|Description|
|---|---|
|**NVM Subsystem Specific Fields**|**NVM Subsystem Specific Fields**|
|01:00|**Max Streams Limit (MSL):**This field indicates the maximum number of concurrently open streams that<br>the NVM subsystem supports. This field returns the same value independent of specified namespace.|
|03:02|**NVM Subsystem Streams Available (NSSA)**: This field indicates the number of NVM subsystem stream<br>resources available. These are the stream resources that are not allocated for the exclusive use by a<br>host in any specific namespace. This field returns the same value independent of specified namespace.|
|05:04|**NVM Subsystem Streams Open (NSSO)**: This field indicates the number of open streams in the NVM<br>subsystem that are not associated with a namespace for which resources were allocated using an<br>Allocate Resources operation. This field returns the same value independent of specified namespace.|
|06|**NVM Subsystem Stream Capability (NSSC):** This field indicates the stream capabilities of the NVM<br>subsystem.<br>**Bits**<br>**Description**<br>7:2<br>Reserved<br>1 <br>**Streams Require Non-Zero Host Identifier (SRNZID):**This bit indicates whether the Host<br>Identifier is required to be set to a non-zero value before the Streams Directive is able to be<br>enabled. If this bit is cleared to ‘0’, then the Host Identifier is not required to be set to a non-<br>zero value before the Streams Directive is able to be enabled. If this bit is set to ‘1’, then the<br>Host Identifier is required to be set to a non-zero value before the Streams Directive is able<br>to be enabled.<br>0 <br>**Shared Stream Identifiers (SSID):**This bit indicates whether stream identifiers may be<br>shared by multiple Host Identifiers, or if a stream identifier is associated with a single Host<br>Identifier. If this bit is cleared to ‘0’, then the stream identifier is associated with a single non-<br>zero Host Identifier. If this bit is set to ‘1’, then the stream identifier may be associated with<br>multiple non-zero Host Identifiers.|
|15:07|Reserved|
|**Namespace Specific Fields**|**Namespace Specific Fields**|
|19:16|**Stream Write Size (SWS):**This field indicates the alignment and size of the optimal stream write as a<br>number for the specified namespace where the unit of granularity is specified by the applicable I/O<br>Command Set. The size indicated should be less than or equal to Maximum Data Transfer Size (MDTS)<br>that is specified in units of minimum memory page size. SWS may change if the namespace is<br>reformatted with a different User Data Format. If the NSID value is set to FFFFFFFFh, then this field may<br>be cleared to 0h if a single user data size cannot be indicated.<br>Refer to the applicable I/O Command Set specification for how this field is utilized to optimize<br>performance and endurance.|


502


NVM Express [®] Base Specification, Revision 2.2


**Figure 608: Streams Directive – Return Parameters Data Structure**







|Bytes|Description|
|---|---|
|21:20|**Stream Granularity Size (SGS):** This field indicates the stream granularity size for the specified<br>namespace in Stream Write Size (SWS) units. If the NSID value is set to FFFFFFFFh, then this field may<br>be cleared to 0h.<br>Refer to the applicable I/O Command Set specification for how this field is utilized to optimize<br>performance and endurance.|
|**Namespace and Host Identifier Specific Fields**|**Namespace and Host Identifier Specific Fields**|
|23:22|**Namespace Streams Allocated (NSA):**This field indicates the number of stream resources allocated<br>for exclusive use of the specified namespace.<br>If the SSID bit is cleared to ‘0’ in the NSSC field, then those exclusive stream resources are shared by<br>the controller processing the Return Parameters operation and by all other controllers that share the<br>same non-zero Host Identifier, and are attached to the specified namespace.<br>If the SSID bit is set to ‘1’, then those exclusive stream resources are shared by all controllers that are<br>associated with any non-zero Host Identifier and are attached to this namespace.<br>If this value is non-zero, then the namespace may have up to NSA number of concurrently open streams.<br>If this field is cleared to 0h, then no stream resources are currently allocated to this namespace and the<br>namespace may have up to NSSA number of concurrently open streams.|
|25:24|**Namespace Streams Open (NSO)**: This field indicates the number of open streams in the specified<br>namespace.<br>If the SSID bit is cleared to ‘0’, then this field indicates the number of streams that were opened by the<br>controller processing the Return Parameters operation and by all other controllers that share the same<br>non-zero Host Identifier, and are attached to this namespace.<br>If the SSID bit is set to ‘1’, then this field indicates the number of streams that were opened by the<br>controller processing the Return Parameters operation and all other controllers that are associated with<br>any non-zero Host Identifier and are attached to this namespace.<br>Note: It is not possible for a host to retrieve the number of open streams using resources allocated to the<br>specified namespace by other hosts.|
|31:26|Reserved|


**Get Status (Directive Operation 02h)**


The Get Status operation returns information about the status of currently open streams for the specified
namespace and the host issuing the Get Status operation. The DSPEC field in command Dword 11 is not
used for this operation.


If the SSID bit is cleared to ‘0’ in the NSSC field, then the information returned describes only those
resources for the specified namespace that are associated with hosts that are registered with the same
non-zero Host Identifier value as the host issuing the Get Status operation. If the SSID bit is set to ‘1’, then
the information returned describes the resources for the specified namespace that are associated with
hosts that are registered with any non-zero Host Identifier.


If an NSID value of FFFFFFFFh is specified, then the controller shall return information about the status of
currently open streams in the NVM subsystem that use resources which are not allocated for the exclusive
use of a particular namespace. If a stream identifier value being returned is in use by different namespaces,
then that stream identifier shall be returned only once.


Stream Identifier 1 (i.e., returned at offset 03:02) contains the value of the open stream of lowest numerical
value. Each subsequent field contains the value of the next numerically greater stream identifier of an open
stream.


The data structure returned is defined in Figure 609. All fields are specific to the specified namespace if the
NSID value was not set to FFFFFFFFh.


503


NVM Express [®] Base Specification, Revision 2.2


**Figure 609: Streams Directive – Get Status Data Structure**








|Bytes|Description|
|---|---|
|01:00|**Open Stream Count (OSC):**This field specifies the number of streams that are currently open.|
|03:02|**Stream Identifier 1 (SID1):**This field specifies the stream identifier of the first (numerically lowest)<br>open stream.|
|05:04|**Stream Identifier 2 (SID2):**This field specifies the stream identifier of the second open stream.|
|…|…|
|131071:<br>131070|**Stream Identifier 65,535 (SID655355):**This field specifies the stream identifier of the 65,535th<br>open stream.|



**Allocate Resources (Directive Operation 03h)**


The Allocate Resources operation indicates the number of streams that the host requests for the exclusive
use for the specified namespace. If the SSID bit is cleared to ‘0’ in the NSSC field, then those resources
are for the exclusive use of hosts that are registered with the same Host Identifier as the host that made
the request. If the SSID bit is set to ‘1’, then those resources are for the exclusive use of any host that is
registered with any non-zero Host Identifier. The DSPEC field in command Dword 11 is not used for this
operation. The operation returns the number of streams allocated in Dword 0 of the completion queue entry.
The value allocated may be less than or equal to the number requested. The allocated resources shall be
reflected in the Namespace Streams Allocated field of the Return Parameters data structure.


If the controller is unable to allocate any stream resources for the exclusive use for the specified
namespace, then the controller shall:

  - return a status value of Stream Resource Allocation Failed; or

  - if NVM subsystem stream resources are available, then clear NSA to 0h in the completion queue
entry to indicate that the host may use stream resources from the NVM subsystem for this
namespace.


If the specified namespace already has stream resources allocated for the exclusive use of the host issuing
the Allocate Resources operation, then the controller shall return a status code of Invalid Field in Command.
To allocate additional streams resources, the host should release resources and request a complete set of
resources.


No data transfer occurs.


**Figure 610: Allocate Resources – Command Dword 12**

|Bits|Description|
|---|---|
|31:16|Reserved|
|15:00|**Namespace Streams Requested (NSR):**This field specifies the number of stream resources the host<br>is requesting be allocated for exclusive use by the specified namespace.|



**Figure 611: Allocate Resources – Completion Queue Entry Dword 0**






|Bits|Description|
|---|---|
|31:16|Reserved|
|15:00|**Namespace Streams Allocated (NSA):**This field indicates the number of streams resources that have<br>been allocated for exclusive use by the specified namespace. The allocated resources are available to<br>all controllers associated with that host.|



**8.1.8.3.2** **Directive Send**


This section defines operations used with the Directive Send command for the Streams Directive.


**Release Identifier (Directive Operation 01h)**


The Release Identifier operation specifies that the stream identifier specified in the DSPEC field in
command Dword 11 is no longer in use by the host. Specifically, if the host uses that stream identifier in a


504


NVM Express [®] Base Specification, Revision 2.2


future operation, then that stream identifier is referring to a different stream. If the specified identifier does
not correspond to an open stream for the specified namespace, then the Directive Send command should
not fail as a result of the specified identifier. If there are stream resources allocated for the exclusive use of
the specified namespace, then those exclusive stream resources remain allocated for this namespace and
may be re-used in a subsequent write command. If there are no stream resources allocated for the exclusive
use of the specified namespace, then the stream resources are returned to the NVM subsystem stream
resources for future use by a namespace without exclusive allocated stream resources. If an NSID value
of FFFFFFFFh is specified, then the controller shall abort the command with a status code of Invalid Field
in Command.


No data transfer occurs.


**Release Resources (Directive Operation 02h)**


The Release Resources operation is used to release all streams resources allocated for the exclusive use
of the namespace attached to all controllers:

  - associated with the same non-zero Host Identifier of the controller that processed the operation if
the SSID bit is cleared to ‘0’ in the NSSC field is cleared to ‘0’; and

  - associated with any non-zero Host Identifier if the SSID bit is set to ‘1’.


On successful completion of this command, the exclusive allocated stream resources are released and the
Namespace Streams Allocated (refer to Figure 608) field is cleared to 0h for the specified namespace. If
this command is issued when no streams resources are allocated for the exclusive use of the namespace,
then the Directive Send command shall take no action and shall not fail as a result of no allocated stream
resources.


No data transfer occurs.


**Data Placement (Directive Type 02h, Optional)**


The Data Placement Directive enables the host to specify to the controller the Reclaim Unit (refer section
8.1.10) to place the user data in I/O commands specified by the appropriate I/O Command Set specification.


The Data Placement Directive has no Directive Operations defined. Any Directive Receive command or
Directive Send command that specifies the Data Placement Directive in the Directive Type (DTYPE) field
in Command Dword 11 shall be aborted by the controller with a status code of Invalid Field in Command.


If a Directive Send command to enable the Data Placement Directive is processed (refer to section
8.1.8.2.2.1) and the specified namespace is not contained in an Endurance Group with Flexible Data
Placement enabled, then the controller shall abort the Directive Send command with a status code of FDP
Disabled.


**Dispersed Namespaces**


Dispersed namespaces provide hosts with access to the same namespace using multiple participating NVM
subsystems. A typical Dispersed Namespace implementation uses Fabrics based NVM subsystems. Two
prominent scenarios that require namespace access from multiple participating NVM subsystems are:


1. online data migration; and
2. data replication.


Online data migration is used to transparently move the contents of one or more namespaces across
participating NVM subsystems without disrupting host access to those namespaces during the migration.
For each namespace whose contents are migrated, one or more paths to the namespace in the destination
NVM subsystem are added to the multi-path I/O on the host, in addition to the existing paths to the
namespace in the source NVM subsystem. Once the online data migration completes (i.e., all of the
contents of all namespaces being migrated has been successfully migrated from the source NVM
subsystem to the destination NVM subsystem), all of the paths to the namespace in the source NVM
subsystem are subsequently removed from the multi-path I/O on the host. During the online data migration,
the host and participating NVM subsystems must manage the paths so that there is no interruption to I/O.


505


NVM Express [®] Base Specification, Revision 2.2


Figure 612 shows an example of online data migration, where the contents of namespace B are migrated
from one participating NVM subsystem to another participating NVM subsystem. In this figure, the lines
from the host to the NVMe controllers may represent multiple connections from the host to multiple
controllers in each participating NVM subsystem.


**Figure 612: Online Data Migration**





















Data replication is used to replicate the contents of one or more dispersed namespaces across participating
NVM subsystems such that each participating NVM subsystem is able to provide host access to the same
namespace data. Other behavior (e.g., persistent reservations) must also be maintained between hosts
and each participating NVM subsystem. Figure 613, Figure 614, and Figure 615 show different examples
of data replication, where the contents of namespace B are replicated across two participating NVM
subsystems. In these figures, the lines from hosts to NVMe controllers may represent multiple connections
from the hosts to multiple controllers in each participating NVM subsystem. Figure 613 shows an example
of single NVM subsystem host connectivity, where two hosts access the same dispersed namespace being
replicated across two participating NVM subsystems via controllers in only one NVM subsystem.


506


NVM Express [®] Base Specification, Revision 2.2


**Figure 613: Data Replication Example 1**



















Figure 614 shows another example of single NVM subsystem host connectivity, where two hosts access
the same dispersed namespace being replicated across two participating NVM subsystems via controllers
in only one NVM subsystem, but the host connected to NVM Subsystem 2 only accesses namespace B in
the event of a failure scenario.


**Figure 614: Data Replication Example 2**



















Figure 615 shows an example of multiple NVM subsystem host connectivity, where two hosts access the
same dispersed namespace being replicated across two participating NVM subsystem via controllers in
both NVM subsystems.


507


NVM Express [®] Base Specification, Revision 2.2


**Figure 615: Data Replication Example 3**



















**Dispersed Namespace Management**


The Namespace Management command (refer to section 5.1.21) may be used to create a namespace that
is capable of being accessed using controllers contained in two or more participating NVM subsystems
concurrently (i.e., may be used to create a namespace that is capable of being a dispersed namespace).
The methods for dispersing a namespace (e.g., attaching that namespace to controllers contained in
separate participating NVM subsystems) are outside the scope of this specification. The Namespace
Management or Capacity Management command may be used to delete a dispersed namespace on the
participating NVM subsystem containing the controller processing the command. Deleting a dispersed
namespace on one participating NVM subsystem may or may not affect that namespace on other
participating NVM subsystems (e.g., a deletion from one participating NVM subsystem may have no effect
on the namespace on other participating NVM subsystems, or a deletion from one participating NVM
subsystem may delete the namespace from all participating NVM subsystems).


The Namespace Management command may be used to create a shared namespace that is not a
dispersed namespace which is later converted to a dispersed namespace. The method of converting a
namespace that is not a dispersed namespace to a dispersed namespace is outside the scope of this
specification. NVM subsystems should not convert private namespaces to dispersed namespaces.
Whenever a namespace that is not a dispersed namespace is converted to a dispersed namespace or a
dispersed namespace is converted to a namespace that is not a dispersed namespace, the controller
reports a Namespace Attribute Changed event as described in Figure 152.


The host may attach or detach a dispersed namespace from the controller by using the Namespace
Attachment command (refer to section 5.1.20).


**NSID and Globally Unique Namespace Identifier Usage**


The NSID for a dispersed namespace is unique for all controllers in a participating NVM subsystem, as
described in section 3.2.1.6. The NSID for a dispersed namespace may be different on different
participating NVM subsystems.


A dispersed namespace has a globally unique namespace identifier (refer to section 4.7.1.4) that uniquely
identifies the namespace in all participating NVM subsystems. The globally unique namespace identifier
has the same value for that namespace in all participating NVM subsystems and shall be used to determine
which NSIDs on different participating NVM subsystems refer to the same namespace. The globally unique


508


NVM Express [®] Base Specification, Revision 2.2


namespace identifier that uniquely identifies the dispersed namespace in all participating NVM subsystems
shall be either:


a) a Namespace Globally Unique Identifier (NGUID); or
b) a Universally Unique Identifier (UUID).


If the dispersed namespace has an NGUID and does not have a UUID, then:


a) that NGUID shall be the globally unique namespace identifier that uniquely identifies the dispersed

namespace in all participating NVM subsystems;
b) all participating NVM subsystems shall use the same NGUID value for the dispersed namespace;

and
c) the dispersed namespace may have an EUI64 that shall not be the globally unique namespace

identifier that uniquely identifies the dispersed namespace in all participating NVM subsystems.


If the dispersed namespace has a UUID and does not have an NGUID, then:


a) that UUID shall be the globally unique namespace identifier that uniquely identifies the dispersed

namespace in all participating NVM subsystems;
b) all participating NVM subsystems shall use the same UUID value for the dispersed namespace;

and
c) the dispersed namespace may have an EUI64 that shall not be the globally unique namespace

identifier that uniquely identifies the dispersed namespace in all participating NVM subsystems.


If the dispersed namespace has an NGUID and has a UUID, then:


a) the NGUID shall be the globally unique namespace identifier that uniquely identifies the dispersed

namespace in all participating NVM subsystems;
b) all participating NVM subsystems shall use the same NGUID value for the dispersed namespace;

and
c) the dispersed namespace may have an EUI64 that shall not be the globally unique namespace

identifier that uniquely identifies the dispersed namespace in all participating NVM subsystems.


**Dispersed Namespace Access**


The host may discover if a namespace is capable of being accessed using controllers contained in two or
more participating NVM subsystems concurrently (i.e., may discover if a namespace may be a dispersed
namespace) by issuing an Identify command (i.e., CNS 00h if supported by the I/O Command Set or CNS
08h) to the controller for the specified NSID. If the namespace is capable of being accessed using
controllers contained in two or more participating NVM subsystem concurrently, then the controller shall set
the Dispersed Namespace (DISNS) bit to ‘1’ in the Namespace Multi-path I/O and Namespace Sharing
Capabilities (NMIC) field of the returned I/O Command Set Independent Identify Namespace data structure
(refer to Figure 320) or Identify Namespace data structure (refer to the NVM Command Set Specification).


All controllers in each participating NVM subsystem that are able to provide access to a specific dispersed
namespace shall support the I/O Command Set associated with that dispersed namespace.


The host may discover the NQNs of participating NVM subsystems which contain controllers that are able
to provide access to a dispersed namespace by issuing a Get Log Page command for the Dispersed
Namespace Participating NVM Subsystems log page (i.e., the Log Page Identifier (LID) field set to 17h
(refer to section 5.1.12.1.23)).


Hosts specify support for dispersed namespaces by setting the Host Dispersed Namespace Support
(HDISNS) field to 1h in the Host Behavior Support feature by issuing a Set Features command with Feature
Identifier (FID) set to 16h (refer to Figure 408).


If the HDISNS field is set to 1h, the host specifies support for:

  - treating all instances of a dispersed namespace as the same namespace, based upon the shared
globally unique namespace identifier (refer to section 8.1.9.2) when accessing that dispersed
namespace through multiple controllers on the same participating NVM subsystem;


509


NVM Express [®] Base Specification, Revision 2.2


  - treating all instances of a dispersed namespace as the same namespace, based upon the shared
globally unique namespace identifier when accessing that dispersed namespace through
controllers on multiple participating NVM subsystems; and

  - specifying a Host Identifier that is unique across all hosts that connect to any participating NVM
subsystem.


If the HDISNS field is set to 1h, the controller shall not abort any command that the host submits to
dispersed namespaces with a status code of Host Dispersed Namespace Support Not Enabled.


A participating NVM subsystem shall support prohibiting host access to dispersed namespaces when the
HDISNS field is cleared to 0h in the Host Behavior Support feature, as described in section 8.1.9.4. A
participating NVM subsystem may either:

  - allow host access to a dispersed namespace when the HDISNS field is cleared to 0h in the Host
Behavior Support feature if the host associated with the Host NQN in the connection is only able to
access the dispersed namespace from a single participating NVM subsystem; or

  - prohibit host access to dispersed namespaces when the HDISNS field is cleared to 0h in the Host
Behavior Support feature.


A participating NVM subsystem that allows host access to a dispersed namespace when the HDISNS field
is cleared to 0h in the Host Behavior Support feature if the host associated with the Host NQN in the
connection is only able to access the dispersed namespace from a single participating NVM subsystem
shall implement a method to determine if the host is able to access the dispersed namespace from multiple
participating NVM subsystems. The method used to determine if the host is able to access the dispersed
namespace from multiple participating NVM subsystems is outside the scope of this specification. If a
participating NVM subsystem determines that a Connect command requests a host with the HDISNS field
cleared to 0h in the Host Behavior Support feature having access to the same dispersed namespace
through multiple participating NVM subsystems, then that participating NVM subsystem shall either:


a) abort a Connect command with a status code of Connect Invalid Host if that Connect command

requests the host associated with the Host NQN in the connection having access to a dispersed
namespace through multiple participating NVM subsystems. Aborting a Connect command for this
reason may result in the host being unable to access other namespaces (i.e., namespaces that are
unrelated to the dispersed namespace) on that NVM subsystem. This enforces the requirement
that a host that has not set the HDISNS field to 1h in the Host Behavior Support feature be allowed
to access a dispersed namespace on only one participating NVM subsystem by preventing all
access to any other participating NVM subsystems (including all other namespaces on those other
participating NVM subsystems); or
b) allow a Connect command that requests the host associated with the Host NQN in the connection

having access to a dispersed namespace through multiple participating NVM subsystems, but
prohibit host access to that dispersed namespace from multiple participating NVM subsystems
(e.g., prohibit host access to that dispersed namespace on the second participating NVM
subsystem) as described in section 8.1.9.4. This enforces the requirement that a host that has not
set the HDISNS field to 1h in the Host Behavior Support feature be allowed to access a dispersed
namespace on only one participating NVM subsystem by, for each dispersed namespace,
preventing access to that dispersed namespace on any other participating NVM subsystems (and
allowing access to other namespaces that are not dispersed namespaces on those other
participating NVM subsystems).


**Prohibiting Host Access to Dispersed Namespaces**


If a participating NVM subsystem prohibits host access to dispersed namespaces when the Host Dispersed
Namespace Support (HDISNS) field is cleared to 0h in the Host Behavior Support feature, then the
controller shall abort the following commands with a status code of Host Dispersed Namespace Support
Not Enabled:

  - any I/O commands (refer to section 7 in this specification and the I/O Commands section in the
appropriate I/O Command Set specification) that specify the NSID of a dispersed namespace in
the command; or


510


NVM Express [®] Base Specification, Revision 2.2


  - any of the Admin commands listed in Figure 616 that specify the NSID of a dispersed namespace
in the command.


The Additional Restrictions column in Figure 616 lists additional restrictions that apply while the HDISNS
field is cleared to 0h in the Host Behavior Support feature for Admin commands that are capable of affecting
dispersed namespaces without specifying the NSID of a dispersed namespace.


**Figure 616: Dispersed Namespaces Command Restrictions - Prohibited Admin Commands**






|Admin Command|Additional Restrictions|
|---|---|
|Directive Receive|None.|
|Directive Send|None.|
|Set Features|This command is prohibited if a dispersed namespace is attached to the controller and<br>an NSID of FFFFFFFFh is specified for a feature capable of affecting all namespaces<br>attached to that controller.|
|Format NVM|This command is prohibited if a dispersed namespace exists in the participating NVM<br>subsystem and the scope of the command includes all namespaces that exist in that<br>NVM subsystem (refer to Figure 189).<br>This command is prohibited if a dispersed namespace is attached to the controller and<br>the scope of the command includes all namespaces attached to that controller (refer to<br>Figure 189).|



**ANA Considerations**


If more than one participating NVM subsystem contains controllers that provide a host with access to a
dispersed namespace, then Asymmetric Namespace Access (ANA) and Asymmetric Namespace Access
Reporting (refer to section 8.1.1) should be supported in all participating NVM subsystems. If ANA is used
with dispersed namespaces, then globally unique namespace identifiers (refer to section 8.1.9.2) are used
to determine when multiple paths are available to the same dispersed namespace. Hosts specify to
controllers that their host software (e.g., multipath I/O software) uses globally unique namespace identifiers
to determine when multiple paths are available to the dispersed namespace by setting the HDISNS field to
1h in the Host Behavior Support feature, as described in section 8.1.9.3.


ANA Group usage with dispersed namespaces is described in section 8.1.1.2.


**Reservation Considerations**


Reservations for a dispersed namespace that is able to be accessed by controllers in multiple participating
NVM subsystems are intended to be coordinated between each participating NVM subsystem. To ensure
the uniqueness of a host’s identity and prevent potential data corruption, each host that sets the Host
Dispersed Namespace Support (HDISNS) field to 1h in the Host Behavior Support feature specifies a Host
Identifier that is unique across all hosts that connect to any participating NVM subsystem, as described in
section 8.1.9.3.


If a host is a reservation registrant on a dispersed namespace, and that host submits a Reservation Report
command to that namespace, then for reservations established using controllers that are not contained in
the same participating NVM subsystem as the controller processing the Reservation Report command, the
Controller ID (CNTLID) field shall be set to FFFDh in the Registered Controller data structure (refer to Figure
584) or Registered Controller Extended data structure (refer to Figure 585). Multiple identical Registered
Controller or Registered Controller Extended data structures with the CNTLID field set to FFFDh shall not
be returned by a single Reservation Report command; as a result, a Registered Controller or Registered
Controller Extended data structure with the CNTLID field set to FFFDh indicates one or more controllers
are associated with a host that is a registrant of the dispersed namespace in another participating NVM
subsystem. A Registered Controller or Registered Controller Extended data structure with the CNTLID field
set to FFFDh is returned for each host (i.e., as identified by the HOSTID field in that data structure) that is
a registrant of the dispersed namespace in any other participating NVM subsystem.


The Dispersed Namespace Reservation Support (DISNSRS) bit in a command is set to ‘1’ by hosts that
support reservations on dispersed namespaces (i.e., hosts that support receiving a value of FFFDh in the
CNTLID field of a Registered Controller data structure or Registered Controller Extended data structure).


511


NVM Express [®] Base Specification, Revision 2.2


A controller that supports dispersed namespaces and supports reservations (i.e., a controller that has the
Reservations Support (RESERVS) bit set to ‘1’ in the Optional NVM Command Support (ONCS) field of the
Identify Controller data structure (refer to Figure 313)) shall support the DISNSRS bit being set to ‘1’ in each
command in the following list:

  - Reservation Acquire (refer to section 7.5);

  - Reservation Register (refer to section 7.6);

  - Reservation Release (refer to section 7.7); and

  - Reservation Report (refer to section 7.8).


If the HDISNS field is set to 1h in the Host Behavior Support feature and the DISNSRS bit is cleared to ‘0’
in any of the commands in the preceding list when submitted to a dispersed namespace, then the controller
shall abort that command with a status code of Namespace Is Dispersed.


**Flexible Data Placement**


**Flexible Data Placement Overview**


The Flexible Data Placement (FDP) capability is an optional capability which allows the host to reduce write
amplification by aligning user data usage to physical media. The controller supports log pages which
indicate the status of FDP, statistics about the FDP operation, and information the host uses to detect and
correct usage patterns that increase write amplification.


The scope of the Flexible Data Placement capability is an Endurance Group.


The host enables or disables Flexible Data Placement by issuing a Set Features command specifying the
Flexible Data Placement feature (refer to section 5.1.25.1.20) and the FDP configuration (refer to section
5.1.12.1.28) to be applied to an Endurance Group. The host is required to delete all namespaces associated
with the specified Endurance Group before modifying the value of the Flexible Data Placement feature
(e.g., transitioning from disabled to enabled).


If a Set Features command specifies:

  - the Flexible Data Placement feature;

  - an Endurance Group in which one or more namespaces exist; and

  - a different value from the current value of that feature for that Endurance Group,


then the controller shall abort the command with a status code of Command Sequence Error.


If a Set Features command is successful and changes the Feature value, then:

  - all events in the FDP Events log page (refer to section 5.1.12.1.31) are cleared; and

  - all fields in the FDP Statistics log page (refer to section 5.1.12.1.30) are cleared to 0h.


Refer to section 3.2.4 for the logical view of the non-volatile storage capacity for the Endurance Group with
Flexible Data Placement enabled.


The Namespace Management command (refer to section 8.1.15) is used to create a namespace within the
Endurance Group. All namespaces in an Endurance Group with Flexible Data Placement enabled shall be
associated with the NVM Command Set (refer to Figure 312) (i.e., the Command Set Identifier (CSI) field
in the Namespace Management command shall be cleared to 00h). The capacity for the user data stored
by a write command to a namespace is allocated from the Reclaim Unit referenced by the Reclaim Unit
Handle and Reclaim Group specified by that write command. The user data for a namespace is allowed to
be in any stored Reclaim Unit within any Reclaim Group within the Endurance Group (refer to Figure 15).


The Namespace Management command specifies a Placement Handle List (refer to the Namespace
Management command in the appropriate I/O Command Set specification). Each entry in that list specifies
the Reclaim Unit Handle associated with the Placement Handle for that entry. The Placement Handles are
numbered from 0h to the number of entries in the list minus 1. Figure 617 shows an example where
Namespace A associates Reclaim Unit Handle 1 with Placement Handle 0. A specific Reclaim Unit Handle
is not allowed to be associated with more than one Placement Handle per namespace. There are no other
requirements on which Reclaim Unit Handle is associated with which Placement Handle.


512


NVM Express [®] Base Specification, Revision 2.2


Namespaces are allowed to utilize the same (i.e., share) Reclaim Unit Handle but may have restrictions
defined in the applicable I/O Command Set specification.


The host is required to enable the Data Placement Directive (refer to section 8.1.8.4) to submit write
commands that specify a Placement Identifier (refer to Figure 283 and Figure 284) in the DSPEC field. That
Placement Identifier uniquely specifies the Reclaim Unit in which to place the user data (refer to Figure
617). The controller determines the Reclaim Unit by using the Reclaim Unit Handle associated with the
Placement Handle that was specified by the host when the namespace was created. For example, if the
write command in Figure 617 specifies a Reclaim Group Identifier value of 2h and a Placement Handle
value of 1h, then the host is targeting the user data for that write command to be placed into the Reclaim
Unit associated with Reclaim Group 2h and Reclaim Unit Handle _NRUH_ -1.


A Placement Identifier is invalid if:

  - the Reclaim Group Identifier value is greater than or equal to the number of Reclaim Groups
supported by the enabled FDP configuration (refer to the NRG field in Figure 281); or

  - the Placement Handle is greater than or equal to the number of Placement Handles supported by
the Namespace Management command of the applicable I/O Command Set specification.


If the Placement Identifier in the DSPEC field of a write command is invalid, then the controller shall:

  - select the Reclaim Group and Reclaim Unit Handle accessible by the specified namespace to
determine the placement of the user data for that write command; and

  - generate an Invalid Placement Identifier FDP Event if that event is enabled for the selected Reclaim
Unit Handle. To receive the FDP event, the host should enable the Invalid Placement Identifier FDP
Event on all Reclaim Unit Handles.


Any write command to a namespace that exists in an Endurance Group with Flexible Data Placement
enabled that does not specify the Data Placement Directive uses the Placement Handle value 0h and the
controller selects the Reclaim Group for that command. For example, if the write command does not specify
the Data Placement Directive, then, as illustrated in Figure 617, Placement Handle value of 0h is associated
with Reclaim Unit Handle 1h and the controller may place the user data into the Reclaim Unit associated
any Reclaim Group using Reclaim Unit Handle 1h.


513


NVM Express [®] Base Specification, Revision 2.2


**Figure 617: Flexible Data Placement Model**






















|Col1|Col2|Col3|Col4|Col5|Col6|Col7|Col8|
|---|---|---|---|---|---|---|---|
|||Reclaim Unit H|Reclaim Unit H|an|dle 0|||
|||||||||
|||||||||















Reclaim
Group 0











Reclaim
Group 1





Reclaim
Group 2







Reclaim Group

_NRG-1_



A write command that places user data into a Reclaim Unit causes reduction of the remaining capacity of
that Reclaim Unit. If that Reclaim Unit is written to capacity, then the controller modifies the Reclaim Unit
Handle referencing that Reclaim Unit to reference a different Reclaim Unit within the same Reclaim Group.


A controller may modify a Reclaim Unit Handle to reference a different Reclaim Unit as part of performing
a sanitize operation (refer to section 8.1.24).


A Reclaim Unit shall only be referenced by one Reclaim Unit Handle. Therefore, a write command that
utilizes a Reclaim Unit Handle results in the user data from that write command being initially isolated from
the user data from any other write command that utilizes a different Reclaim Unit Handle. Each Reclaim
Unit Handle has a type as defined in Figure 282 that identifies the isolation requirements of the user data
moved by the controller to a different Reclaim Unit due to vendor specific controller operations (e.g.,
garbage collection).


A controller is allowed to move user data that was written by the host that utilized a Reclaim Unit Handle
with an Initially Isolated type (Figure 282) to a different Reclaim Unit within the same Reclaim Group. In
addition, the controller is allowed to move user data written by the host that utilized different Reclaim Unit
Handles with an Initially Isolated type to that different Reclaim Unit within the same Reclaim Group as
shown in Figure 618.


A controller is allowed to move user data that was written by the host that utilized a Reclaim Unit Handle
with a Persistently Isolated type (Figure 282) to a different Reclaim Unit within the same Reclaim Group.
However, the controller shall only move user data written by the host that utilized the same Reclaim Unit
Handles with a Persistently Isolated type to the different Reclaim Unit within the same Reclaim Group as
shown in Figure 619.


514


NVM Express [®] Base Specification, Revision 2.2


**Figure 618: Initially Isolated Reclaim Unit Handles**


**Figure 619: Persistently Isolated Reclaim Unit Handle**


The result of a Namespace Management command that creates a namespace within the Endurance Group
is that at least one Placement Handle is defined for that namespace (refer to the Namespace Management
section in applicable I/O Command Set specification).


For any namespace created in an Endurance Group that has Flexible Data Placement enabled, the host
may issue an I/O Management Receive command to obtain a list of Placement Handles and the associated
Reclaim Unit Handles that are used by the Data Placement Directive in write commands.


If the Flexible Data Placement capability is supported, then the controller shall support the following:


a) the Feature Identifiers Supported and Effects log page (refer to section 5.1.12.1.18);
b) the I/O Management Receive command (refer to section 7.3) and the Reclaim Unit Handle Status

Management Operation in that command (refer to Figure 562);
c) the I/O Management Send command (refer to section 7.4) and the Placement Identifier Update

Management Operation in that command (refer to Figure 566);
d) the Flexible Data Placement feature (refer to section 5.1.25.1.20);
e) the FDP Configurations log page (refer to section 5.1.12.1.28);
f) the Reclaim Unit Handle Usage log page (refer to section 5.1.12.1.29);
g) the FDP Statistics log page (refer to section 5.1.12.1.30);
h) the Flexible Data Placement Events feature (refer to section 5.1.25.1.21);
i) the FDP Events log page (refer to section 5.1.12.1.31); and
j) the Data Placement Directive (refer to section 8.1.8.4).


**Enabling Flexible Data Placement (Informative)**


The host prepares an Endurance Group for operation in Flexible Data Placement using the following
process:


515


NVM Express [®] Base Specification, Revision 2.2


1) Validate that the Flexible Data Placement capability is supported by issuing an Identify command

to access the Identify Controller data structure and checking that the Flexible Data Placement
Support (FDPS) bit is set to ‘1’.
2) Delete any existing namespaces that exist in the Endurance Group where Flexible Data Placement

is to be enabled.
3) Issue a Get Log Page command specifying the FDP Configurations log page (refer to section

5.1.12.1.28). Parse the FDP Configurations List in the returned log page to determine the desired
FDP configuration.
4) Enable Flexible Data Placement utilizing that desired FDP configuration by issuing a Set Features

command specifying:


a. the Flexible Data Placement feature;
b. the Endurance Group Identifier field set to the ENDGID of the Endurance Group in which

Flexible Data Placement is to be enabled;
c. the FDPE bit set to ‘1’ (i.e., enabling Flexible Data Placement); and
d. the Flexible Data Placement Configuration Index field set to the index of the desired FDP

configuration from the FDP Configurations List in the FDP Configurations log page.


5) Issue an Identify command specifying the Identify Namespace data structure (i.e., CNS 00h as

defined in Figure 273) to identify which LBA formats are supported.
6) For each namespace to be created in the Endurance Group, issue a Namespace Management

command specifying:


a. the Select field set to the Create operation (refer to the NVM Express Base Specification);
b. the User Data Format; and
c. the Placement Handle List used to define the Reclaim Unit Handle associated with each

Placement Handle of the namespace (refer to the Namespace Management section of the
applicable I/O Command Set specification).


7) Issue Get Features commands for the FDP Events feature (refer to section 5.1.25.1.21) to acquire

the list of supported FDP events and the enabled state of each supported FDP event.
8) Issue Set Features commands for the FDP Events feature (refer to section 5.1.25.1.21) to specify

if FDP events are required for Reclaim Unit Handles.
9) For each namespace created in an Endurance Group in which the Data Placement Directive is to

be utilized by the host by write commands specifying that namespace:


a. Issue a Directive Send command specifying:


i. the Directive Operation field set to Enable Directive (i.e., 01h);
ii. the NSID of that namespace;
iii. the DTYPE field in Command Dword 11 set to Identify (i.e., 00h);
iv. the DTYPE field in Command Dword 12 set to Data Placement (i.e., 02h); and

v. the Enable Directive bit set to ‘1’ (i.e., to enable the Data Placement Directive).


b. Issue an Identify command with CNS value 08h (i.e., the I/O Command Set Independent

Identify Namespace data structure) to determine if a volatile write cache is present for the
namespace.


Following a Controller Level Reset, the host performs the following actions before resuming use of Flexible
Data Placement in an Endurance Group:


1) Determine the FDP configuration:


a. Issue a Get Feature command specifying the Flexible Data Placement feature (i.e., 1Dh)

and the ENDGID for the Endurance Group to determine if Flexible Data Placement is
enabled and the Flexible Data Placement Configuration Index.
b. Issue a Get Log Page command specifying the FDP Configurations log page (i.e., Log

Page Identifier 20h).


2) Issue Get Features commands for the FDP Events feature (refer to section 5.1.25.1.21) to acquire

the list of supported FDP events and the enabled state of each supported FDP event.


516


NVM Express [®] Base Specification, Revision 2.2


3) Issue Set Features commands for the FDP Events feature (refer to section 5.1.25.1.21) to specify

if supported FDP events are required for Reclaim Unit Handles.
4) For each namespace in the Endurance Group that the Data Placement Directive is to be utilized

by the host by write commands specifying that namespace:


a. Issue an I/O Management Receive command to determine the Placement Handles for that

namespace; and
b. Issue an Identify command with CNS value 08h (i.e., the I/O Command Set Independent

Identify Namespace data structure) to determine if a volatile write cache is present for the
namespace.


**Write Commands using Flexible Data Placement (Informative)**


Hosts writing user data to a namespace created in an Endurance Group that has Flexible Data Placement
enabled have two mechanisms for specifying the placement of the user data with the Endurance Group to
the controller.


1. Each namespace has a default Placement Handle. If any write command:


a. has the DTYPE field being ignored by the controller (refer to section 8.1.8.4); or
b. has the DTYPE field not being ignored by the controller and specifies a DTYPE field value

cleared to 00h,


then the Placement Handle value of 0h for the specified namespace is combined with a Reclaim
Group selected by the controller to create the Placement Identifier (refer to Figure 283 and Figure
284) utilized for that write command.


2. If any write command has the DTYPE field not being ignored by the controller and specifies a
DTYPE field set to Data Placement (i.e., 02h) and specifies a namespace in which the Data
Placement Directive is enabled, then the Placement Identifier specified by the DSPEC field
specifies the Reclaim Group Identifier and Placement Handle used for the write command.


To reduce write amplification, hosts track the user data written to an entire Reclaim Unit and deallocate that
user data by issuing one or more Dataset Management commands specifying the AD bit set to ‘1’ and one
or more Range fields specifying the LBA ranges that were written to that Reclaim Unit.


**Host-Initiated Refresh Operation**


The Host-Initiated Refresh operation of the Device Self-test command performs implementation-specific
refresh operations that verify the media integrity and ensure access to media (e.g., media in an NVM
subsystem that has not been in operation for a long period of time and/or has been subject to extreme
environmental conditions). Examples of refresh operations may include read verification, rewrite of
underlying media that are exhibiting a high correctable error rate (e.g., to prevent future errors), and other
maintenance activities. A Host-Initiated Refresh operation does not change stored user data.


If the Host-Initiated Refresh operation is supported, then the controller shall set the HIRS bit to ‘1’ in the
DSTO field in the Identify Controller data structure (refer to Figure 313).


The percentage complete of the Host-Initiated Refresh operation is indicated in the Current Percentage
Complete field in the Device Self-test log page (refer to section 5.1.12.1.7).


For Host-Initiated Refresh operation, the NSID field in the Device Self-test command is ignored by the
controller and all media in the NVM subsystem is refreshed regardless of whether any portion of the media
is or is not part of any namespace.


A Host-Initiated Refresh operation shall be aborted:


a) if any Controller Level Reset affects the controller on which the device self-test is being performed;
b) if a Format NVM command is processed by any controller in the NVM subsystem;
c) if a sanitize operation is started (refer to section 5.1.22); or
d) if a Device Self-test command with the Self-Test Code field set to Fh is processed by any controller

in the NVM subsystem.


517


NVM Express [®] Base Specification, Revision 2.2


A Controller Level Reset on a controller that is not performing the Host-Initiated Refresh operation shall not
impact that Host-Initiated Refresh operation.


**Host Managed Live Migration**


The migration of a controller, by a host that is using the Host Managed Live Migration capability involves
one or more NVM subsystems, multiple hosts, and multiple controllers. In this section, to differentiate
between the multiple hosts and controllers, each is given a unique name as illustrated in Figure 620. In an
NVM subsystem that supports Host Managed Live Migration, each controller that sets the HMLMS bit to ‘1’
is referred to as a Migration Management Controller (MMC) and each host associated with an MMC is
referred to as a Migration Management Host (MMH). In that same NVM subsystem, all other controllers
(i.e., those that clear the HMLMS bit to ‘0’) are referred to as Migratable Controllers.


The Host Managed Live Migration capability allows an MMH to use an MMC to migrate a Migratable
Controller from a Source NVM Subsystem to a Migratable Controller in a Destination NVM Subsystem.
During that migration, a host is actively submitting commands to a Migratable Controller in the Source NVM
Subsystem and that controller is processing those commands.


The MMH that is managing the migration of a Migratable Controller from the Source NVM Subsystem is
responsible for ensuring that the Migratable Controller in the Destination NVM Subsystem is compatible
with controller state of the Migratable Controller from the Source NVM Subsystem. It is also the
responsibility of the MMH to transfer the migrating data between the NVM subsystems.


**Figure 620: Host Managed Live Migration Host and Controller Naming**

































An MMC is an I/O controller or an Administrative controller that supports the Host Managed Live Migration
capability and provides the ability for the MMH to use privileged actions (refer to section 3.10 to:

   - suspend the processing of commands on the Migratable Controller in the Source NVM Subsystem
being migrated (refer to the Migration Send command in section 5.1.17.1.1);

   - obtain the state of the Migratable Controller in the Source NVM Subsystem being migrated (refer
to the Migration Receive command in section 5.1.16.1.1);

   - set that controller state in the Migratable Controller in the Destination NVM Subsystem (refer to
the Migration Send command in section 5.1.17.1.3); and

   - resume the operation on the Migratable Controller in the Destination NVM Subsystem (refer to the
Migration Send command in section 5.1.17.1.2).


518


NVM Express [®] Base Specification, Revision 2.2


A controller indicates support for the Host Managed Live Migration capability by setting the Host Managed
Live Migration Support (HMLMS) bit to ‘1’ in the Optional Admin Command Support (OACS) field in the
Identify Controller data structure (refer to Figure 313).


An MMC is not permitted to be migrated and:

  - shall support:

    - the Migration Send command with the Management Operations,


`o` Suspend (i.e., 0h);

`o` Resume (i.e., 1h); and

`o` Set Controller State (i.e., 2h);

    - the Migration Receive command with the Management Operations,


`o` Controller State (i.e., 1h);


and

    - the CNS value of 21h in the Identify command (i.e., Supported Controller State Formats data
structure (refer to section 5.1.13.2.21)).


If the NVM subsystem contains one or more Migration Management Controllers, then:

  - each controller (i.e., MMC and Migratable Controller) in that NVM subsystem does not support the
Host Memory Buffer (refer to the Host Memory Buffer Preferred Size (HMPRE) field in the Identify
Controller data structure in Figure 313); and

  - each Migratable Controller in that NVM subsystem is allowed to be migrated and shall not support:


`o` the Migration Send command (refer to section 5.1.17);

`o` the Migration Receive command (refer to section 5.1.16);

`o` the CNS value of 21h in the Identify command (i.e., returning Supported Controller State
Formats data structure (refer to section 5.1.13.2.21)); and

`o` the Controller Data Queue command with the Create Queue management operation
specifying the User Data Migration Queue (refer to section 5.1.4.1.1).


A Controller Level Reset on an MMC shall cause that MMC to:

  - delete all User Data Migration Queues on that MMC; and

  - stop tracking all host memory changes on that MMC;


A Controller Level Reset on a Migratable Controller shall cause that Migratable Controller to:

  - remove a suspended state if that Migratable Controller is suspended by a Migration Send command
specifying the Suspend management operation (refer to section 5.1.17.1.1); and

  - retain any persistent controller state that has been committed to that Migratable Controller from a
Migration Send command specifying the Set Controller State management operation (refer to
section 5.1.17.1.3).


During the migration of a Migratable Controller in the Source NVM Subsystem while that Migratable
Controller is processing commands, it may be necessary for the MMHS to obtain the user data
modifications to namespaces attached to that Migratable Controller and modifications made by that
Migratable Controller to host memory in the host. The Track Send command (refer to section 5.1.27) and
the Track Receive command (refer to section 5.1.26) allows the host to use privileged actions (refer to
section 3.10) to:

  - determine user data in namespaces attached to a controller that has changed; and

  - determine host memory that has changed due to commands processed by a controller.


A controller indicates support for tracking changes to user data in namespaces attached to a controller by
setting the Track User Data Changes Support (TUDCS) bit to ‘1’ in the Tracking Attributes (TRATTR) field
in the Identify Controller data structure (refer to Figure 313).


519


NVM Express [®] Base Specification, Revision 2.2


A controller indicates support for tracking changes to host memory (refer to section 1.5.46) due to the
processing of commands by a controller by setting the Track Host Memory Changes Support (THMCS) bit
to ‘1’ in the TRATTR field.


**Process for Migrating a Controller**


The controller This section provides an example sequence of steps to allow the MMHS to migrate a
Migratable Controller in the Source NVM Subsystem and the attached namespaces to a Migratable
Controller in the Destination NVM Subsystem (refer to Figure 620). Additionally, the steps include obtaining
the host memory modifications made to the host due to the Migratable Controller in the Source NVM
Subsystem processing commands during the migration.


In this example the MMC in the Source NVM Subsystem has:

  - the Track User Data Changes Support (TUDCS) bit set to ‘1’ in the Tracking Attributes (TRATTR)
field in the Identify Controller data structure (refer to Figure 313); and

  - the Track Host Memory Changes Support (THMCS) bit set to ‘1’ in the Tracking Attributes
(TRATTR) field in the Identify Controller data structure.


If attached namespaces are not required to be migrated by the MMHS, then those steps may be ignored.
If host memory modifications are not required to be obtained by the MMHS, then those steps may be
ignored.


1. The MMHS copies (i.e., migrates) the user data in namespaces attached to the Migratable

Controller in the Source NVM Subsystem while the host is submitting commands and the
Migratable Controller is processing those submitted commands.


a. The MMHS creates a User Data Migration Queue in the MMC in the Source NVM Subsystem

by submitting a Controller Data Queue command to that MMC (refer to section 5.1.4)
specifying:

      - the Select field set to the Create Queue management operation (i.e., 1h);

      - the Queue Type field set to User Data Migration Queue; and

      - the Controller Identifier field (refer to Figure 167) set to the controller identifier for the
Migratable Controller in the Source NVM Subsystem.


b. If the Controller Data Queue command is successful, the completion queue entry contains the

Controller Data Queue Identifier for the created User Data Migration Queue. The MMHS
causes the MMC in the Source NVM Subsystem to post user data modifications to namespaces
attached to the Migratable Controller by submitting a Track Send command to that MMC
specifying:

      - the Select field set to Log User Data Changes management operation (i.e., 0h);

      - the Logging Action bit set to ‘1’ (i.e., start logging); and

      - the Controller Data Queue Identifier field set to the Controller Data Queue Identifier from
the completion queue entry for the Controller Data Queue command.


It is the responsibility of the MMHS to make sure that the User Data Migration Queue is sized
properly and there may be more restrictions on that MMHS as specified by the appropriate I/O
command set (e.g., the NVM Command Set requires the MMHS to not allow the User Data
Migration Queue to become full). Refer to section 8.1.6 for a description of the User Data
Migration Queue (i.e., a Controller Data Queue).
c. If the Track Send command is successful, then the MMHS starts copying the namespaces

attached to the Migratable Controller in the Source NVM Subsystem to the Destination NVM
Subsystem. Refer to the applicable I/O Command Set specifications for capabilities that may
reduce the amount of user date that is required to copied (e.g., the Get LBA Status command
in the NVM Command Set Specification).


2. The MMHS causes the MMC in the Source NVM Subsystem to start tracking the modifications to

host memory in the host due to the Migratable Controller processing submitted commands.


520


NVM Express [®] Base Specification, Revision 2.2


a. The MMHS submits a Track Send command to the MMC in the Source NVM Subsystem (refer

to section 5.1.27) specifying:

      - the Select field set to the Track Memory Changes management operation (i.e., 0h);

      - the Tracking Action (TACT) bit set to ‘1’;

      - the Controller Identifier field specifying the identifier for the Migratable Controller in the
Source NVM Subsystem being migrated; and

      - a Track Memory Changes data structure specifying the host memory to be tracked as
described by the set of host memory ranges.


b. If the Track Send command is successful, then the MMHS may query the host memory

modifications that have resulted from the Migratable Controller processing commands by
submitting a Track Receive command to the MMC in the Source NVM Subsystem specifying:

      - the Select field set to the Track Memory Changes management operation (i.e., 0h); and

      - the Controller Identifier field specifying the identifier for the Migratable Controller in the
Source NVM Subsystem being migrated.


3. Once the MMHS has copied the namespaces attached to the Migratable Controller in the Source

NVM Subsystem, that MMHS determines a time to suspend that Migratable Controller. During this
period, that MMHS is migrating the user data in the namespaces attached to that Migratable
Controller that are identified in the posted entries in the User Data Migration Queue. That MMHS
may handle the modified host memory in the host as reported by the Track Receive command.
4. The MMHS suspends the Migratable Controller in the Source NVM Subsystem by submitting a

Migration Send command to the MMC in the Source NVM Subsystem specifying:

      - the Select field set to the Suspend management operation (i.e., 0h);

      - the Suspend Type field set to Suspend;

      - Delete User Data Migration Queue bit set to ‘1’, if the MMHS desires that the MMC delete
the User Data Migration Queue being used to log user data changes of the Migratable
Controller being migrated; and

      - the Controller Identifier field (refer to Figure 167) set to the controller identifier for the
Migratable Controller to be suspended (i.e., the Migratable Controller being migrated).


Prior to completing that Migration Send command:

      - the specified Migratable Controller being suspended:


`o` stops fetching commands (i.e.; from the Admin queue and I/O queues); and

`o` completes all previously fetched commands;


and


      - the MMC processing that Migration Send command:


`o` if user data is being logged into a User Data Migration Queue that is associated with
the Migratable Controller being migrated, an entry is placed into the User Data
Migration Queue that indicates the user data logging has suspended, and then deletes
the User Data Migration Queue, if the Delete User Data Migration Queue bit is set to
‘1’.


5. Since the Migratable Controller in the Source NVM Subsystem is suspended, the MMHS migrates

the user data in the namespaces attached to the Migratable Controller that are identified in the
posted entries in the User Data Migration Queue. Refer to the appropriate I/O command set
specification to determine how the entries identify when entries have completed being posted. That
MMHS may handle the modified host memory in the host as reported by the Track Receive
command.
6. The MMHS is able to obtain the controller state of the Migratable Controller in the Source NVM

Subsystem by submitting one or more Migration Receive commands to the MMC in the Source
NVM Subsystem specifying:


521


NVM Express [®] Base Specification, Revision 2.2


a. the Select field set to the Get Controller State management operation (i.e., 0h);
b. the Sequence Indicator field set to the proper sequence value;
c. the Controller Identifier field set to the controller identifier for the Migratable Controller in the

Source NVM Subsystem;
d. the Controller State Version Index field set to an index into the NVMe Controller State Version

list in the Supported Controller State Formats data structure for MMC in the Source NVM
Subsystem (refer to Figure 330) if the NVMe defined controller state is required; and
e. the Controller State UUID Index field set to an index in the Vendor Specific Controller State

UUID Supported list in the Supported Controller State Formats Data Structure for MMC in the
Source NVM Subsystem (refer to Figure 330), if vendor specific controller state is required.


7. After the MMHS has transferred the obtained controller state information to the MMHD, the MMHD

sets that controller state into a Migratable Controller by submitting a sequence of one or more
Migration Send commands to the MMC in the Destination NVM Subsystem specifying:

      - the Select field set to Set Controller State management operation (i.e., 3h);

      - the Sequence Indicator field set to the proper sequence value;

      - the Controller Identifier field set to the controller identifier for the Migratable Controller in
the Destination NVM Subsystem;

      - the Controller State Version Index field set to an index into the NVMe Controller State
Version list in the Supported Controller State Formats data structure for MMC in the
Destination NVM Subsystem (refer to Figure 330) if value of the NVMe Controller State
Size (NVMECSS) field is non-zero (refer to Figure 359); and

      - the Controller State UUID Index field set to an index in the Vendor Specific Controller State
UUID Supported list in the Supported Controller State Formats Data Structure for MMC in
the Source NVM Subsystem (refer to Figure 330), if the value of the Vendor Specific Size
(VSS) field is non-zero (refer to Figure 359).


8. The MMHD resumes operation on the Migratable Controller in the Destination NVM Subsystem

(i.e., the migrated controller) by submitting a Migration Send command to the MMC in the
Destination NVM Subsystem specifying:

      - the Select field set to Resume management operation (i.e., 2h);

      - the Controller Identifier field (refer to Figure 167) set to the controller identifier for the
Migratable Controller to be resumed.


**Key Per I/O**


The Key Per I/O capability provides a mechanism to use encryption keys that have been injected into an
NVM subsystem by a host. The mechanism to perform activation of the Key Per I/O capability, encryption
key injection, management, and association to encryption key tag is outside the scope of this specification.
One mechanism is defined in the TCG Storage Security Subsystem Class: Key Per I/O Specification using
the NVMe Admin commands Security Send and Security Receive. If the TCG mechanism is used, any
additional modifications to the NVM subsystem as a result of activation of the Key Per I/O Security Provider
are defined in the TCG Storage Interface Interactions Specification (SIIS).


Encryption keys injected into the NVM subsystem may be referenced by I/O commands through the use of
the encryption key tag (refer to the KEYTAG field in Figure 621) associated with the encryption keys. If an
I/O command CETYPE field is set to the KPIOTAG value, then the CEV field (refer to Figure 621) of that
I/O command specifies the encryption key tag associated with the encryption key to be used to encrypt or
decrypt the data in that I/O command. The association of an encryption key tag to a specific encryption key
is outside the scope of this specification. One association mechanism is defined in the TCG Storage
Security Subsystem Class: Key Per I/O Specification.


The Key Per I/O Scope bit (refer to Figure 313) indicates if the Key Per I/O capability:

  - applies to all read and write commands in all namespaces within the NVM subsystem; or

  - independently applies to read and write commands in each namespace within the NVM subsystem.


522


NVM Express [®] Base Specification, Revision 2.2


The Key Per I/O capability does not have any effect on host accesses to RPMBs and Boot Partitions as
these features are not addressed through I/O commands that specify a namespace.


A controller that supports the Key Per I/O capability shall set the KPIOS bit to ‘1’ in the Identify Controller
data structure (refer to Figure 313).


A namespace that supports the Key Per I/O capability shall set the KPIOSNS bit to ‘1’ in the I/O Command
Set Independent Identify Namespace data structure (refer to Figure 320).


The Key Per I/O capability uses the Command Extension Type (CETYPE) and Command Extension Value
(CEV) fields in all read and write commands. Definition of the CETYPE fields are shown in Figure 621.


**Figure 621: CETYPE Definition**









|Value|Definition|CEV Field Definition|
|---|---|---|
|0h|Reserved|Reserved|
|1h|**Key Per I/O Tag (KPIOTAG):** <br>This command is using the Key<br>Per I/O capability.|**Key Tag (KEYTAG)**: Specifies a namespace-specific 16-bit<br>encryption key tag that identifies the encryption key used to encrypt<br>or decrypt the data of the command.<br>The same Key Tag value on different namespaces may or may not<br>identify the same encryption key.<br>Refer to the Maximum Key Tag field in the I/O Command Set<br>Independent Identify Namespace data structure (refer to Figure 320)<br>for the supported values.|
|2h to Eh|Reserved|Reserved|
|Fh|Vendor Specific|Vendor Specific|


If:

  - the Key Per I/O capability is enabled in a namespace (i.e., the KPIOENS bit set to ‘1’);

  - an I/O command supports the CETYPE field; and

  - the CETYPE field in that I/O command is set to a value that is reserved,


then the controller shall abort that command with a status code of Invalid Field in Command.


**Management Addresses**


Various entities on a network are able to request a management agent to perform management operations
on NVM subsystems. A controller in an NVM subsystem use the Management Addresses capability to
indicate the network addresses of those management agents. When an NVM subsystem is provisioned in
a storage system, the management addresses are established in the controller.


Management agents are able to be located in various networked entities, including:

  - NVM subsystems;

  - Fabric interface managers;

  - Embedded management controllers; and

  - Host software.


Each management address is represented as a uniform resource indicator (URI; refer to RFC 3986).


The address of a management agent contained in an NVM subsystem (e.g., an Ethernet-attached SSD) is
indicated in the Management Address List log page (refer to section 5.1.12.1.24), in a Management Address
Descriptor indicating a Management Address Type of 1h. The method by which the address is determined
is outside the scope of this specification.


The address of a management agent contained in a fabric interface manager is indicated in the
Management Address List log page (refer to section 5.1.12.1.24), in a Management Address Descriptor
indicating a Management Address Type of 2h. The method by which the address is determined is outside
the scope of this specification.


523


NVM Express [®] Base Specification, Revision 2.2


The address of a management agent contained in an embedded management controller (e.g., a BMC) is
set and retrieved using the Embedded Management Controller Address feature (refer to section
5.1.25.1.24). The Embedded Management Controller Address feature is intended to be set only by the
storage system containing the embedded management controller. The embedded management controller
is able to ensure this by issuing a Lockdown command (refer to section 5.1.15) with the OFI field specifying
this Feature, and the PRHBT bit set to ‘1’ and the IFC field set to Admin Submission Queue (i.e., 00b).


The address of a management agent contained in host software is set and retrieved using the Host
Management Controller Address feature (refer to section 5.1.25.1.25). The Host Management Agent
Address feature is intended to be set only by host software. Host software is able to ensure this by issuing
a Lockdown command (refer to section 5.1.15) with the OFI field specifying this Feature, and the PRHBT
bit set to ‘1’ and the IFC field set to Out-of-band on a Management Endpoint (i.e., 10b).


**Namespace Management**


The Namespace Management capability consists of the Namespace Management command (refer to
section 5.1.21) and the Namespace Attachment command (refer to section 5.1.20). The Namespace
Management command is used to create a namespace or delete a namespace. The Namespace
Attachment command is used to attach and detach controllers from a namespace. The Namespace
Management capability is intended for use during manufacturing or by a system administrator.


In addition to the Namespace Management capability, there are other events and capabilities that are able
to affect the number of namespaces that exist within an NVM subsystem (e.g., the Capacity Management
capability as described in section 8.1.4).


If the Namespace Management capability is supported, then the controller:


a) shall support the Namespace Management command and the Namespace Attachment

command;
b) shall set the NMS bit to ‘1’ in the OACS field (refer to Figure 313);
c) shall support the Attached Namespace Attribute Changed asynchronous event (refer to Figure

152 and section 5.1.25.1.5);
d) should support the Allocated Namespace Attribute Changed asynchronous event (refer to

Figure 152 and section 5.1.25.1.5); and
e) may support Namespace Granularity (refer to the NVM Command Set Specification).


A controller may support the Namespace Attachment command without supporting the Namespace
Management command. Such a controller:


a) shall not set the Namespace Management Supported (NMS) bit to ‘1’ in the OACS field (refer

to Figure 313); and
b) should support the Namespace Attribute Change asynchronous event.


If a namespace is detached from a controller, then the NSID that referred to that namespace becomes an
inactive NSID (refer to section 3.2.1.4) on that controller. If a namespace is deleted from the NVM
subsystem, then the NSID that referred to that namespace becomes an unallocated NSID (refer to section
3.2.1.3) in the NVM subsystem. Previously submitted but uncompleted or subsequently submitted
commands to the affected NSID are handled by the controller as if they were issued to an inactive NSID
(refer to Figure 92).


The size of a namespace that contains formatted storage is based on the size requested in a create
operation, the format of the namespace, and any characteristics (e.g., endurance). The controller
determines the NVM capacity allocated for that namespace. Namespaces may be created with different
usage characteristics (e.g., endurance) that utilize differing amounts of NVM capacity. Namespace
characteristics and the mapping of these characteristics to NVM capacity usage are outside the scope of
this specification.


Reporting of capacity information for the NVM subsystem, Domain, Endurance Group, and NVM Set are
described in section 3.8. For each namespace that contains formatted storage, the NVM Set and the
Endurance Group that contain the namespace are reported in the Identify Namespace data structure. The
NVM Set to be used for a namespace that contains formatted storage is based on the value in the NVM


524


NVM Express [®] Base Specification, Revision 2.2


Set Identifier field in a create operation. If the NVM Set Identifier field is cleared to 0h in a create operation
for a namespace that contains formatted storage, then the controller shall choose the NVM Set from which
to allocate capacity to create that namespace.


If the NVM Set Identifier field and the Endurance Group Identifier field are both cleared to 0h in a create
operation for a namespace that contains formatted storage, then the controller shall choose the Endurance
Group and the NVM Set from which to allocate capacity to create that namespace.


If the NVM Set Identifier field is cleared to 0h and the Endurance Group Identifier field is set to a non-zero
value in a create operation for a namespace that contains formatted storage, then the controller shall
choose the NVM Set in the specified Endurance Group from which to allocate capacity to create that
namespace.


If the NVM Set Identifier field is set to a non-zero value and the Endurance Group Identifier field is cleared
to 0h in a create operation for a namespace that contains formatted storage, then the controller shall abort
the command with a status code of Invalid Field in Command.


If the NVM Set Identifier field and the Endurance Group Identifier field are both set to non-zero values in a
create operation for a namespace that contains formatted storage and the specified NVM Set exists in the
specified Endurance Group, then the controller shall allocate capacity for that created namespace from the
specified NVM Set.


If the NVM Set Identifier field and the Endurance Group Identifier field are both set to non-zero values in a
create operation for a namespace that contains formatted storage and the specified NVM Set does not exist
in the specified Endurance Group, then the controller shall abort the command with a status code of Invalid
Field in Command.


For each namespace that contains formatted storage, the NVM capacity used for that namespace is
reported in the Identify Namespace data structure (refer to the applicable I/O Command Set specification).
The controller may allocate NVM capacity in units such that the requested size for a namespace that
contains formatted storage may be rounded up to the next unit boundary. The units in which NVM capacity
is allocated are reported in the Namespace Granularity List (refer to the NVM Command Set Specification),
if supported. For example, when using the NVM Command Set, if host software requests a namespace of
32 logical blocks with a logical block size of 4 KiB for a total size of 128 KiB and the allocation unit for the
implementation is 1 MiB, then the NVM capacity consumed may be rounded up to 1 MiB. The NVM capacity
fields may not correspond to the logical block size multiplied by the total number of logical blocks.


The method of allocating ANA Group identifiers is outside the scope of this specification. If the ANA Group
Identifier (refer to Figure 320 and the Identify Namespace data structure in the NVM Command Set
Specification) is cleared to 0h, then the controller shall determine the ANAGRPID that is assigned to that
namespace.


**Namespace Management Examples**


The following is an example of how a host creates a namespace:


1. the host requests the Identify Namespace data structure that specifies common namespace

capabilities (i.e., using an Identify command with the NSID field set to FFFFFFFFh and the CNS
field cleared to 0h);
2. if the controller supports reporting of I/O Command Set specific Namespace Management content

(refer to the Namespace Management section in the applicable I/O Command Set specification),
host software optionally requests that information (e.g., Namespace Granularity).
3. the host determines available resources (e.g., capacity for a namespace that contains formatted

storage) (refer to section 3.8);
4. the host creates the data structure defined in Figure 370 (e.g., taking into account the common

namespace capabilities, available capacity);
5. the host issues the Namespace Management command specifying the Create operation and the

data structure. On successful completion of the command, the Namespace Identifier of the new
namespace is returned in Dword 0 of the completion queue entry. At this point, the new namespace
is not attached to any controller; and


525


NVM Express [®] Base Specification, Revision 2.2


6. if Allocated Namespace Attribute Notices are enabled on the controller, then the host requests the

Identify Namespace data structures (refer to section 1.5.49) for the new namespace to determine
all attributes of the namespace upon receiving an Allocated Namespace Attribute Changed
asynchronous event from that controller.


The following is an example of how a host attaches a namespace:


1. the host issues the Namespace Attachment command specifying the Controller Attach operation

to attach the specified namespace to one or more controllers;
2. the host receives an Attached Namespace Attribute Changed asynchronous event from each

controller that has a namespace newly attached to that controller if Attached Namespace Attribute
Notices are enabled on that controller; and
3. the host receives an Allocated Namespace Attribute Changed asynchronous event from each

controller that has Allocated Namespace Attribute Notices enabled.


The following is an example of how a host detaches a namespace:


1. the host issues the Namespace Attachment command specifying the Controller Detach operation

to detach the specified namespace from one or more controllers;
2. the host receives an Attached Namespace Attribute Changed asynchronous event from each

controller that has a namespace newly detached from that controller if Attached Namespace
Attribute Notices are enabled on that controller; and
3. the host receives an Allocated Namespace Attribute Changed asynchronous event from each

controller that has Allocated Namespace Attribute Notices enabled.


The following is an example of how a host deletes a namespace:


1. the host should detach the namespace from all controllers;
2. the host issues the Namespace Management command specifying the Delete operation for the

specified namespace. On successful completion of the command, the namespace has been
deleted;
3. if the namespace was attached to any controller(s) when deleted:


a. the host receives an Attached Namespace Attribute Changed asynchronous event from

each of those controllers that has Attached Namespace Attribute Notices enabled as
described in section 8.1.15.2; and
b. the host receives an Allocated Namespace Attribute Changed asynchronous event from

each of those controllers that has Allocated Namespace Attribute Notices enabled as
described in section 8.1.15.2;


and


4. if the namespace was not attached to any controller when deleted, the host receives an Allocated

Namespace Attribute Changed asynchronous event from each controller that has Allocated
Namespace Attribute Notices enabled as described in section 8.1.15.2.


**Namespace Deletion Asynchronous Event Reporting**


If a delete operation is requested for a namespace:

  - via a command (e.g., a Namespace Management command or Capacity Management command)
received on the Admin Submission Queue (e.g., not via a Management Endpoint, refer to the NVM
Express Management Interface Specification), then:


`o` each controller, to which the namespace is attached, that has Attached Namespace
Attribute Notices enabled (refer to Figure 392) other than the controller processing that
delete operation, shall issue an Attached Namespace Attribute Changed asynchronous
event as part of the delete operation to indicate a namespace change; and

`o` each controller that has Allocated Namespace Attribute Notices enabled (refer to Figure
392) other than the controller processing that delete operation, shall issue an Allocated
Namespace Attribute Changed asynchronous event as part of the delete operation to
indicate a namespace change;


526


NVM Express [®] Base Specification, Revision 2.2


or

  - via any other method (e.g., a method outside the scope of this specification or via a Management
Endpoint, refer to the NVM Express Management Interface Specification), then:


`o` each controller, to which the namespace is attached, that has Attached Namespace
Attribute Notices enabled (refer to Figure 392) shall issue an Attached Namespace
Attribute Changed asynchronous event as part of the delete operation to indicate a
namespace change; and

`o` each controller that has Allocated Namespace Attribute Notices enabled (refer to Figure
392) shall issue an Allocated Namespace Attribute Changed asynchronous event as part
of the delete operation to indicate a namespace change.


**Namespace Management Considerations for Exported NVM Subsystems (informative)**


A host is able to determine whether an Exported NVM Subsystem supports the Namespace Attachment
command by reading the Commands Supported and Effects log page (refer to section 5.1.12.1.6). The
Namespace Attachment command is used to attach namespaces to controllers and detach namespaces
from controllers. The Namespace Management command is not supported by controllers in an Exported
NVM subsystem.


If an Exported Namespace is detached from a controller in the Exported NVM Subsystem, then the NSID
that referred to that namespace becomes an inactive NSID (refer to section 3.2.1.4) on that controller. If an
Underlying Namespace is disassociated from the Exported NVM Subsystem (refer to section 5.3.7.1.2),
then the NSID of the Exported Namespace that referred to that namespace becomes an unallocated NSID
(refer to section 3.2.1.3) and is not available to any controller in the Exported NVM Subsystem. Previously
submitted but uncompleted or subsequently submitted commands to the namespace that is:

  - detached from a controller; or

  - disassociated from the Exported NVM Subsystem,


are handled by the controller as if they were issued to an inactive NSID (refer to section 3.2.1.4 and Figure
92). Refer to section 8.1.15 for Host actions to attach or detach a specified Namespace.


If an Exported NVM Subsystem Exports an Underlying Namespace that becomes unavailable (e.g.,
detached or deleted) or is affected by a Capacity Management command (e.g., Endurance Group deletion,
NVM Set deletion (refer to section 8.1.4)) then:

  - Previously submitted but uncompleted or subsequently submitted commands to the Exported
Namespace are handled by the controller as if they were issued to an inactive NSID (refer to section
3.2.1.4 and Figure 92); and

  - If Namespace Attribute Notices are enabled controllers affected by Underlying Namespace
changes report a Namespace Attribute Changed asynchronous event to the host as described in
Figure 152.


**Namespace Write Protection**


Namespace Write Protection is an optional configurable controller capability that enables the host to control
the write protection state of a namespace or to determine the write protection state of a namespace. Support
for this capability is reported in the Namespace Write Protection Capabilities (NWPC) field in the Identify
Controller data structure (refer to Figure 313).


Figure 622 defines the write protection states that may be supported for a namespace. All states persist
across power cycles and Controller Level Resets (refer to section 3.7.2) except Write Protect Until Power
Cycle state, which transitions to the No Write Protect state on the occurrence of a power cycle.


527


NVM Express [®] Base Specification, Revision 2.2


**Figure 622: Namespace Write Protection State Definitions**













|M/O|State|Definition|Persistent Across|Col5|
|---|---|---|---|---|
|**M/O**|**State**|**Definition**|**Power**<br>**Cycles**|**Controller**<br>**Level Resets**|
|M|No Write Protect|The namespace is not write protected.|Yes|Yes|
|M|Write Protect|The namespace is write protected.|Yes|Yes|
|O|Write Protect Until<br>Power Cycle|The namespace is write protected until<br>the next power cycle.|No|Yes|
|O|Permanent Write<br>Protect|The namespace is permanently write<br>protected.|Yes|Yes|
|Notes:<br>M – If the Namespace Write Protection capability is supported, then support of this state is mandatory.<br>O – If the Namespace Write Protection capability is supported, then support of this state is optional.|Notes:<br>M – If the Namespace Write Protection capability is supported, then support of this state is mandatory.<br>O – If the Namespace Write Protection capability is supported, then support of this state is optional.|Notes:<br>M – If the Namespace Write Protection capability is supported, then support of this state is mandatory.<br>O – If the Namespace Write Protection capability is supported, then support of this state is optional.|Notes:<br>M – If the Namespace Write Protection capability is supported, then support of this state is mandatory.<br>O – If the Namespace Write Protection capability is supported, then support of this state is optional.|Notes:<br>M – If the Namespace Write Protection capability is supported, then support of this state is mandatory.<br>O – If the Namespace Write Protection capability is supported, then support of this state is optional.|


The Write Protect Until Power Cycle state shall not be used in multi-domain NVM subsystems because
clearing that state requires simultaneous power cycle of the namespace and all controllers to which that
namespace is attached. The result of a command that attempts to use that state in a multi-domain NVM
subsystem is specified in section 5.1.25.1.31.


Figure 623 defines the transition between write protection states. All state transitions are based on Set
Features commands unless otherwise specified. The initial state of a namespace at the time of its creation
is the No Write Protect state.


**Figure 623: Namespace Write Protection State Machine Model**


The Write Protect Until Power Cycle and Permanent Write Protect states are subject to the controls defined
in the Write Protection Control field (refer to Figure 634), which determines whether the controller processes
or aborts Set Features commands which cause a transition into either of these two states (refer to section
8.1.21).


The results of using Namespace Write Protection in combination with an external write protection system
(e.g., TCG Storage Interface Interactions Specification) are outside the scope of this specification.


**Namespace Write Protection – Theory of Operation**


If Namespace Write Protection is supported by the controller, then the controller shall:

  - indicate the level of support for Namespace Write Protection capabilities in the Namespace Write
Protection Capabilities (NWPC) field in the Identify Controller data structure by:


`o` setting the No Write Protect and Write Protect Support bit to ‘1’ in the NWPC field;

`o` setting the Write Protect Until Power Cycle Support bit to ‘1’ in the NWPC field, if the Write
Protect Until Power Cycle state is supported; and


528


NVM Express [®] Base Specification, Revision 2.2


`o` setting the Permanent Write Protect Support bit to ‘1’ in the NWPC field, if the Permanent
Write Protect state is supported;


and

  - support the Namespace Write Protection Config feature (refer to section 5.1.25.1.31).


If the controller supports the Write Protect Until Power Cycle state or the Permanent Write Protect state,
then the controller shall support the Write Protection Control field in the RPMB Device Configuration Block
data structure (refer to section 8.1.21).


The controller shall not set the All Media Read-Only bit to ‘1’ in the Critical Warning field (refer to Figure
207) if the read-only condition on the media is a result of a change in the namespace write protection state
as defined by the Namespace Write Protection State Machine (refer to Figure 623), or due to any
autonomous namespace write protection state transitions (e.g., power cycle). Host software may check the
current namespace write protection state of a namespace using the Get Features command with the
Namespace Write Protection Config Feature Identifier.


If any controller in the NVM subsystem supports Namespace Write Protection, then the write protection
state of a namespace shall be enforced by any controller to which that namespace is attached.


**Namespace Write Protection – Command Interactions**


Unless otherwise noted, the commands listed in Figure 624 are processed normally when specifying an
NSID for a namespace that is write protected.


**Figure 624: Commands Allowed when Specifying a Write Protected NSID**

|Admin Command Set|NVM Command Set|
|---|---|
|Device Self–test|Compare|
|Directive Send1|Dataset Management1|
|Directive Receive3|Read|
|Get Features|Reservation Register|
|Get Log Page|Reservation Report|
|Identify|Reservation Acquire|
|Namespace Attachment|Reservation Release|
|Security Receive1|Vendor Specific1|
|Security Send1|Flush2|
|Set Features1|Verify|
|Vendor Specific1||
|Notes:<br>1.<br>The controller shall fail commands if the specified action attempts to modify the non-volatile storage medium of<br>the specified namespace.<br>2.<br>A Flush command shall complete successfully with no effect. All volatile write cache data and metadata<br>associated with the specified namespace is written to non-volatile storage medium as part of transitioning to the<br>write protected state (refer to section 5.1.25.1.31).<br>3.<br>A Directive Receive command which attempts to allocate streams resources shall be aborted with a status code<br>of Namespace is Write Protected.|Notes:<br>1.<br>The controller shall fail commands if the specified action attempts to modify the non-volatile storage medium of<br>the specified namespace.<br>2.<br>A Flush command shall complete successfully with no effect. All volatile write cache data and metadata<br>associated with the specified namespace is written to non-volatile storage medium as part of transitioning to the<br>write protected state (refer to section 5.1.25.1.31).<br>3.<br>A Directive Receive command which attempts to allocate streams resources shall be aborted with a status code<br>of Namespace is Write Protected.|



Commands not listed in Figure 624, and which meet the following conditions, shall be aborted with a status
code of Namespace Is Write Protected (refer to Figure 102):


a) Commands that specify an NSID for a namespace that is write protected;
b) Commands that specify an NSID for a namespace that is not write protected and the execution of

which would modify another namespace that is write protected (e.g., a Format NVM command);
and
c) Commands that do not specify an NSID, and the execution of which would modify a namespace

that is write protected (e.g., Sanitize command).


529


NVM Express [®] Base Specification, Revision 2.2


**Power Management**


The power management capability allows the host to manage NVM subsystem power statically or
dynamically. Static power management consists of the host determining the maximum power that may be
allocated to an NVM subsystem and setting the NVM Express power state to one that consumes this
amount of power or less. Dynamic power management is illustrated in Figure 625 and consists of the host
modifying the NVM Express power state to best satisfy changing power and performance objectives. This
power management mechanism is meant to complement and not replace autonomous power management
or thermal management performed by a controller.


**Figure 625: Dynamic Power Management**


The number of power states implemented by a controller is returned in the Number of Power States
Supported (NPSS) field in the Identify Controller data structure. If the controller supports this feature, at
least one power state shall be defined and optionally, up to a total of 32 power states may be supported.
Power states shall be contiguously numbered starting with zero such that each subsequent power state
consumes less than or equal to the maximum power consumed in the previous state. Thus, power state
zero indicates the maximum power that the NVM subsystem is capable of consuming.


Associated with each power state is a Power State Descriptor in the Identify Controller data structure (refer
to Figure 314). The descriptors for all implemented power states may be viewed as forming a table as
shown in the example in Figure 626 for a controller with seven implemented power states. Note that Figure
626 is illustrative and does not include all fields in the power state descriptor. The Maximum Power (MP)
field indicates the sustained maximum power that may be consumed in that state, where power
measurement methods are outside the scope of this specification. The controller may employ autonomous
power management techniques to reduce power consumption below this level, but under no circumstances
is power allowed to exceed this level except for non-operational power states as described in section
8.1.17.1.


**Figure 626: Example Power State Descriptor Table**




























|Power<br>State|Maximum<br>Power<br>(MP)|Entry<br>Latency<br>(ENLAT)|Exit<br>Latency<br>(EXLAT)|Relative<br>Read<br>Throughput<br>(RRT)|Relative<br>Read<br>Latency<br>(RRL)|Relative<br>Write<br>Throughput<br>(RWT)|Relative<br>Write<br>Latency<br>(RWL)|
|---|---|---|---|---|---|---|---|
|0|25 W|5 µs|5 µs|0|0|0|0|
|1|18 W|5 µs|7 µs|0|0|1|0|
|2|18 W|5 µs|8 µs|1|0|0|0|
|3|15 W|20 µs|15 µs|2|0|2|0|
|4|10 W|20 µs|30 µs|1|1|3|0|
|5|8 W|50 µs|50 µs|2|2|4|0|
|6|5 W|20 µs|5,000 µs|4|3|5|1|



530


NVM Express [®] Base Specification, Revision 2.2


The Idle Power (IDLP) field indicates the typical power consumed by the NVM subsystem over 30 seconds
in the power state when idle (e.g., there are no pending commands, property accesses, background
processes, nor device self-test operations). The measurement starts after the NVM subsystem has been
idle for 10 seconds.


The Active Power (ACTP) field indicates the largest average power of the NVM subsystem over a 10 second
window on a particular workload (refer to section 8.1.17.3). Active Power measurement starts when the first
command is submitted and ends when the last command is completed. The largest average power over a
10 second window, consumed by the NVM subsystem in that state is reported in the Active Power field. If
the workload completes faster than 10 seconds, the average active power should be measured over the
period of the workload. Non-operational states shall set Active Power Scale, Active Power Workload, and
Active Power fields to 0h.


The host may dynamically modify the power state using the Set Features command and determine the
current power state using the Get Features command. The host may directly transition between any two
supported power states. The Entry Latency (ENLAT) field in the Power State Descriptor data structure
indicates the maximum amount of time in microseconds to enter that power state and the Exit Latency
(EXLAT) field indicates the maximum amount of time in microseconds to exit that state.


The maximum amount of time to transition between any two power states is equal to the sum of the old
state’s exit latency and the new state’s entry latency. The host is not required to wait for a previously
submitted power state transition to complete before initiating a new transition. The maximum amount of
time for a sequence of power state transitions to complete is equal to the sum of transition times for each
individual power state transition in the sequence.


Associated with each power state descriptor are Relative Read Throughput (RRT), Relative Write
Throughput (RWT), Relative Read Latency (RRL) and Relative Write Latency (RWL) fields that provide the
host with an indication of relative performance in that power state. Relative performance values provide an
ordering of performance characteristics between power states. Relative performance values may repeat,
may be skipped, and may be assigned in any order (i.e., increasing power states are not required to have
increasing relative performance values).


A lower relative performance value indicates better performance (e.g., higher throughput or lower latency).
For example, in Figure 626 power state 1 has higher read throughput than power state 2, and power states
0 through 3 all have the same read latency. Relative performance ordering is only with respect to a single
performance characteristic. Thus, although the relative read throughput value of one power state may equal
the relative write throughput value of another power state, this does not imply that the actual read and write
performance of these two power states are equal.


The default NVM Express power state is implementation specific and shall correspond to a state that does
not consume more power than the lowest value specified in the applicable form factor specification, if any.
Refer to the Power Management section in the applicable NVM Express transport specification for transport
specific power requirements impacting NVMe power states, if any.


**Non-Operational Power States**


A power state may be a non-operational power state, as indicated by Non-Operational State (NOPS) field
in Figure 314. Non-operational power states allow the following operations:

  - property accesses;

  - PMR accesses, if any;

  - CMB accesses, if any;

  - processing of Admin commands and processing background operations, if any, initiated by that
command (e.g., Device Self-test command (refer to section 5.1.5), Sanitize command (refer to
section 5.1.22)); and

  - additional transport-specific accesses as defined in the applicable NVMe Transport binding
specification.


531


NVM Express [®] Base Specification, Revision 2.2


For the operations listed in the preceding paragraph, the controller:

  - may exceed the power advertised by the non-operational power state;

  - shall logically remain in the current non-operational power state unless an I/O command is received
or if an explicit transition is requested by a Set Features command with the Power Management
Feature Identifier; and

  - shall not exceed the maximum power advertised for the most recent operational power state.


HMB non-operational power state access restriction (refer to section 5.1.25.2.4) does not prohibit the
controller from accessing the HMB while processing Admin commands and while performing host-initiated
background operations initiated by Admin commands. HMB non-operational power state access restriction
does prohibit the controller from accessing the HMB in order to perform controller-initiated activity (i.e.,
activity not directly associated with a command).


Execution of controller-initiated background operations may exceed the power advertised by the nonoperational power state, if the Non-Operational Power State Permissive Mode is supported and enabled
(refer to section 5.1.25.1.10).


No I/O commands are processed by the controller while in a non-operational power state. The host should
wait until there are no pending I/O commands prior to issuing a Set Features command to change the
current power state of the device to a non-operational power state and not submit new I/O commands until
the Set Features command completes. Issuing an I/O command in parallel may result in the controller being
in an unexpected power state.


When in a non-operational power state, regardless of whether autonomous power state transitions are
enabled, the controller shall autonomously transition back to the most recent operational power state to
process an I/O command.


**Autonomous Power State Transitions**


The controller may support autonomous power state transitions, as indicated in the Identify Controller data
structure in Figure 313. Autonomous power state transitions provide a mechanism for the host to configure
the controller to automatically transition between power states on certain conditions without software
intervention.


The entry condition to transition to the Idle Transition Power State is that the controller has been in idle for
a continuous period of time exceeding the Idle Time Prior to Transition time specified. The controller is idle
when there are no commands outstanding to any I/O Submission Queue. If a controller has an operation in
process (e.g., device self-test operation) that would cause controller power to exceed that advertised for
the proposed non-operational power state, then the controller should not autonomously transition to that
state.


The power state to transition to shall be a non-operational power state (a non-operational power state may
autonomously transition to another non-operational power state). If an operational power state is specified
by a Set Features command specifying the Autonomous Power State Transitions feature (i.e., the Feature
Identifier field set to 0Ch (refer to section 5.1.25.1.6), then the controller should abort the command with a
status code of Invalid Field in Command. Refer to section 8.1.17.1 for more details.


**NVM Subsystem Workloads**


The workload values described in this section may specify a workload hint in the Power Management
Feature (refer to section 5.1.25.1.2) to inform the NVM subsystem or indicate the conditions for the active
power level.


Active power values in the power state descriptors are specified for a particular workload since they may
vary based on the workload of the NVM subsystem. The workload field indicates the conditions to observe
the energy values. If Active Power is indicated for a power state, a corresponding workload shall also be
indicated.


The workload values are described in Figure 627.


532


NVM Express [®] Base Specification, Revision 2.2


**Figure 627: Workload Hints**







|Value|Definition|
|---|---|
|000b|**No Workload:**The workload is unknown or not provided.|
|001b|**Workload 1:**Extended Idle Period with a Burst of Random Writes. Workload #1 consists of five (5)<br>minutes of idle followed by thirty-two (32) random write commands of size 1 MiB submitted to a<br>single controller while all other controllers in the NVM subsystem are idle, and then thirty (30)<br>seconds of idle.|
|010b|**Workload 2:**Heavy Sequential Writes. Workload #2 consists of 80,000 sequential write commands<br>of size 128 KiB submitted to a single controller while all other controllers in the NVM subsystem are<br>idle. The submission queue(s) should be sufficiently large allowing the host to ensure there are<br>multiple commands pending at all times during the workload.|
|011b to 111b|Reserved|


**Runtime D3 (RTD3) Transitions (PCIe only)**



In Runtime D3, main power is removed from the controller. Auxiliary power may or may not be provided.
RTD3 is used for additional power savings when the controller is expected to be idle for a period of time.


In this specification, RTD3 refers to the D3cold power state described in the PCI Express Base Specification.
RTD3 does not include the PCI Express D3hot power state because main power is not removed from the
controller in the D3hot power state. Refer to the PCI Express Base Specification for details on the D3hot
power state and the D3cold power state.


To enable host software to determine when to use RTD3, the controller reports the RTD3 Entry Latency
(RTD3E) field and the RTD3 Resume Latency (RTD3R) field in the Identify Controller data structure in
Figure 313. The host may use the sum of these two values to evaluate whether the expected idle period is
long enough to benefit from a transition to RTD3.


The RTD3 Resume Latency is the expected elapsed time from the time power is applied until the controller
is able to:


a) process and complete I/O commands; and
b) access the resources (e.g., formatted storage) associated with attached namespace(s), if any, as

part of I/O command processing.


The latency reported is based on a normal shutdown with optimal controller settings preceding the RTD3
resume. The latency reported assumes that host software enables and initializes the controller and sends
a 4 KiB read operation.


If CSTS.ST is cleared to ‘0’, then the RTD3 Entry Latency is the expected elapsed time from the time
CC.SHN is set to 01b by host software until CSTS.SHST is set to 10b by the controller. When CSTS.SHST
is set to 10b, the controller is ready for host software to remove power.


**Host Controlled Thermal Management**


A controller may support host controlled thermal management (HCTM), as indicated in the Host Controlled
Thermal Management Attributes of the Identify Controller data structure in Figure 313. Host controlled
thermal management provides a mechanism for the host to configure a controller to automatically transition
between active power states or perform vendor specific thermal management actions in order to attempt to
meet thermal management requirements specified by the host. If active power states transitions are used
to attempt to meet these thermal management requirements specified by the host, then those active power
states transitions are vendor specific.


The host specifies and enables the thermal management requirements by setting the Thermal Management
Temperature 1 field and/or Thermal Management Temperature 2 field (refer to section 5.1.25.1.9) in a Set
Features command to a non-zero value. The supported range of values for the Thermal Management
Temperature 1 field and Thermal Management Temperature 2 field are indicated in the Identify Controller
data structure in Figure 313.


533


NVM Express [®] Base Specification, Revision 2.2


The Thermal Management Temperature 1 specifies that if the Composite Temperature (refer to Figure 208)
is:


a) greater than or equal to this value; and
b) less than the Thermal Management Temperature 2, if non-zero,


then the controller should start transitioning to lower power active power states or perform vendor specific
thermal management actions while minimizing the impact on performance in order to attempt to reduce the
Composite Temperature (e.g., transition to an active power state that performs light throttling).


The Thermal Management Temperature 2 field specifies that if the Composite Temperature is greater than
or equal to this value, then the controller shall start transitioning to lower power active power states or
perform vendor specific thermal management actions regardless of the impact on performance in order to
attempt to reduce the Composite Temperature (e.g., transition to an active power state that performs heavy
throttling).


If the controller is currently in a lower power active power state or performing vendor specific thermal
management actions because of this feature (e.g., throttling performance) because the Composite
Temperature is:


a) greater than or equal to the current value of the Thermal Management Temperature 1 field; and
b) less than the current value of the Thermal Management Temperature 2 field,


and the Composite Temperature decreases to a value below the current value of the Thermal Management
Temperature 1 field, then the controller should return to the active power state that the controller was in
prior to going to a lower power active power state or stop performing vendor specific thermal management
actions because of this feature, the Composite Temperature and the current value of the Thermal
Management Temperature 1 field.


If the controller is currently in a lower power active power state or performing vendor specific thermal
management actions because the Composite Temperature is greater than or equal to the current value of
the Thermal Management Temperature 2 field and the Composite Temperature decreases to a value less
than the current value of the Thermal Management Temperature 1 field, then the controller should return
to the active power state that the controller was in prior to going to a lower power active power state or stop
performing vendor specific thermal management actions because of this feature, and the Composite
Temperature.


The temperature at which the controller stops being in a lower power active power state or performing
vendor specific thermal management actions because of this feature is vendor specific (i.e., hysteresis is
vendor specific).


Figure 628 shows examples of how the Composite Temperature may be affected by this feature.


534


NVM Express [®] Base Specification, Revision 2.2


**Figure 628: HCTM Example**


TMT2


TMT1


Vendor
Specific




|Col1|Col2|Col3|e.g., heavy thottling<br>e.g., light throttle<br>No Thermal Management|
|---|---|---|---|
|||||
|Lines represent the<br>Composite Temperature|Lines represent the<br>Composite Temperature|Lines represent the<br>Composite Temperature|Lines represent the<br>Composite Temperature|



Note: Since the host controlled thermal management (HCTM) feature uses the Composite Temperature,
the actual interactions between a platform (e.g., tablet, or laptop) and two different device implementations
may vary even with the same Thermal Management Temperature 1 and Thermal Management
Temperature 2 temperature settings. The use of this feature requires validation between those devices’
implementations and the platform in order to be used effectively.


The SMART / Health Information log page (refer to section 5.1.12.1.3) contains statistics related to Host
Controller Thermal Management.


**Predictable Latency Mode**


Predictable Latency Mode is used to achieve predictable latency for read and write operations. When
configured to operate in this mode using the Predictable Latency Mode Config Feature (refer to section
5.1.25.1.12), the namespaces in an NVM Set (refer to section 3.2.2) provide windows of operation for
deterministic operation or non-deterministic operation.


When Predictable Latency Mode is enabled:

  - NVM Sets and their associated namespaces have vendor specific quality of service attributes;

  - I/O commands that access NVM in the same NVM Set have the same quality of service attributes;
and

  - I/O commands that access NVM in one NVM Set do not impact the quality of service of I/O
commands that access NVM in a different NVM Set.


The quality of service attributes apply within the NVM subsystem and do not include the PCIe or fabric
connection. To enhance isolation, the host should submit I/O commands for different NVM Sets to different
I/O Submission Queues.


535


NVM Express [®] Base Specification, Revision 2.2


Read Recovery Levels (refer to section 8.1.20) shall be supported when Predictable Latency Mode is
supported. The host configures the Read Recovery Level to specify the tradeoff between the quality of
service versus the amount of error recovery to apply for a particular NVM Set.


The Deterministic Window (DTWIN) is the window of operation during which the NVM Set is able to provide
deterministic latency for read and write operations. The Non-Deterministic Window (NDWIN) is the window
of operation during which the NVM Set is not able to provide deterministic latency for read and write
operations as a result of preparing for a subsequent Deterministic Window. Examples of actions that may
be performed in the Non-Deterministic Window include background operations on the non-volatile storage
media. The current window that an NVM Set is operating in is configured by the host using the Predictable
Latency Mode Window Feature or by the controller as a result of an autonomous action.


**Figure 629: Deterministic and Non-Deterministic Windows**


To remain in the Deterministic Window, the host is required to follow operating rules (refer to section
8.1.18.1) ensuring that certain attributes do not exceed the typical or maximum values indicated in the
Predictable Latency Per NVM Set log page. If the attributes exceed any of the typical or maximum values
indicated in the Predictable Latency Per NVM Set log page or a Deterministic Excursion occurs, then the
associated NVM Set may autonomously transition to the Non-Deterministic Window. A Deterministic
Excursion is a rare occurrence in the NVM subsystem that requires immediate action by the controller.


The host configures Predictable Latency Events to report using the Predictable Latency Mode Config
feature. The host may configure a Predictable Latency Event to be triggered when that value exceeds a
specific value in order to manage window changes and avoid autonomous transitions by the controller.
Refer to section 8.1.18.3.


If Predictable Latency Mode is supported, then all controllers in the NVM subsystem shall:

  - Support one or more NVM Sets;

  - Support Read Recovery Levels;

  - Support the Predictable Latency Mode log page for each NVM Set;

  - Support the Predictable Latency Event Aggregate log page;

  - Support the Predictable Latency Mode Config Feature;

  - Support the Predictable Latency Mode Window Feature;

  - Support Predictable Latency Event Aggregate Log Change Notices; and

  - Indicate support for Predictable Latency Mode in the Controller Attributes field in the Identify
Controller data structure.


**Host Operating Rules to Achieve Determinism**


In order to achieve deterministic operation, the host is required to follow operating rules.


An NVM Set remains in the Deterministic Window while attributes do not exceed any of the typical or
maximum values indicated in the Predictable Latency Per NVM Set log page, there is not a Deterministic
Excursion, and the host does not request a transition to the Non-Deterministic Window. The attributes


536


NVM Express [®] Base Specification, Revision 2.2


specified in this specification are the number of random 4 KiB reads, the number of writes in Optimal Write
Size, and time in the Deterministic Window. Additional attributes are vendor specific.


For reads, writes, and time in the Deterministic Window, two values are provided in the Predictable Latency
Per NVM Set log page (refer to section 5.1.12.1.11):

  - A typical or maximum amount of that attribute that the host may consume during any given DTWIN;
and

  - A reliable estimate of the amount of that attribute that remains to be consumed during the current
DTWIN.


Figure 630 shows how the Typical, Maximum, and Reliable Estimates for the DTWIN attributes increase or
decrease when the associated NVM Set is in the Deterministic Window or Non-Deterministic Window.


**Figure 630: DTWIN Attributes and Estimates**


An NVM Set may transition autonomously to the NDWIN if, since entry to the current DTWIN:


a) the number of reads is greater than the value indicated in the DTWIN Reads Typical field;
b) the number of writes is greater than the value indicated in the DTWIN Writes Typical field;
c) the amount of time indicated in the DTWIN Time Maximum field has passed; or
d) a Deterministic Excursion occurs.


Figure 631 is an example that shows the relationship between the typical and reliable estimate values for
DTWIN Reads. DTWIN Reads Reliable Estimate begins near the DTWIN Reads Typical value at the start
of the current DTWIN at time 0. During the first time increment, the host reads _x_ units, and the value of the
reliable estimate at time t2 is decremented by approximately _x_ . During the second time increment, the host
reads a smaller amount consisting of _y_ units and thus the reliable estimate at t3 is decremented by
approximately _y_ .


537


NVM Express [®] Base Specification, Revision 2.2


**Figure 631: Typical and Reliable Estimate Example**


The host configures the current window to be either DTWIN or NDWIN using a Set Features command with
the Predictable Latency Mode Window Feature. The host may use the reliable estimates provided in the
Predictable Latency Mode log page to ensure that the host transitions the NVM Set to the NDWIN prior to
any reliable estimates exceeding one of the typical or maximum values (e.g., DTWIN Reads Estimate = 0).


The reliable estimates provided shall have the following properties when in the Deterministic Window:

  - The estimates shall be monotonically decreasing towards 0h for the entirety of the DTWIN,
depending on the attribute. For example, DTWIN Reads Reliable Estimate is monotonically
decreasing and thus does not increase without transitioning from the DTWIN to the NDWIN; and

  - The estimates shall not change abruptly unless operating conditions have changed abruptly. The
estimate should be based on averaging or smoothing of data collected over some period of time.


**Configuring Periodic Windows**


When using the NVM Set in Predictable Latency Mode, the host should transition the controller to NDWIN
for periodic maintenance. The maintenance is required in order for the NVM subsystem to reliably provide
the amount of time indicated for Deterministic Windows.


There are three static time based parameters reported in the Predictable Latency Per NVM Set log page
(refer to section 5.1.12.1.11) that may be used by the host to configure periodic windows. The values
provided are worst-case for the life of the NVM subsystem:

  - NDWIN Time Minimum Low is the minimum time that the NVM Set remains in the Non-Deterministic
Window. The controller may delay completion of a Set Features command requesting a transition
to the Deterministic Window until this time is completed. This time does not account for additional
host activity in the Non-Deterministic Window;

  - NDWIN Time Minimum High is the minimum time that the host should allow the NVM Set to remain
in the Non-Deterministic Window after the NVM Set remained in the previous Deterministic Window
for DTWIN Time Maximum. This time does not account for additional host activity in the NonDeterministic Window; and

  - DTWIN Time Maximum is the maximum time that the NVM Set is able to stay in a Deterministic
Window.


538


NVM Express [®] Base Specification, Revision 2.2


The DTWIN Time Maximum and NDWIN Time Minimum High may provide a ratio of the amount of
maintenance that needs to be performed based on the time that the NVM Set remains in the DTWIN,
assuming no threshold is exceeded. Any scaling of the time in the Non-Deterministic Window based on the
read, write, and time behavior in the previous Deterministic Window is implementation dependent.


The DTWIN Time Estimate may be used by the host when a Deterministic Excursion has occurred. This
estimate allows the host to re-synchronize an NVM Set with other NVM Sets operating in Predictable
Latency Mode, if applicable.


**Configuring and Managing Events**


The host may configure events to be triggered when thresholds do not exceed certain levels or when
autonomous transitions occur using the Predictable Latency Mode Feature. The host submits a Set Feature
command for the particular NVM Set and configures the specific event(s) and threshold(s) values that shall
trigger a Predictable Latency Event Aggregate Log Change Notice event for that particular NVM Set to the
host. Refer to Figure 405.


The host determines the NVM Sets that have outstanding events by reading the Predictable Latency Event
Aggregate log page (refer to section 5.1.12.1.12). An entry is returned for each NVM Set that has an event
outstanding. The host may use the NVM Set Identifier Maximum value reported in the Identify Controller
data structure in order to determine the maximum size of this log page.


To determine the specific event(s) that have occurred for a reported NVM Sets, the host reads the
Predictable Latency Per NVM Set log page (refer to section 5.1.12.1.11) for that NVM Set. The Event Type
field indicates the event(s) that have occurred (e.g., an autonomous transition to the NDWIN). An event(s)
for a particular NVM Set is cleared if the controller successfully processes a read for the Predictable Latency
Per NVM Set log page for the affected NVM Set where the Get Log Page command has the Retain
Asynchronous Event parameter cleared to ‘0’. If the Event Type field in the Predictable Latency Per NVM
Set log page is cleared to 0h, then events for that particular NVM Set are not reported in the Predictable
Latency Event Aggregate log page.


**Reachability Reporting architecture**


**Reachability Reporting overview**


For some operations that specify multiple namespaces it is necessary to indicate what namespaces are
able to be used in those operations (e.g., Copy command that specifies multiple namespaces, Execute
command in the Computational Programs command set). This ability is called reachability. Reachability is
defined at the controller level (i.e., only namespaces attached to the same controller are reachable).


A Reachability Group becomes available to a controller if:


a) a namespace becomes attached to that controller and that namespace is associated with a

Reachability Group that did not currently have any namespaces attached to that controller; or
b) a configuration change in an NVM subsystem changes the membership in a Reachability Group

(e.g., a new Reachability Group is present in the Reachability Groups log page (refer to section
5.1.12.1.25)).


A Reachability Group becomes unavailable to a controller if a namespace is detached that is the only
namespace attached to that controller for that Reachability Group (i.e., a Reachability Group that was
present in the Reachability Groups log page is no longer present).


A Reachability Association change occurs if a Reachability Group that is associated with that Reachability
Association becomes available or unavailable to that controller. (e.g., a new Reachability Association is
present in the Reachability Associations log page (refer to section 5.1.12.1.26) or a Reachability Association
that was present in the Reachability Associations log page is no longer present).


If an NVM subsystem supports Reachability Reporting, then all controllers in that NVM subsystem shall:

  - set the RRSUP bit to ‘1’ in the Controller Reachability Capabilities (CRCAP) field in the Identify
Controller data structure (refer to Figure 313) to indicate support for Reachability Reporting;

  - support Reachability Groups Change Notices (refer to section 5.1.25.1.5);


539


NVM Express [®] Base Specification, Revision 2.2


  - support Reachability Association Change Notices (refer to section 5.1.25.1.5);

  - support the Reachability Groups log page; and

  - support the Reachability Associations log page.


Namespaces attached to a controller in an NVM subsystem that supports Reachability Reporting shall:

  - be members of a Reachability Group; and

  - supply a valid Reachability Group Identifier in the Reachability Group Identifier (RGRPID) field in
the I/O Command Set Independent Identify Namespace Data Structure (refer to Figure 320).


Reachability and characteristics of reachability are indicated in the combination of the Reachability Groups
log page (refer to section 5.1.12.1.25) and the Reachability Associations log page (refer to section
5.1.12.1.26). A Reachability Group defines a group of namespaces that are all associated with namespaces
in other Reachability Groups defined by a Reachability Association. The method of assigning Reachability
Group identifiers and Reachability Association identifiers is outside the scope of this specification. If
members of a Reachability Group are able to reach members of that Reachability Group, then a
Reachability Association that contains only that Reachability Group specifies the characteristics of that
reachability. All Reachability Groups in a Reachability Association have identical access characteristics. All
namespaces in a Reachability Group have identical access characteristics. If a Reachability Group is not
in any Reachability Association then the members of that Reachability Group are not reachable by any
other namespaces, including the members of that Reachability Group. A namespace is always able to reach
itself (i.e., a command that has two or more NSIDs as part of the command where those NSIDs are all the
same is not constrained by reachability).


If the Reachability Association Characteristics field (refer to Figure 279) is set to is 01h, then all namespaces
in the associated Reachability Groups are able to reach other namespaces in the other Reachability Groups
in that Reachability Association without any indication of a performance characteristic (e.g., for the Execute
command in the Computational Programs Command Set). If the Reachability Association Characteristics
field is set to 02h, then all namespaces in the associated Reachability Groups are reachable and support
fast copy operations as defined by the applicable I/O Command Set specification (e.g., the Fast copy
operations section in the NVM Command Set Specification). If the Reachability Association Characteristics
field is set to 03h, then all namespaces in the associated Reachability Groups are reachable but do not
support fast copy operations.


A namespace is only allowed to be in one Reachability Group. A Reachability Group is in zero or more
Reachability Associations with different values of the Reachability Association Characteristics field for each
Reachability Association.


The Reachability Group Identifier (RGRPID) for each Reachability Group shall be unique within the NVM
subsystem. If RGIDC bit in the CRCAP field in the Identify Controller data structure is set to ‘1’, then the
Reachability Group Identifier shall not change while the namespace is attached to any controller in the NVM
subsystem. If RGIDC bit in the CRCAP field is cleared to ‘0’, then the Reachability Group Identifier may
change while the namespace is attached to any controller in the NVM subsystem. If the Reachability Group
Identifier changes, the controller shall issue the Reachability Groups Change Notice as described in this
section.


Figure 632 is an example configuration that shows that:

  - Reachability Association 1 (i.e., RA 1):


`o` specifies that:


      - NSID 10 and NSID 30 are able to reach each other; and

      - NSID 10 and NSID 31 are able to reach each other;


and


`o` does not specify any reachability between NSID 30 and NSID 31;

  - Reachability Association 2 (i.e., RA 2) is a self-reference for Reachability Group A (i.e., RG A) that
specifies:


540


NVM Express [®] Base Specification, Revision 2.2


`o` that NSID 30 and NSID 31 are able to reach each other;

  - Reachability Association 3 (i.e., RA 3):


`o` specifies that:


      - NSID 11 and NSID 30 are able to reach each other; and

      - NSID 11 and NSID 31 are able to reach each other;


and


`o` does not specify any reachability between NSID 30 and NSID 31;

  - The lack of a Reachability Association that contains Reachability Group B (i.e., RG B) and
Reachability Group D (i.e., RG D) specifies:


`o` that NSID 10 and NSID 11 are not able to reach each other;


and

  - The lack of a self-referencing Reachability Association for Reachability Group E (i.e., RG E)
specifies:


`o` that NSID 22 and NSID 23 are not able to reach each other.


**Figure 632: Reachability Associations Example**



























**Reachability event notifications**


Reachability may generate a Reachability Group Change notice (refer to section 5.1.2.1) or a Reachability
Association Change notice (refer to section 5.1.2.1).


Receipt of a Reachability Group Change Notice from a controller may indicate:


a) an NSID has been added to one or more of the Reachability Group Descriptors;
b) an NSID has been removed from one or more of the Reachability Group Descriptors;
c) a Reachability Group no longer has any NSIDs attached to this controller as members of that

Reachability Group and therefore is no longer reported in the Reachability Groups log page for this
controller; or
d) the NSID of a namespace has moved from one Reachability Group Descriptor to a different

Reachability Group Descriptor (i.e., the RGRPID field in the I/O Command Set Independent Identify


541


NVM Express [®] Base Specification, Revision 2.2


Namespace Data Structure for that namespace has changed), if RGIDC bit in the CRCAP field is
cleared to ‘0’ in the Identify Controller data structure (refer to Figure 313).


As a result of receiving a Reachability Group Change notice, the host should read the Reachability Groups
log page (refer to section 5.1.12.1.25) to check for each of those possible changes.


Receipt of a Reachability Association Change Notice from a controller may indicate:


a) an RGID has been added to one or more of the Reachability Association Descriptors;
b) an RGID has been removed from one or more of the Reachability Association Descriptors; and/or
c) a Reachability Association no longer has any RGIDs associated with this controller as members of

that Reachability Association and therefore is no longer reported in the Reachability Associations
log page for this controller.


As a result of receiving a Reachability Association Change notice, the host should read the Reachability
Associations log page (refer to section 5.1.12.1.26) to check for each of those possible changes.


**Read Recovery Level**


The Read Recovery Level (RRL) is an NVM Set configurable attribute that balances the completion time
for read commands and the amount of error recovery applied to those read commands. The Read Recovery
Level applies to an NVM Set with which the Read Recovery Level is associated. A namespace created
within an NVM Set inherits the Read Recovery Level of that NVM Set. If NVM Sets are not supported, all
namespaces in the NVM subsystem use an identical Read Recovery Level.


The controller indicates support for Read Recovery Levels in the Controller Attributes field in the Identify
Controller data structure (refer to Figure 313). If Read Recovery Levels are supported, then the specific
levels supported are indicated in the Read Recovery Levels Supported field in the Identify Controller data
structure. There are 16 levels that may be supported. Level 0, if supported, provides the maximum amount
of recovery. Level 4 is a mandatory level that provides a nominal amount of recovery and is the default
level. Level 15 is a mandatory level that provides the minimum amount of recovery and is referred to as the
‘Fast Fail’ level. The levels are organized based on the amount of recovery supported, such that a higher
numbered level provides less recovery than the preceding lower level.


Interactions between the Read Recovery Level and the Limited Retry (LR) field in I/O commands are
implementation specific.


The Read Recovery Level may be configured using a Set Features command for the Read Recovery Level
Config Feature. The Read Recovery Level may be determined using a Get Features command for the Read
Recovery Level Config Feature.


542


NVM Express [®] Base Specification, Revision 2.2


**Figure 633: Read Recovery Level Overview**


Maximum
Recovery


Minimum
Recovery

|Level|O/M|Definition|
|---|---|---|
|0|O||
|1|O||
|2|O||
|3|O||
|4|M|Default|
|5|O||
|6|O||
|7|O||
|8|O||
|9|O||
|10|O||
|11|O||
|12|O||
|13|O||
|14|O||
|15|M|Fast Fail|



If Read Recovery Levels are supported, then the NVM subsystem and all controllers shall:

  - Support at least Level 4 and Level 15;

  - Indicate support for Read Recovery Levels in the Controller Attributes field in the Identify Controller
data structure;

  - Support the Read Recovery Levels Supported field in the Identify Controller data structure; and

  - Support the Read Recovery Level Config Feature.


**Replay Protected Memory Block**


The Replay Protected Memory Block (RPMB) provides a means for the system to store data to a specific
memory area in an authenticated and replay protected manner. This is provided by first programming
authentication key information to the controller that is used as a shared secret. The system is not
authenticated in this phase, therefore the authentication key programming should be done in a secure
environment (e.g., as part of the manufacturing process). The authentication key is utilized to sign the read
and write accesses made to the replay protected memory area with a Message Authentication Code (MAC).
Use of random number (nonce) generation and a write count property provide additional protection against
replay of messages where messages could be recorded and played back later by an attacker.


Any attempt to access the replay protected memory area prior to the Authentication Key being programmed
results in an RPMB Operation Result Operation Status field set to 07h (i.e., Authentication Key not yet


543


NVM Express [®] Base Specification, Revision 2.2


programmed) (refer to Figure 636). Once the key is programmed, the RPMB Operation Result Operation
Status field shall not be set to 07h.


An Authenticated Data Write to the RPMB Device Configuration Block data structure that attempts to set
the Boot Partition Write Protection Enabled bit when RPMB Boot Partition Write Protection is not supported
results in an RPMB Operation Result Operation Status of 05h (i.e., Write failure in the RPMB Operation
Status field) (refer to Figure 636).


An Authenticated Data Write to the RPMB Device Configuration Block data structure that attempts to set
the Boot Partition Write Protection Enabled bit when either Boot Partition is in the Write Locked Until Power
Cycle state (refer to section 5.1.25.1.32 and section 8.1.3.3.1) results in an RPMB Operation Result
Operation Status of 05h (i.e., Write failure in the RPMB Operation Status field) (refer to Figure 636).


An Authenticated Data Write to the RPMB Device Configuration Block data structure that attempts to
change either the Boot Partition 0 Write Locked bit or the Boot Partition 1 Write Locked bit when the Boot
Partition Write Protection Enabled bit is cleared to ‘0’ results in an RPMB Operation Result Operation Status
field set to 05h (i.e., Write failure) (refer to Figure 636).


If Set Features Boot Partition Write Protection is supported, then an Authenticated Data Write to the RPMB
Device Configuration Block data structure that successfully enables RPMB Boot Partition Write Protection
shall also result in the controller changing the Boot Partition 0 Write Protection State and Boot Partition 1
Write Protection State values in the Boot Partition Write Protection Config feature to a value of 100b to
indicate that Boot Partition write protection is controlled by RPMB.


The controller may support multiple RPMB targets. RPMB targets are not contained within a namespace.
Controllers in the NVM subsystem may share the same RPMB targets. Security Send and Security Receive
commands for RPMB do not use the namespace ID field; NSID shall be cleared to 0h. Each RPMB target
operates independently – there may be requests outstanding to multiple RPMB targets at once (where the
requests may be interleaved between RPMB targets). In order to guarantee ordering the host should issue
and wait for completion for one Security Send or Security Receive command at a time. Each RPMB target
requires individual authentication and key programming. Each RPMB target may have its own unique
Authentication Key.


The message types defined in Figure 635 are used by the host to communicate with an RPMB target.
Request Message Types are sent from the host to the controller using Security Send commands. Response
Message Types are retrieved by the host from the controller using Security Receive commands.


Figure 634 defines the RPMB Device Configuration Block data structure – the non-volatile contents stored
within the controller for RPMB target 0.


**Figure 634: RPMB Device Configuration Block Data Structure**









|Bytes|Type|Description|
|---|---|---|
|00|RW|**Boot Partition Protection Enable (BPPEE):** This field specifies whether Boot Partition Protection<br>is enabled.<br>**Bits**<br>**Description**<br>7:1<br>Reserved<br>0 <br>**Boot Partition Write Protection Enabled (BPPED):** If this bit is set to ‘1’, then<br>RPMB Boot Partition Write Protection is enabled. If this bit is cleared to ‘0’, then<br>RPMB Boot Partition Write Protection is disabled or not supported. Once enabled,<br>the controller shall prevent disabling RPMB Boot Partition Write Protection.<br>|


|Bits|Description|
|---|---|
|7:1|Reserved|
|0|**Boot Partition Write Protection Enabled (BPPED):** If this bit is set to ‘1’, then<br>RPMB Boot Partition Write Protection is enabled. If this bit is cleared to ‘0’, then<br>RPMB Boot Partition Write Protection is disabled or not supported. Once enabled,<br>the controller shall prevent disabling RPMB Boot Partition Write Protection.|


544


NVM Express [®] Base Specification, Revision 2.2


**Figure 634: RPMB Device Configuration Block Data Structure**






|Bits|Description|
|---|---|
|7:2|Reserved|
|1|**Boot Partition 1 Write Locked (BPP1L):** If this bit is set to ‘1’, then Boot Partition 1<br>(i.e., the BPID bit in Figure 182 is set to 1) is write locked. If this bit is cleared to ‘0’,<br>then the Boot Partition 1 is write unlocked.|
|0|**Boot Partition 0 Write Locked (BPP0L):**If this bit is set to ‘1’, then Boot Partition 0<br>(i.e., the BPID bit in Figure 182 is cleared to 0) is write locked. If this bit is cleared to<br>‘0’, then the Boot Partition 0 is write unlocked.|












|Bits|Description|
|---|---|
|7:2|Reserved|
|1|**Permanent Write Protect Control (PWPC):**This bit cleared to ‘0’ specifies that the<br>controller shall fail a Set Features command which attempts to set the namespace<br>write protection state to Permanent Write Protect, as defined in section 8.1.16. This<br>bit set to ‘1’ specifies that the controller shall process a Set Features command which<br>attempts to set the namespace write protection state to Permanent Write Protect.<br>If the controller supports Namespace Write Protection, then this bit shall be cleared<br>to ‘0’ after a power cycle or a Controller Level Reset.|
|0|**Write Protect Until Power Cycle Control (WPUPCC):** This bit cleared to ‘0’<br>specifies that the controller shall fail a Set Features command which attempts to set<br>the namespace write protection state to Write Protect Until Power Cycle, as defined<br>in section 8.1.16. This bit set to ‘1’ specifies that the controller shall process a Set<br>Features command which sets the namespace write protection state to Write Protect<br>Until Power Cycle.<br>If the controller supports Namespace Write Protection, then this bit shall be cleared<br>to ‘0’ after a power cycle or a Controller Level Reset.|



|Bytes|Type|Description|
|---|---|---|
|01|RW|**Boot Partition Protection State (BPLS):**This field specifies the current Boot Partition protection<br>state when RPMB Boot Partition Write Protection is enabled. This field shall be cleared to 0h unless<br>RPMB Boot Partition Write Protection is enabled. Refer to section 8.1.3.3.<br>**Bits**<br>**Description**<br>7:2<br>Reserved<br>1 <br>**Boot Partition 1 Write Locked (BPP1L):** If this bit is set to ‘1’, then Boot Partition 1<br>(i.e., the BPID bit in Figure 182 is set to 1) is write locked. If this bit is cleared to ‘0’,<br>then the Boot Partition 1 is write unlocked.<br>0 <br>**Boot Partition 0 Write Locked (BPP0L):**If this bit is set to ‘1’, then Boot Partition 0<br>(i.e., the BPID bit in Figure 182 is cleared to 0) is write locked. If this bit is cleared to<br>‘0’, then the Boot Partition 0 is write unlocked.<br>|
|02|RW|**Write Protection Control (WPC):** This field specifies whether the controller processes or aborts<br>Set Features commands which enable certain namespace write protection states (refer to section<br>8.1.16 and section 5.1.25.1.31). If the controller does not support Namespace Write Protection,<br>then this field shall be cleared to 0h.<br>**Bits**<br>**Description**<br>7:2<br>Reserved<br>1 <br>**Permanent Write Protect Control (PWPC):**This bit cleared to ‘0’ specifies that the<br>controller shall fail a Set Features command which attempts to set the namespace<br>write protection state to Permanent Write Protect, as defined in section 8.1.16. This<br>bit set to ‘1’ specifies that the controller shall process a Set Features command which<br>attempts to set the namespace write protection state to Permanent Write Protect.<br>If the controller supports Namespace Write Protection, then this bit shall be cleared<br>to ‘0’ after a power cycle or a Controller Level Reset.<br>0 <br>**Write Protect Until Power Cycle Control (WPUPCC):** This bit cleared to ‘0’<br>specifies that the controller shall fail a Set Features command which attempts to set<br>the namespace write protection state to Write Protect Until Power Cycle, as defined<br>in section 8.1.16. This bit set to ‘1’ specifies that the controller shall process a Set<br>Features command which sets the namespace write protection state to Write Protect<br>Until Power Cycle.<br>If the controller supports Namespace Write Protection, then this bit shall be cleared<br>to ‘0’ after a power cycle or a Controller Level Reset.<br>|
|511:03||Reserved|


**Figure 635: RPMB Request and Response Message Types**









|Request Message Types|Col2|Description|Requires<br>Data|RPMB Frame<br>Length<br>(bytes)|
|---|---|---|---|---|
|0001h|Authentication<br>key<br>programming request|The host is attempting to program the Authentication<br>Key for the selected RPMB target to the controller.|No|256|
|0002h|Reading of the Write<br>Counter value request|The host is requesting to read the current Write<br>Counter value from the selected RPMB target.|No|256|
|0003h|Authenticated data write<br>request|The host is attempting to write data to the selected<br>RPMB target.|Yes|M + 256|
|0004h|Authenticated data read<br>request|The host is attempting to read data from the selected<br>RPMB target.|No|256|
|0005h|Result read request|The host is attempting to read the result code for any<br>of the other Message Types.|No|256|


545


NVM Express [®] Base Specification, Revision 2.2


**Figure 635: RPMB Request and Response Message Types**




















|Request Message Types|Col2|Description|Requires<br>Data|RPMB Frame<br>Length<br>(bytes)|
|---|---|---|---|---|
|0006h|Authenticated<br>Device<br>Configuration Block write<br>request|The host is attempting to write Device Configuration<br>Block (DCB) to the selected RPMB target. This<br>request message type is only valid for RPMB target<br>0.|Yes|512 + 256|
|0007h|Authenticated<br>Device<br>Configuration Block read<br>request|The host is attempting to read Device Configuration<br>Block (DCB) from the selected RPMB target. This<br>request message type is only valid for RPMB target<br>0.|No|256|
|0100h|Authentication<br>key<br>programming response|Returned as a result of the host requesting a Result<br>read request Message Type after programming the<br>Authentication Key.|No|256|
|0200h|Reading of the Write<br>Counter value response|Returned as a result of the host requesting a Result<br>read request Message Type after requesting the<br>Write Counter value.|No|256|
|0300h|Authenticated data write<br>response|Returned as a result of the host requesting a Result<br>read request Message Type after attempting to write<br>data to an RPMB target.|No|256|
|0400h|Authenticated data read<br>response|Returned as a result of the host requesting a Result<br>read request Message Type after attempting to read<br>data from an RPMB target.|Yes|M + 256|
|0600h|Authenticated<br>Device<br>Configuration data write<br>response|Returned as a result of the host requesting a Result<br>read request Message Type after attempting to write<br>a Device Configuration Block to an RPMB target.|No|256|
|0700h|Authenticated<br>Device<br>Configuration data read<br>response|Returned as a result of the host requesting a Result<br>read request Message Type after attempting to read<br>DCB from an RPMB target.|Yes|512 + 256|



The operation result defined in Figure 636 indicates whether an RPMB request was successful or not.


**Figure 636: RPMB Operation Result**






|Bits|Description|
|---|---|
|15:08|Reserved|
|07|**Write Counter Status (WCS):**Indicates if the Write Counter has expired (i.e., reached its maximum value).<br>A value of ‘1’ indicates that the Write Counter has expired. A value of ‘0’ indicates a valid Write Counter.|
|06:00|**Operation Status (OPSTAT):**Indicates the operation status. Valid operation status values are listed below.<br>**Value**<br>**Definition**<br>00h<br>Operation successful<br>01h<br>General failure<br>02h<br>Authentication failure (MAC comparison not matching, MAC calculation failure)<br>03h<br>Counter failure (counters not matching in comparison, counter incrementing failure)<br>04h<br>Address failure (address out of range, wrong address alignment)<br>05h<br>Write failure (data/counter/result write failure)<br>06h<br>Read failure (data/counter/result read failure)<br>07h<br>Authentication Key not yet programmed<br>08h<br>Invalid RPMB Device Configuration Block – this may be used when the target is not 0h.<br>09 to 3Fh<br>Reserved|


|Value|Definition|
|---|---|
|00h|Operation successful|
|01h|General failure|
|02h|Authentication failure (MAC comparison not matching, MAC calculation failure)|
|03h|Counter failure (counters not matching in comparison, counter incrementing failure)|
|04h|Address failure (address out of range, wrong address alignment)|
|05h|Write failure (data/counter/result write failure)|
|06h|Read failure (data/counter/result read failure)|
|07h|Authentication Key not yet programmed|
|08h|Invalid RPMB Device Configuration Block – this may be used when the target is not 0h.|
|09 to 3Fh|Reserved|



Figure 637 defines the non-volatile contents stored within the controller for each RPMB target.


546


NVM Express [®] Base Specification, Revision 2.2


**Figure 637: RPMB Contents**


















|Content|Type|Size|Description|
|---|---|---|---|
|Authentication<br>Key|Write once,<br>not erasable<br>or readable|Size is dependent on<br>authentication method<br>reported in Identify<br>Controller data structure<br>(e.g., SHA-256 is 32 bytes<br>(refer to RFC 6234))|Authentication key which is used to authenticate<br>accesses when MAC is calculated.|
|Write Counter|Read only|4 bytes|Counter value for the total amount of successful<br>authenticated data write requests made by the host.<br>The initial value of this property after manufacture is<br>00000000h. The value is incremented by one<br>automatically by the controller with each successful<br>programming access. The value is not resettable.<br>After the counter has reached the maximum value<br>of FFFFFFFFh, the controller shall no longer<br>increment to prevent overflow.|
|RPMB Data<br>Area|Readable<br>and writable,<br>not erasable|Size is reported in Identify<br>Controller data structure<br>(128 KiB minimum, 32 MiB<br>maximum)|Data that is able to be read and written only via<br>successfully authenticated read/write access.|



Each RPMB Data Frame is 256 bytes in size plus the size of the Data field, and is organized as shown in
Figure 638. RPMB uses a sector size of 512 bytes. The RPMB sector size is independent and not related
to the user data size used for the namespace(s).


**Figure 638: RPMB Data Frame**







|Bytes|Description|
|---|---|
|222-_N_:00|**Stuff Bytes (STBY):** Padding for the frame. Values in this field are not part of the MAC<br>calculation. The size is 223 bytes minus the size of the Authentication Key (_N_).|
|_222:222-(N-1)_|**Message Authentication Code / Authentication Key (MAC/Key):** Size is dependent on<br>authentication method reported in the Identify Controller data structure (e.g., SHA-256 key is 32<br>bytes (refer to RFC 6234)).|
|_223_|**RPMB Target (RBT):** Indicates which RPMB this Request/Response is targeted for. Values 0-6<br>are supported. If the value in this field is not equal to the NVMe Security Specific Field (NSSF) in<br>the Security Send or Security Receive command, then the controller shall return an error of Invalid<br>Field in Command for the Security Send or Security Receive command.|
|_239:224_|**Nonce (NCE):** Random number generated by the host for the requests and copied to the<br>response by the RPMB target.|
|_243:240_|**Write Counter (WCNTR):** Total amount of successfully authenticated data write requests.|
|_247:244_|**Address (ADDR):** Starting address of data to be programmed to or read from the RPMB.|
|_251:248_|**Sector Count (SCNT):** Number of sectors (512 bytes) requested to be read or written.|
|_253:252_|**Result (RSLT):**Defined in Figure 636. Note: The Result field is not needed for Requests.|
|_255:254_|**Request or Response Message (RRM):** Defined in Figure 635.|
|_(M-1)+256:256_|**Data (DATA):** Data to be written or read by signed access where_M_ = 512 * Sector Count. This<br>field is optional.|


Security Send and Security Receive commands are used to encapsulate and deliver data packets of any
security protocol between the host and controller without interpreting, dis-assembling or re-assembling the
data packets for delivery. Security Send and Security Receive commands used for RPMB access are
populated with the RPMB Data Frame(s) defined in Figure 638. The controller shall not return successful
completion of a Security Send or Security Receive command for RPMB access until the requested RPMB
Request/Response Message Type indicated is completed. The Security Protocol used for RPMB is defined
in section 5.1.23.3.


547


NVM Express [®] Base Specification, Revision 2.2


**Authentication Method**


A controller supports one Authentication Method as indicated in the Identify Controller data structure.


If the Authentication Method supported is HMAC SHA-256 (refer to RFC 6234), then the message
authentication code (MAC) is calculated using HMAC SHA-256 as defined in RFC 6234. The key used to
generate a MAC using HMAC SHA-256 is the 256-bit Authentication Key stored in the controller for the
selected RPMB target. The HMAC SHA-256 calculation takes as input a key and a message. Input to the
MAC calculation is the concatenation of the fields in the RPMB Data Frame (request or response) excluding
stuff bytes and the MAC itself – i.e., bytes [223:255] and Data of the frame in that order.


**RPMB Operations**


The host sends a Request Message Type to the controller to request an operation by the controller or to
deliver data to be written into the RPMB memory block. To deliver a Request Message Type, the host uses
the Security Send command. If the data to be delivered to the controller is more than reported in Identify
Controller data structure, the host sends multiple Security Send commands to transfer the entire data.


The host sends a Response Message Type to the controller to read the result of a previous operation
request, to read the Write Counter, or to read data from the RPMB memory block. To deliver a Response
Message Type, the host uses the Security Receive command. If the data to be read from the controller is
more than reported in Identify Controller data structure, the host sends multiple Security Receive
commands to transfer the entire data.


**8.1.21.2.1 Authentication Key Programming**


Authentication Key programming is initiated by a Security Send command to program the Authentication
Key to the specified RPMB target, followed by a subsequent Security Send command to request the result,
and lastly, the host issues a Security Receive command to retrieve the result.


**Figure 639: RPMB – Authentication Key Data Flow**







|Command|Bytes in Command|Field Name|Value|Objective|
|---|---|---|---|---|
|Security<br>Send 1|**Data populated by the host and sent to the controller**|**Data populated by the host and sent to the controller**|**Data populated by the host and sent to the controller**|Send<br>Authentication<br>Key<br>to<br>be<br>Programmed<br>to<br>the controller|
|Security<br>Send 1|222-_N_:00|Stuff Bytes|0…00h|0…00h|
|Security<br>Send 1|222:222-(_N_-1)|MAC/Key|_Key_<br>_to_<br>_be_<br>_programmed_|_Key_<br>_to_<br>_be_<br>_programmed_|
|Security<br>Send 1|223|RPMB Target|_RPMB_<br>_target_<br>_to_<br>_access_|_RPMB_<br>_target_<br>_to_<br>_access_|
|Security<br>Send 1|239:224|Nonce|0…00h|0…00h|
|Security<br>Send 1|243:240|Write Counter|00000000h|00000000h|
|Security<br>Send 1|247:244|Address|00000000h|00000000h|
|Security<br>Send 1|251:248|Sector Count|00000000h|00000000h|
|Security<br>Send 1|253:252|Result|0000h|0000h|
|Security<br>Send 1|255:254|Request/Response|0001h_(Request)_|0001h_(Request)_|
|Security<br>Send 2|**Data populated by the host and sent to the controller**|**Data populated by the host and sent to the controller**|**Data populated by the host and sent to the controller**|Request Result of<br>Key<br>Programming|
|Security<br>Send 2|222-_N_:00|Stuff Bytes|0…00h|0…00h|
|Security<br>Send 2|222:222-(_N_-1)|MAC/Key|0…00h|0…00h|
|Security<br>Send 2|223|RPMB Target|_RPMB_<br>_target_<br>_to_<br>_access_|_RPMB_<br>_target_<br>_to_<br>_access_|
|Security<br>Send 2|239:224|Nonce|0…00h|0…00h|
|Security<br>Send 2|243:240|Write Counter|00000000h|00000000h|
|Security<br>Send 2|247:244|Address|00000000h|00000000h|
|Security<br>Send 2|251:248|Sector Count|00000000h|00000000h|
|Security<br>Send 2|253:252|Result|0000h|0000h|
|Security<br>Send 2|255:254|Request/Response|0005h_(Request)_|0005h_(Request)_|
|Security<br>Receive 1|**Data populated by the controller and returned to the host**|**Data populated by the controller and returned to the host**|**Data populated by the controller and returned to the host**|Retrieve the Key<br>Programming<br>Result|
|Security<br>Receive 1|222-_N_:00|Stuff Bytes|0…00h|0…00h|
|Security<br>Receive 1|222:222-(_N_-1)|MAC/Key|0…00h|0…00h|


548




NVM Express [®] Base Specification, Revision 2.2


**Figure 639: RPMB – Authentication Key Data Flow**

|Command|Bytes in Command|Field Name|Value|Objective|
|---|---|---|---|---|
||223|RPMB Target|_RPMB_<br>_target_<br>_response was sent_<br>_from_||
||239:224|Nonce|0…00h|0…00h|
||243:240|Write Counter|00000000h|00000000h|
||247:244|Address|00000000h|00000000h|
||251:248|Sector Count|00000000h|00000000h|
||253:252|Result|_Result Code_|_Result Code_|
||255:254|Request/Response|0100h_(Response)_|0100h_(Response)_|



**8.1.21.2.2 Read Write Counter Value**


The Read Write Counter Value sequence is initiated by a Security Send command to request the Write
Counter value, followed by a Security Receive command to retrieve the Write Counter result.


**Figure 640: RPMB – Read Write Counter Value Flow**








|Command|Bytes in Command|Field Name|Value|Objective|
|---|---|---|---|---|
|Security<br>Send 1|Data populated by the host and sent to the controller|Data populated by the host and sent to the controller|Data populated by the host and sent to the controller|Request<br>Write<br>Counter Read|
|Security<br>Send 1|222-_N_:00|Stuff Bytes|0…00h|0…00h|
|Security<br>Send 1|222:222-(_N_-1)|MAC/Key|0…00h|0…00h|
|Security<br>Send 1|223|RPMB Target|_RPMB target to access_|_RPMB target to access_|
|Security<br>Send 1|239:224|Nonce|_Nonce generated by the_<br>_host_|_Nonce generated by the_<br>_host_|
|Security<br>Send 1|243:240|Write Counter|00000000h|00000000h|
|Security<br>Send 1|247:244|Address|00000000h|00000000h|
|Security<br>Send 1|251:248|Sector Count|00000000h|00000000h|
|Security<br>Send 1|253:252|Result|0000h|0000h|
|Security<br>Send 1|255:254|Request/Response|0002h_(Request)_|0002h_(Request)_|
|Security<br>Receive 1|Data populated by the controller and returned to the host|Data populated by the controller and returned to the host|Data populated by the controller and returned to the host|Retrieve<br>Write<br>Counter<br>Read<br>Result|
|Security<br>Receive 1|222-_N_:00|Stuff Bytes|0…00h|0…00h|
|Security<br>Receive 1|222:222-(_N_-1)|MAC/Key|_MAC generated by the_<br>_controller_|_MAC generated by the_<br>_controller_|
|Security<br>Receive 1|223|RPMB Target|_RPMB target response_<br>_was sent from_|_RPMB target response_<br>_was sent from_|
|Security<br>Receive 1|239:224|Nonce|_Copy_<br>_of_<br>_the_<br>_Nonce_<br>_generated by the host_|_Copy_<br>_of_<br>_the_<br>_Nonce_<br>_generated by the host_|
|Security<br>Receive 1|243:240|Write Counter|_Current_<br>_Write_<br>_Counter_<br>_value_|_Current_<br>_Write_<br>_Counter_<br>_value_|
|Security<br>Receive 1|247:244|Address|00000000h|00000000h|
|Security<br>Receive 1|251:248|Sector Count|00000000h|00000000h|
|Security<br>Receive 1|253:252|Result|_Result Code_|_Result Code_|
|Security<br>Receive 1|255:254|Request/Response|0200h_(Response)_|0200h_(Response)_|



**8.1.21.2.3 Authenticated Data Write**


The Authenticated Data Write is initiated by a Security Send command. The RPMB Data Frame delivered
from the host to the controller includes the Request Message Type = 0003h, Block Count, Address, Write
Counter, Data and MAC.


When the controller receives this RPMB Data Frame, that controller first checks whether the Write Counter
has expired. If the Write Counter has expired, then that controller sets the RPMB Operation Result to 0085h
(write failure, write counter expired) and no data is written to the RPMB data area.


549


NVM Express [®] Base Specification, Revision 2.2


After checking the Write Counter is not expired, the Address is checked. If there is an error in the Address
(e.g., out of range), then the result is set to 0004h (address failure) and no data is written to the RPMB data
area.


After checking the Address is valid, the controller calculates the MAC (refer to section 8.1.21.1) and
compares this with the MAC in the request. If the MAC in the request and the calculated MAC are different,
then the controller sets the result to 0002h (authentication failure) and no data is written to the RPMB data
area.


If the MAC in the request and the calculated MAC are equal, then the controller compares the Write Counter
in the request with the Write Counter stored in the controller. If the counters are different, then the controller
sets the result to 0003h (counter failure) and no data is written to the RPMB data area.


If the MAC and Write Counter comparisons are successful, then the write request is authenticated. The
Data from the request is written to the Address indicated in the request and the Write Counter is
incremented by one.


If the write fails, then the returned result is 0005h (write failure). If another error occurs during the write
procedure, then the returned result is 0001h (general failure).


The controller returns a successful completion for the Security Send command when the Authenticated
Data Write operation is completed regardless of whether the Authenticated Data Write was successful or
not.


The success of programming the data should be checked by the host by reading the result property of the
RPMB:


1) The host initiates the Authenticated Data Write verification process by issuing a Security Send

command with delivery of a RPMB data frame containing the Request Message Type = 0005h;
2) The controller returns a successful completion of the Security Send command when the verification

result is ready for retrieval;
3) The host should then retrieve the verification result by issuing a Security Receive command; and
4) The controller returns a successful completion of the Security Receive command and returns the

RPMB data frame containing the Response Message Type = 0300h, the incremented counter
value, the data address, the MAC and result of the data programming operation.


550


NVM Express [®] Base Specification, Revision 2.2


**Figure 641: RPMB – Authenticated Data Write Flow**








|Command|Bytes in Command|Field Name|Value|Objective|
|---|---|---|---|---|
|Security<br>Send 1|** Data populated by the host and sent to the controller**|** Data populated by the host and sent to the controller**|** Data populated by the host and sent to the controller**|Program<br>data<br>request|
|Security<br>Send 1|222-N:00|Stuff Bytes|0…00h|0…00h|
|Security<br>Send 1|222:222-(N-1)|MAC/Key|MAC generated by the host|MAC generated by the host|
|Security<br>Send 1|223|RPMB Target|RPMB target to access|RPMB target to access|
|Security<br>Send 1|239:224|Nonce|0…00h|0…00h|
|Security<br>Send 1|243:240|Write Counter|Current Write Counter value|Current Write Counter value|
|Security<br>Send 1|247:244|Address|Address in the RPMB|Address in the RPMB|
|Security<br>Send 1|251:248|Sector Count|Number of 512B blocks|Number of 512B blocks|
|Security<br>Send 1|253:252|Result|0000h|0000h|
|Security<br>Send 1|255:254|Request/Response|0003h (Request)|0003h (Request)|
|Security<br>Send 1|(M-1)+256:256|Data|Data to be written|Data to be written|
|Security<br>Send 2|**Data populated by the host and sent to the controller**|**Data populated by the host and sent to the controller**|**Data populated by the host and sent to the controller**|Request Result of<br>data<br>programming|
|Security<br>Send 2|222-_N_:00|Stuff Bytes|0…00h|0…00h|
|Security<br>Send 2|222:222-(_N_-1)|MAC/Key|0…00h|0…00h|
|Security<br>Send 2|223|RPMB Target|_RPMB target to access_|_RPMB target to access_|
|Security<br>Send 2|239:224|Nonce|0…00h|0…00h|
|Security<br>Send 2|243:240|Write Counter|00000000h|00000000h|
|Security<br>Send 2|247:244|Address|00000000h|00000000h|
|Security<br>Send 2|251:248|Sector Count|00000000h|00000000h|
|Security<br>Send 2|253:252|Result|0000h|0000h|
|Security<br>Send 2|255:254|Request/Response|0005h_(Request)_|0005h_(Request)_|
|Security<br>Receive 1|**Data populated by the controller and returned to the host**|**Data populated by the controller and returned to the host**|**Data populated by the controller and returned to the host**|Retrieve<br>Result<br>from<br>data<br>programming|
|Security<br>Receive 1|222-_N_:00|Stuff Bytes|0…00h|0…00h|
|Security<br>Receive 1|222:222-(_N_-1)|MAC/Key|_MAC_<br>_generated_<br>_by_<br>_the_<br>_controller_|_MAC_<br>_generated_<br>_by_<br>_the_<br>_controller_|
|Security<br>Receive 1|223|RPMB Target|_RPMB target response was_<br>_sent from_|_RPMB target response was_<br>_sent from_|
|Security<br>Receive 1|239:224|Nonce|0…00h|0…00h|
|Security<br>Receive 1|243:240|Write Counter|_Incremented Write Counter_<br>_value_|_Incremented Write Counter_<br>_value_|
|Security<br>Receive 1|247:244|Address|_Address in RPMB_|_Address in RPMB_|
|Security<br>Receive 1|251:248|Sector Count|00000000h|00000000h|
|Security<br>Receive 1|253:252|Result|_Result Code_|_Result Code_|
|Security<br>Receive 1|255:254|Request/Response|0300h_(Response)_|0300h_(Response)_|



**8.1.21.2.4 Authenticated Data Read**


The Authenticated Data Read sequence is initiated by a Security Send command. The RPMB data frame
delivered from the host to the controller includes the Request Message Type = 0004h, Nonce, Address,
and the Sector Count.


When the controller receives this RPMB Data Frame, that controller first checks the Address. If there is an
error in the Address, then the result is set to 0004h (address failure) and the data read is not valid.


When the host receives a successful completion of the Security Send command from the controller, that
host should send a Security Receive command to the controller to retrieve the data. The controller returns
an RPMB Data Frame with Response Message Type (0400h), the Sector Count, a copy of the Nonce
received in the request, the Address, the Data, the controller calculated MAC, and the Result. Note: It is
the responsibility of the host to verify the MAC returned on an Authenticated Data Read Request.


If the data transfer from the addressed location in the controller fails, the returned Result is 0006h (read
failure). If the Address provided in the Security Send command is not valid, then the returned Result is
0004h (address failure). If another error occurs during the read procedure, then the returned Result is 0001h
(general failure).


551


NVM Express [®] Base Specification, Revision 2.2


**Figure 642: RPMB – Authenticated Data Read Flow**








|Command|Bytes in Command|Field Name|Value|Objective|
|---|---|---|---|---|
|Security<br>Send 1|**Data populated by the host and sent to the controller**|**Data populated by the host and sent to the controller**|**Data populated by the host and sent to the controller**|Read<br>Data<br>request|
|Security<br>Send 1|222-_N_:00|Stuff Bytes|0…00h|0…00h|
|Security<br>Send 1|222:222-(_N_-1)|MAC/Key|0…00h|0…00h|
|Security<br>Send 1|223|RPMB Target|_RPMB target to access_|_RPMB target to access_|
|Security<br>Send 1|239:224|Nonce|_Nonce generated by the host_|_Nonce generated by the host_|
|Security<br>Send 1|243:240|Write Counter|00000000h|00000000h|
|Security<br>Send 1|247:244|Address|_Address in RPMB_|_Address in RPMB_|
|Security<br>Send 1|251:248|Sector Count|_Number of 512B blocks_|_Number of 512B blocks_|
|Security<br>Send 1|253:252|Result|0000h|0000h|
|Security<br>Send 1|255:254|Request/Response|0004h_(Request)_|0004h_(Request)_|
|Security<br>Receive 1|**Data populated by the controller and returned to the host**|**Data populated by the controller and returned to the host**|**Data populated by the controller and returned to the host**|Retrieve<br>result<br>and data from<br>read request|
|Security<br>Receive 1|222-_N_:00|Stuff Bytes|0…00h|0…00h|
|Security<br>Receive 1|222:222-(_N_-1)|MAC/Key|_MAC_<br>_generated_<br>_by_<br>_the_<br>_controller_|_MAC_<br>_generated_<br>_by_<br>_the_<br>_controller_|
|Security<br>Receive 1|223|RPMB Target|_RPMB target response was_<br>_sent from_|_RPMB target response was_<br>_sent from_|
|Security<br>Receive 1|239:224|Nonce|_Copy of the Nonce generated_<br>_by the host_|_Copy of the Nonce generated_<br>_by the host_|
|Security<br>Receive 1|243:240|Write Counter|0000h|0000h|
|Security<br>Receive 1|247:244|Address|_Address in RPMB_|_Address in RPMB_|
|Security<br>Receive 1|251:248|Sector Count|_Number of 512B blocks_|_Number of 512B blocks_|
|Security<br>Receive 1|253:252|Result|_Result Code_|_Result Code_|
|Security<br>Receive 1|255:254|Request/Response|0400h_(Response)_|0400h_(Response)_|
|Security<br>Receive 1|(_M_-1)+256:256|Data|_Data read from RPMB target_|_Data read from RPMB target_|



**Authenticated Device Configuration Block Write**


The Authenticated Device Configuration Block Write is initiated by a Security Send command. The RPMB
Data Frame delivered from the host to the controller includes the Request Message Type = 0006h, Sector
Count = 01h, MAC, Write Counter set to the current Write Counter value, and the RPMB Device
Configuration Block data structure (refer to Figure 643). All other fields are cleared to 0h.


If the Write Counter has expired, then that controller sets the result to 0005h (write failure, write counter
expired) and no data is written to the Device Configuration Block.


The controller calculates the MAC of Request Type, Block Count, Write Counter, Address and Data, and
compares this with the MAC in the request. If the MAC in the request and the calculated MAC are different,
then the controller sets the result to 0002h (authentication failure) and no data is written to the RPMB Device
Configuration Block.


If the Data from the RPMB Device Configuration Block attempts to disable Boot Partition Protection, then
the controller sets the result to 0008h (Invalid RPMB Device Configuration Block) and no data is written to
the RPMB Device Configuration Block.


If the MAC in the request and the calculated MAC are equal, then the write request is authenticated. The
Data from the request is written to the RPMB Device Configuration Block.


If any other error occurs during the write procedure, then the returned result is 0001h (general failure).


The controller returns a successful completion for the Security Send command when the Authenticated
Data Write operation is completed regardless of whether the Authenticated Device Configuration Block
Write was successful or not.


When the host receives a successful completion of the Security Send command from the controller, that
host should send a Security Receive command to the controller to retrieve the data. The controller returns
an RPMB Data Frame with Response Message Type (0600h), the incremented counter value, the MAC,
and the Result. All other fields are cleared to 0h.


552


NVM Express [®] Base Specification, Revision 2.2


The Write Counter for the Device Configuration Block is independent of the Write Counter for RPMB target
0. Authenticated Device Configuration Block Writes do not affect the Write Counter for RPMB target 0 since
the data is not part of the RPMB data area. The current value of the Write Counter for the Device
Configuration Block may be read using an Authenticated Device Configuration Block Read (refer to section
8.1.21.4).


**Figure 643: RPMB – Authenticated Device Configuration Block Write Flow**














|Command|Bytes in Command|Field Name|Value|Objective|
|---|---|---|---|---|
|Security<br>Send 1|** Data populated by the host and sent to the controller**|** Data populated by the host and sent to the controller**|** Data populated by the host and sent to the controller**|Request Device<br>Configuration<br>Block Write|
|Security<br>Send 1|222-_N_:00|Stuff Bytes|0…00h|0…00h|
|Security<br>Send 1|222:222-(_N_-1)|MAC/Key|_MAC generated by the_<br>_host_|_MAC generated by the_<br>_host_|
|Security<br>Send 1|223|RPMB Target|00h|00h|
|Security<br>Send 1|239:224|Nonce|0…00h|0…00h|
|Security<br>Send 1|243:240|Write Counter|_Current_<br>_Write_<br>_Counter_<br>_value_|_Current_<br>_Write_<br>_Counter_<br>_value_|
|Security<br>Send 1|247:244|Address|00000000h|00000000h|
|Security<br>Send 1|251:248|Sector Count|00000001h|00000001h|
|Security<br>Send 1|253:252|Result|0000h|0000h|
|Security<br>Send 1|255:254|Request/Response|0006h_(Request)_|0006h_(Request)_|
|Security<br>Send 1|767:256|Data|_RPMB_<br>_Device_<br>_Configuration Block data_<br>_structure_|_RPMB_<br>_Device_<br>_Configuration Block data_<br>_structure_|
|Security<br>Send 2|Data populated by the host and sent to the controller|Data populated by the host and sent to the controller|Data populated by the host and sent to the controller|Request Result of<br>data<br>programming|
|Security<br>Send 2|222-N:00|Stuff Bytes|0…00h|0…00h|
|Security<br>Send 2|222:222-(N-1)|MAC/Key|0…00h|0…00h|
|Security<br>Send 2|223|RPMB Target|_RPMB target to access_|_RPMB target to access_|
|Security<br>Send 2|239:224|Nonce|0…00h|0…00h|
|Security<br>Send 2|243:240|Write Counter|00000000h|00000000h|
|Security<br>Send 2|247:244|Address|00000000h|00000000h|
|Security<br>Send 2|251:248|Sector Count|00000000h|00000000h|
|Security<br>Send 2|253:252|Result|0000h|0000h|
|Security<br>Send 2|255:254|Request/Response|0005h_ (Request)_|0005h_ (Request)_|
|Security<br>Receive 1|**Data populated by the controller and returned to the host**|**Data populated by the controller and returned to the host**|**Data populated by the controller and returned to the host**|Retrieve Device<br>Configuration<br>Block<br>Write<br>Result|
|Security<br>Receive 1|222-_N_:00|Stuff Bytes|0…00h|0…00h|
|Security<br>Receive 1|222:222-(_N_-1)|MAC/Key|_MAC generated by the_<br>_controller_|_MAC generated by the_<br>_controller_|
|Security<br>Receive 1|223|RPMB Target|00h|00h|
|Security<br>Receive 1|239:224|Nonce|0…00h|0…00h|
|Security<br>Receive 1|243:240|Write Counter|_Incremented_<br>_Write_<br>_Counter value_|_Incremented_<br>_Write_<br>_Counter value_|
|Security<br>Receive 1|247:244|Address|00000000h|00000000h|
|Security<br>Receive 1|251:248|Sector Count|00000000h|00000000h|
|Security<br>Receive 1|253:252|Result|_Result Code_|_Result Code_|
|Security<br>Receive 1|255:254|Request/Response|0600h_(Response)_|0600h_(Response)_|



**Authenticated Device Configuration Block Read**


The Authenticated Device Configuration Block Read sequence is initiated by a Security Send command.
The RPMB data frame delivered from the host to the controller includes the Nonce, Request Message Type
= 0007h and the Sector Count = 01h. All other fields are cleared to 0h.


When the host receives a successful completion of the Security Send command from the controller, that
host should send a Security Receive command to the controller to retrieve the data. The controller returns
an RPMB Data Frame with Response Message Type (0700h), the Sector Count = 01h, a copy of the Nonce
received in the request, the RPMB Device Configuration Block Data Structure (refer to Figure 634), the


553


NVM Express [®] Base Specification, Revision 2.2


MAC, the Write Counter set to the current Write Counter value, and the Result. All other fields are cleared
to 0h.


The Write Counter for the Device Configuration Block is independent of the Write Counter for RPMB target
0. The controller returns the Device Configuration Block Write Counter as shown in Figure 644.


The MAC is calculated from Response Type, Nonce, Address, Data and Result fields. If the MAC calculation
fails, then the returned result is 0002h (i.e., authentication failure). If another error occurs during the read
procedure, then the returned Result is 0001h (i.e., general failure).


**Figure 644: RPMB – Authenticated Device Configuration Block Read Flow**









|Command|Bytes in Command|Field Name|Value|Objective|
|---|---|---|---|---|
|Security<br>Send 1|**Data populated by the host and sent to the controller**|**Data populated by the host and sent to the controller**|**Data populated by the host and sent to the controller**|Request Device<br>Configuration<br>Block Read|
|Security<br>Send 1|222-_N_:00|Stuff Bytes|0…00h|0…00h|
|Security<br>Send 1|222:222-(_N_-1)|MAC/Key|0…00h|0…00h|
|Security<br>Send 1|223|RPMB Target|00h|00h|
|Security<br>Send 1|239:224|Nonce|_Nonce generated by the_<br>_host_|_Nonce generated by the_<br>_host_|
|Security<br>Send 1|243:240|Write Counter|00000000h|00000000h|
|Security<br>Send 1|247:244|Address|00000000h|00000000h|
|Security<br>Send 1|251:248|Sector Count|00000001h|00000001h|
|Security<br>Send 1|253:252|Result|0000h|0000h|
|Security<br>Send 1|255:254|Request/Response|0007h_(Request)_|0007h_(Request)_|
|Security<br>Receive 1|**Data populated by the controller and returned to the host**|**Data populated by the controller and returned to the host**|**Data populated by the controller and returned to the host**|Retrieve Device<br>Configuration<br>Block<br>Read<br>Result|
|Security<br>Receive 1|222-_N_:00|Stuff Bytes|0…00h|0…00h|
|Security<br>Receive 1|222:222-(_N_-1)|MAC/Key|_MAC generated by the_<br>_controller_|_MAC generated by the_<br>_controller_|
|Security<br>Receive 1|223|RPMB Target|00h|00h|
|Security<br>Receive 1|239:224|Nonce|_Copy_<br>_of_<br>_the_<br>_Nonce_<br>_generated by the host_|_Copy_<br>_of_<br>_the_<br>_Nonce_<br>_generated by the host_|
|Security<br>Receive 1|243:240|Write Counter|_Current Write Counter value_|_Current Write Counter value_|
|Security<br>Receive 1|247:244|Address|00000000h|00000000h|
|Security<br>Receive 1|251:248|Sector Count|00000001h|00000001h|
|Security<br>Receive 1|253:252|Result|_Result Code_|_Result Code_|
|Security<br>Receive 1|255:254|Request/Response|0700h_(Response)_|0700h_(Response)_|
|Security<br>Receive 1|767:256|Data|_RPMB_<br>_Device_<br>_Configuration Block data_<br>_structure_|_RPMB_<br>_Device_<br>_Configuration Block data_<br>_structure_|


**Reservations**





NVM Express reservations provide capabilities that may be utilized by two or more hosts to coordinate
access to a shared namespace. The protocol and manner in which these capabilities are used is outside
the scope of this specification. Incorrect application of these capabilities may corrupt data and/or otherwise
impair system operation.


Reservation operation after a division event (refer to section 3.2.5.1) is described in section 3.2.5.2.


A reservation on a namespace restricts hosts access to that namespace. If a host submits a command that
uses the Namespace Identifier (NSID) field and that NSID field contains an active NSID, then in the
presence of a reservation on the namespace identified by that NSID where that host lacks sufficient rights,
that command is aborted by the controller with a status code of Reservation Conflict. If a host submits a
command that uses the NSID field and that NSID field is set to FFFFFFFFh, then in the presence of a
reservation on any of the namespaces impacted by that command where that host lacks sufficient rights on
any of the impacted namespaces, that command is aborted by the controller with a status code of
Reservation Conflict. Capabilities are provided that allow recovery from a reservation on a namespace held
by a failing or uncooperative host.


A command is checked for reservation conflict at the time that the controller begins processing that
command. If that reservation conflict check allows the command to be performed (i.e., the host has sufficient


554


NVM Express [®] Base Specification, Revision 2.2


rights for that command with respect to existing reservations, if any), then that command shall not be
subsequently aborted by the controller with a status code of Reservation Conflict (e.g., due to a subsequent
reservation).


**Figure 645: Example Multi-Host System**





















A reservation requires an association between a host and a namespace. As shown in Figure 645, each
controller in a multi-path I/O and namespace sharing environment is associated with exactly one host. While
it is possible to construct systems where two or more hosts share a single controller, such usage is outside
the scope of this specification.


A host may be associated with multiple controllers. In Figure 645 host A is associated with two controllers
while hosts B and C are each associated with a single controller. A host should register a non-zero Host
Identifier (refer to section 5.1.25.1.28) with each controller with which that host is associated using a Set
Features command (refer to section 5.1.25) prior to performing any operations associated with reservations.
The Host Identifier allows the NVM subsystem to identify controllers associated with the same host and
preserve reservation properties across these controllers (i.e., a host issued command has the same
reservation rights no matter which controller associated with the host processes the command).


An NVM subsystem may require that the host register a non-zero Host Identifier for a host to use
reservations (i.e., the RHII bit is set to ‘1’ in the CTRATT field of the Identify Controller data structure (refer
to Figure 313)). If the controller does not support reservations with a Host Identifier value of 0h and a
reservation command is received from a host with a Host Identifier value of 0h, then the controller shall
abort that reservation command with a status of Host Identifier Not Initialized.


If an NVM subsystem supports reservations with a Host Identifier value of 0h, and:


1. registrations or reservations are established by a host with a Host Identifier value of 0h; and
2. the Host Identifier of that host is changed to a non-zero value,


then those registrations or reservations remain associated with the Host with a Host Identifier value of 0h
and are not associated with the host with the non-zero Host Identifier.


If the controller does not support reservations with a Host Identifier value of 0h, reservations may have
been established by hosts with non-zero Host Identifiers connected to other controllers, and commands
from a host with a Host Identifier value of 0h that conflict with a reservation (refer to Figure 646 and Figure
647) are aborted by the controller with a status code of Reservation Conflict.


555


NVM Express [®] Base Specification, Revision 2.2


Support for reservations by a namespace or controller is optional. A namespace indicates support for
reservations by reporting a non-zero value in the Reservation Capabilities (RESCAP) field in the Identify
Namespace data structure. A controller indicates support for reservations through the Optional NVM
Command Support (ONCS) field in the Identify Controller data structure (refer to Figure 313). If a host
submits a command associated with reservations (i.e., Reservation Report, Reservation Register,
Reservation Acquire, and Reservation Release):

  - to a controller that does not support reservations; or

  - that impacts a namespace that does not support reservations,


then the command is aborted by the controller with a status code of Invalid Command Opcode.


Controllers that make up an NVM subsystem shall all have the same support for reservations. Although
strongly encouraged, namespaces that make up an NVM subsystem are not all required to have the same
support for reservations. For example, some namespaces within a single controller may support
reservations while others do not, or the supported reservation types may differ among namespaces. If a
controller supports reservations, then the controller shall:

   - Indicate support for reservations by returning a '1' in the Reservations Support (RESERVS) bit of
the Optional NVM Command Support (ONCS) field in the Identify Controller data structure;

   - Support the Reservation Report command (refer to section 7.8), Reservation Register command
(refer to section 7.6), Reservation Acquire command (refer to section 7.5), and Reservation
Release command (refer to section 7.7);

   - Support the Reservation Notification log page;

   - Support the Reservation Log Page Available asynchronous events;

   - Support the Reservation Notification Mask Feature;

   - Support the Host Identifier Feature; and

   - Support the Reservation Persistence Feature.


If a controller supports dispersed namespaces and supports reservations, then the controller supports the
Dispersed Namespace Reservation Support (DISNSRS) bit being set to ‘1’ in the Reservation Report
command, Reservation Register command, Reservation Acquire command, and Reservation Release
command, as described in section 8.1.9.6.


If a namespace supports reservations, then the namespace shall:

  - Report a non-zero value in the Reservation Capabilities (RESCAP) field in the Identify Namespace
data structure;

  - Support Persist Through Power Loss (PTPL) state; and

  - Support sufficient resources to allow a host to successfully register a reservation key on every
controller in the NVM subsystem with access to the shared namespace (i.e., a Reservation Register
command shall never fail due to lack of resources).


NOTE: The behavior of Ignore Existing Key has been changed to improve compatibility with SCSI based
implementations. Conformance to the modified behavior is indicated in the Reservation Capabilities
(RESCAP) field of the Identify Namespace data structure. For the previous definition of Ignore Existing Key
behavior, refer to NVM Express Base Specification, Revision 1.2.1.


**Reservation Types**


The NVM Express interface supports six types of reservations:

  - Write Exclusive;

  - Exclusive Access;

  - Write Exclusive - Registrants Only;

  - Exclusive Access - Registrants Only;

  - Write Exclusive - All Registrants; and

  - Exclusive Access - All Registrants.


556


NVM Express [®] Base Specification, Revision 2.2


**Figure 646: Command Behavior in the Presence of a Reservation**









|Reservation Type|Reservation<br>Holder|Col3|Registrant|Col5|Non-<br>Registrant|Col7|Reservation Holder Definition|
|---|---|---|---|---|---|---|---|
|**Reservation Type**|**Read**|**Write**|**Read**|**Write**|**Read**|**Write**|**Write**|
|Write Exclusive|Y|Y|Y|N|Y|N|One Reservation Holder|
|Exclusive Access|Y|Y|N|N|N|N|One Reservation Holder|
|Write Exclusive -<br>Registrants Only|Y|Y|Y|Y|Y|N|One Reservation Holder|
|Exclusive Access -<br>Registrants Only|Y|Y|Y|Y|N|N|One Reservation Holder|
|Write Exclusive - All<br>Registrants|Y|Y|Y|Y|Y|N|All Registrants are Reservation<br>Holders|
|Exclusive Access - All<br>Registrants|Y|Y|Y|Y|N|N|All Registrants are Reservation<br>Holders|


The differences between these reservation types are: the type of access that is excluded (i.e., writes or all
accesses), whether registrants have the same access rights as the reservation holder, and whether
registrants are also considered to be reservation holders. These differences are summarized in Figure 646
and the specific behavior for each NVM Express command is shown in Figure 647.


Reservations and registrations persist across all Controller Level Resets and all NVM Subsystem Resets
except reset due to power loss. A reservation may be optionally configured to be retained across a reset
due to power loss using the Persist Through Power Loss State (PTPLS). A Persist Through Power Loss
State (PTPLS) is associated with each namespace that supports reservations and may be modified as a
side effect of a Reservation Register command (refer to section 7.6) or a Set Features command (refer to
section 5.1.25).


**Figure 647: Command Behavior in the Presence of a Reservation**













|NVMe Command|Write<br>Exclusive<br>Reservation|Col3|Exclusive<br>Access<br>Reservation|Col5|Write Exclusive<br>Registrants Only<br>or<br>Write Exclusive<br>All Registrants<br>Reservation|Col7|Exclusive Access<br>Registrants Only<br>or<br>Exclusive Access<br>All Registrants<br>Reservation|Col9|
|---|---|---|---|---|---|---|---|---|
|**NVMe Command**|**Non-Registrant**|**Registrant**|**Non-Registrant**|**Registrant**|**Non-Registrant**|**Registrant**|**Non-Registrant**|**Registrant**|
|<br> <br> <br> <br>**Read Command Group**|<br> <br> <br> <br>**Read Command Group**|<br> <br> <br> <br>**Read Command Group**|<br> <br> <br> <br>**Read Command Group**|<br> <br> <br> <br>**Read Command Group**|<br> <br> <br> <br>**Read Command Group**|<br> <br> <br> <br>**Read Command Group**|<br> <br> <br> <br>**Read Command Group**|<br> <br> <br> <br>**Read Command Group**|
|Security Receive (Admin)4 <br>I/O Command Set specific Copy Commands<br>(source)2,3 <br>I/O Command Set specific Read Commands2|A|A|C|C|A|A|C|A|


557


NVM Express [®] Base Specification, Revision 2.2


**Figure 647: Command Behavior in the Presence of a Reservation**





















|NVMe Command|Write<br>Exclusive<br>Reservation|Col3|Exclusive<br>Access<br>Reservation|Col5|Write Exclusive<br>Registrants Only<br>or<br>Write Exclusive<br>All Registrants<br>Reservation|Col7|Exclusive Access<br>Registrants Only<br>or<br>Exclusive Access<br>All Registrants<br>Reservation|Col9|
|---|---|---|---|---|---|---|---|---|
|**NVMe Command**|**Non-Registrant**|**Registrant**|**Non-Registrant**|**Registrant**|**Non-Registrant**|**Registrant**|**Non-Registrant**|**Registrant**|
|<br> <br> <br> <br>**Write Command Group**|<br> <br> <br> <br>**Write Command Group**|<br> <br> <br> <br>**Write Command Group**|<br> <br> <br> <br>**Write Command Group**|<br> <br> <br> <br>**Write Command Group**|<br> <br> <br> <br>**Write Command Group**|<br> <br> <br> <br>**Write Command Group**|<br> <br> <br> <br>**Write Command Group**|<br> <br> <br> <br>**Write Command Group**|
|Capacity Management (Admin)<br>Flush<br>Format NVM (Admin)<br>Namespace Attachment (Admin)<br>Namespace Management (Admin)<br>Sanitize (Admin)<br>Security Send (Admin)4 <br>I/O Command Set specific Copy Commands<br>(destination)2,3 <br>I/O Command Set specific Write Commands2|C|C|C|C|C|A|C|A|
|**Reservation Command Groups**|**Reservation Command Groups**|**Reservation Command Groups**|**Reservation Command Groups**|**Reservation Command Groups**|**Reservation Command Groups**|**Reservation Command Groups**|**Reservation Command Groups**|**Reservation Command Groups**|
|Reservation Acquire - Acquire|C|C|C|C|C|C|C|C|
|Reservation Acquire - Preempt<br>Reservation Acquire - Preempt and Abort<br>Reservation Release|C|A|C|A|C|A|C|A|
|**All Other Commands Group**|**All Other Commands Group**|**All Other Commands Group**|**All Other Commands Group**|**All Other Commands Group**|**All Other Commands Group**|**All Other Commands Group**|**All Other Commands Group**|**All Other Commands Group**|
|All other commands1|A|A|A|A|A|A|A|A|
|Key:<br>A definition: A=Allowed, command processed normally by the controller<br>C definition: C=Conflict, command aborted by the controller with a status code of Reservation Conflict<br>Notes:<br>1.<br>The behavior of a vendor specific command is vendor specific.<br>2.<br>Refer to the applicable I/O Command Set specification<br>3.<br>For an I/O Command Set specific Copy command, each source namespace is checked for reservation conflict as if accessed<br>by a read command and the destination namespace is checked for reservation conflict as if accessed by a write command,<br>as described in the applicable I/O command Set specification.<br>4.<br>Applies only to commands that use the Namespace Identifier (NSID) field (refer to the applicable row in Figure 142). Any<br>command that does not use the NSID field is part of the All Other Commands Group.|Key:<br>A definition: A=Allowed, command processed normally by the controller<br>C definition: C=Conflict, command aborted by the controller with a status code of Reservation Conflict<br>Notes:<br>1.<br>The behavior of a vendor specific command is vendor specific.<br>2.<br>Refer to the applicable I/O Command Set specification<br>3.<br>For an I/O Command Set specific Copy command, each source namespace is checked for reservation conflict as if accessed<br>by a read command and the destination namespace is checked for reservation conflict as if accessed by a write command,<br>as described in the applicable I/O command Set specification.<br>4.<br>Applies only to commands that use the Namespace Identifier (NSID) field (refer to the applicable row in Figure 142). Any<br>command that does not use the NSID field is part of the All Other Commands Group.|Key:<br>A definition: A=Allowed, command processed normally by the controller<br>C definition: C=Conflict, command aborted by the controller with a status code of Reservation Conflict<br>Notes:<br>1.<br>The behavior of a vendor specific command is vendor specific.<br>2.<br>Refer to the applicable I/O Command Set specification<br>3.<br>For an I/O Command Set specific Copy command, each source namespace is checked for reservation conflict as if accessed<br>by a read command and the destination namespace is checked for reservation conflict as if accessed by a write command,<br>as described in the applicable I/O command Set specification.<br>4.<br>Applies only to commands that use the Namespace Identifier (NSID) field (refer to the applicable row in Figure 142). Any<br>command that does not use the NSID field is part of the All Other Commands Group.|Key:<br>A definition: A=Allowed, command processed normally by the controller<br>C definition: C=Conflict, command aborted by the controller with a status code of Reservation Conflict<br>Notes:<br>1.<br>The behavior of a vendor specific command is vendor specific.<br>2.<br>Refer to the applicable I/O Command Set specification<br>3.<br>For an I/O Command Set specific Copy command, each source namespace is checked for reservation conflict as if accessed<br>by a read command and the destination namespace is checked for reservation conflict as if accessed by a write command,<br>as described in the applicable I/O command Set specification.<br>4.<br>Applies only to commands that use the Namespace Identifier (NSID) field (refer to the applicable row in Figure 142). Any<br>command that does not use the NSID field is part of the All Other Commands Group.|Key:<br>A definition: A=Allowed, command processed normally by the controller<br>C definition: C=Conflict, command aborted by the controller with a status code of Reservation Conflict<br>Notes:<br>1.<br>The behavior of a vendor specific command is vendor specific.<br>2.<br>Refer to the applicable I/O Command Set specification<br>3.<br>For an I/O Command Set specific Copy command, each source namespace is checked for reservation conflict as if accessed<br>by a read command and the destination namespace is checked for reservation conflict as if accessed by a write command,<br>as described in the applicable I/O command Set specification.<br>4.<br>Applies only to commands that use the Namespace Identifier (NSID) field (refer to the applicable row in Figure 142). Any<br>command that does not use the NSID field is part of the All Other Commands Group.|Key:<br>A definition: A=Allowed, command processed normally by the controller<br>C definition: C=Conflict, command aborted by the controller with a status code of Reservation Conflict<br>Notes:<br>1.<br>The behavior of a vendor specific command is vendor specific.<br>2.<br>Refer to the applicable I/O Command Set specification<br>3.<br>For an I/O Command Set specific Copy command, each source namespace is checked for reservation conflict as if accessed<br>by a read command and the destination namespace is checked for reservation conflict as if accessed by a write command,<br>as described in the applicable I/O command Set specification.<br>4.<br>Applies only to commands that use the Namespace Identifier (NSID) field (refer to the applicable row in Figure 142). Any<br>command that does not use the NSID field is part of the All Other Commands Group.|Key:<br>A definition: A=Allowed, command processed normally by the controller<br>C definition: C=Conflict, command aborted by the controller with a status code of Reservation Conflict<br>Notes:<br>1.<br>The behavior of a vendor specific command is vendor specific.<br>2.<br>Refer to the applicable I/O Command Set specification<br>3.<br>For an I/O Command Set specific Copy command, each source namespace is checked for reservation conflict as if accessed<br>by a read command and the destination namespace is checked for reservation conflict as if accessed by a write command,<br>as described in the applicable I/O command Set specification.<br>4.<br>Applies only to commands that use the Namespace Identifier (NSID) field (refer to the applicable row in Figure 142). Any<br>command that does not use the NSID field is part of the All Other Commands Group.|Key:<br>A definition: A=Allowed, command processed normally by the controller<br>C definition: C=Conflict, command aborted by the controller with a status code of Reservation Conflict<br>Notes:<br>1.<br>The behavior of a vendor specific command is vendor specific.<br>2.<br>Refer to the applicable I/O Command Set specification<br>3.<br>For an I/O Command Set specific Copy command, each source namespace is checked for reservation conflict as if accessed<br>by a read command and the destination namespace is checked for reservation conflict as if accessed by a write command,<br>as described in the applicable I/O command Set specification.<br>4.<br>Applies only to commands that use the Namespace Identifier (NSID) field (refer to the applicable row in Figure 142). Any<br>command that does not use the NSID field is part of the All Other Commands Group.|Key:<br>A definition: A=Allowed, command processed normally by the controller<br>C definition: C=Conflict, command aborted by the controller with a status code of Reservation Conflict<br>Notes:<br>1.<br>The behavior of a vendor specific command is vendor specific.<br>2.<br>Refer to the applicable I/O Command Set specification<br>3.<br>For an I/O Command Set specific Copy command, each source namespace is checked for reservation conflict as if accessed<br>by a read command and the destination namespace is checked for reservation conflict as if accessed by a write command,<br>as described in the applicable I/O command Set specification.<br>4.<br>Applies only to commands that use the Namespace Identifier (NSID) field (refer to the applicable row in Figure 142). Any<br>command that does not use the NSID field is part of the All Other Commands Group.|


**Reservation Notifications**


There are three types of reservation notifications: registration preempted, reservation released, and
reservation preempted. Conditions that cause a reservation notification to occur are described in the
following sections. A Reservation Notification log page is created whenever an unmasked reservation
notification occurs on a namespace associated with the controller (refer to section 5.1.12.1.32). Reservation
notifications may be masked from generating a Reservation Notification log page on a per reservation
notification type and per namespace ID basis through the Reservation Notification Mask feature (refer to
section 5.1.25.1.29). A host may use the Asynchronous Event Request command (refer to section 5.1.2)
to be notified of the presence of one or more available Reservation Notification log pages (refer to section
5.1.12.1.32).


558


NVM Express [®] Base Specification, Revision 2.2


**Registering**


Prior to establishing a reservation on a namespace, a host shall become a registrant of that namespace by
registering a reservation key. This reservation key may be used by the host as a means of identifying the
registrant (host), authenticating the registrant, and preempting a failed or uncooperative registrant. The
value of the reservation key used by a host and the method used to select its value is outside the scope of
this specification.


Registering a reservation key with a namespace creates an association between a host and a namespace.
A host that is a registrant of a namespace may use any controller with which that host is associated (i.e.,
that has the same Host Identifier, refer to section 5.1.25.1.28) to access that namespace as a registrant.
Thus, a host is only required to register on a single controller to become a registrant of the namespace on
all controllers in the NVM subsystem that have access to the namespace and are associated with the host.
If a host attempts to access a dispersed namespace that is able to be accessed by controllers in multiple
participating NVM subsystems, then that host is only required to register on a single controller in a single
participating NVM subsystem to become a registrant of the dispersed namespace on all controllers in all
participating NVM subsystems that have access to the dispersed namespace and are associated with the
host.


A host registers a reservation key by executing a Reservation Register command (refer to section 7.6) on
the namespace with the Reservation Register Action (RREGA) field cleared to 000b (i.e., Register
Reservation Key) and supplying a reservation key in the New Reservation Key (NRKEY) field.


A host that is a registrant of a namespace may register the same reservation key value multiple times with
the namespace on the same or different controllers. For a Reservation Register command with the RREGA
field cleared to 000b:


a) the IEKEY field shall be ignored; and
b) if a host that is already a registrant of a namespace attempts to register with that namespace using

a different reservation key value, then the command shall be aborted with a status code of
Reservation Conflict.


There are no restrictions on the reservation key value used by hosts with different Host Identifiers. For
example, multiple hosts may all register with the same reservation key value.


A host that is a registrant of a namespace may replace the existing reservation key value for that
namespace by executing a Reservation Register command on the namespace with the:


a) RREGA field set to 010b (i.e., Replace Reservation Key);
b) current reservation key in the Current Reservation Key (CRKEY) field; and
c) new reservation key in the NRKEY field.


The current reservation key value shall be replaced by the new reservation key value in all controllers to
which the namespace is attached that have the same Host Identifier as the Host Identifier of the controller
processing the command. For dispersed namespaces, this requirement includes all participating NVM
subsystems. If the contents of the CRKEY field do not match the key currently associated with the host,
then the command shall be aborted with a status code of Reservation Conflict. A host may replace its
reservation key without regard to its registration status or current reservation key value by setting the Ignore
Existing Key (IEKEY) bit to '1' in the Reservation Register command. Replacing a reservation key has no
effect on any reservation that may be held on the namespace.


**Unregistering**


A host that is a registrant of a namespace may unregister with the namespace by executing a Reservation
Register command (refer to section 7.6) on the namespace with the RREGA field set to 001b (i.e.,
Unregister Reservation Key) and supplying its current reservation key in the CRKEY field. If the contents
of the CRKEY field do not match the key currently associated with the host, then the command is aborted
with a status code of Reservation Conflict. If the host is not a registrant, then the command is aborted with
a status code of Reservation Conflict.


559


NVM Express [®] Base Specification, Revision 2.2


Successful completion of an unregister operation causes the host to no longer be a registrant of that
namespace. A host may unregister without regard to its current reservation key value by setting the IEKEY
bit to '1' in the Reservation Register command.


Unregistering by a host may cause a reservation held by the host to be released. If a host is the last
remaining reservation holder (i.e., the reservation type is Write Exclusive - All Registrants or Exclusive
Access - All Registrants) or is the only reservation holder, then the reservation is released when the host
unregisters.


If a reservation is released and the type of the released reservation was Write Exclusive - Registrants Only
or Exclusive Access - Registrants Only, then a reservation released notification occurs on all controllers
associated with a registered host other than the host that issued the Reservation Register command.


**Acquiring a Reservation**


In order for a host to obtain a reservation on a namespace, that host shall be a registrant of that namespace.
A registrant obtains a reservation by executing a Reservation Acquire command (refer to section 7.5),
clearing the Reservation Acquire Action (RACQA) field to 000b (Acquire), and supplying the current
reservation key associated with the host in the Current Reservation Key (CRKEY) field. The CRKEY value
shall match that used by the registrant to register with the namespace. If the CRKEY value does not match,
then the command is aborted with a status code of Reservation Conflict. If the host is not a registrant, then
the command is aborted with a status code of Reservation Conflict.


Only one reservation is allowed at a time on a namespace. If a registrant attempts to obtain a reservation
on a namespace that already has a reservation holder, then the command is aborted with a status code of
Reservation Conflict. If a reservation holder attempts to obtain a reservation of a different type on a
namespace for which that host already is the reservation holder, then the command is aborted with a status
code of Reservation Conflict. If a reservation holder attempts to obtain a reservation of the same type on a
namespace for which that host already is the reservation holder, then it is not a Reservation Conflict and
the command is processed. A reservation holder may preempt a reservation to change the reservation type.


**Releasing a Reservation**


Only a reservation holder is able to release a reservation held on a namespace. A host should release a
reservation using the following sequence:


a) executing a Reservation Release command (refer to section 7.7);
b) clearing the Reservation Release Action (RRELA) field to 000b (i.e., Release);
c) setting the Reservation Type (RTYPE) field to the type of reservation being released; and
d) supplying the current reservation key associated with the host in the Current Reservation Key

(CRKEY) field. The CRKEY value shall match that used by the host to register with the namespace.


If the key value does not match, then the command is aborted with a status code of Reservation Conflict. If
the RTYPE field does not match the type of the current reservation, then the command completes with a
status code of Invalid Field in Command.


An attempt by a registrant to release a reservation using the Reservation Release command in the absence
of a reservation held on the namespace or when the host is not the reservation holder shall cause the
command to complete successfully, but shall have no effect on the controller or namespace.


When a reservation is released as a result of actions described in this section and the reservation type is
not Write Exclusive or Exclusive Access, a reservation released notification occurs on all controllers in the
NVM subsystem that are associated with hosts that are registrants except for controllers that are associated
with the host that issued the Reservation Release command.


**Preempting a Reservation or Registration**


A host that is a registrant may preempt a reservation and/or registration by executing a Reservation Acquire
command (refer to section 7.5), specifying:


560


NVM Express [®] Base Specification, Revision 2.2


  - the Reservation Acquire Action (RACQA) field set to 001b (i.e., Preempt) or set to 010b (i.e.,
Preempt and Abort); and

  - the current reservation key associated with the host in the Current Reservation Key (CRKEY) field.


The CRKEY value shall match that used by the registrant to register with the namespace. If the CRKEY
value does not match, then the command is aborted with a status code of Reservation Conflict. The preempt
actions that occur are dependent on the type of reservation held on the namespace, if any, and the value
of the Preempt Reservation Key (PRKEY) field in the command. If the host is not a registrant, then the
command is aborted with a status code of Reservation Conflict. The remainder of this section assumes that
the host is a registrant.


If the existing reservation type is not Write Exclusive - All Registrants and not Exclusive Access - All
Registrants, then the actions performed by the command depend on the value of the PRKEY field as
follows:


a) If the PRKEY field value matches the reservation key of the current reservation holder, then the

following occur as an atomic operation:

    - all registrants with a matching reservation key other than the host that issued the command
are unregistered;

    - the reservation is released; and

    - a new reservation is created of the type specified by the Reservation Type (RTYPE) field in the
command for the host that issued the command as the reservation key holder;


or


b) If the PRKEY field value does not match that of the current reservation holder and is not equal to

0h, then registrants whose reservation key matches the value of the PRKEY field are unregistered.
If the PRKEY field value does not match that of the current reservation holder and is equal to 0h,
then the command is aborted with a status code of Invalid Field in Command.


If the existing reservation type is Write Exclusive - All Registrants or Exclusive Access - All Registrants,
then the actions performed by the command depend on the value of the PRKEY field as follows:


a) If the PRKEY field value is 0h, then the following occurs as an atomic operation:

    - all registrants other than the host that issued the command are unregistered;

    - the reservation is released; and

    - a new reservation is created of the type specified by the Reservation Type (RTYPE) field in the
command for the host that issued the command as the reservation key holder;


or


b) If the PRKEY value is non-zero, then registrants whose reservation key matches the value of the

PRKEY field are unregistered. If the PRKEY value is non-zero and there are no registrants whose
reservation key matches the value of the PRKEY field, the controller shall abort the command with
a status code of Reservation Conflict.


If there is no reservation held on the namespace, then execution of the command causes registrants whose
reservation key match the value of the PRKEY field to be unregistered.


If the existing reservation type is not Write Exclusive - All Registrants and not Exclusive Access - All
Registrants, then a reservation holder may preempt itself using the above mechanism. When a host
preempts itself, the following occurs as an atomic operation:

  - registration of the host is maintained;

  - the reservation is released; and

  - a new reservation is created for the host of the type specified by the RTYPE field.


A host may abort commands as a side effect of preempting a reservation by executing a Reservation
Acquire command (refer to section 7.5) and setting the RACQA field to 010b (Preempt and Abort). The


561


NVM Express [®] Base Specification, Revision 2.2


behavior of such a command is exactly the same as that described above with the RACQA field set to 001b
(Preempt), with two exceptions:

  - After the atomic operation changes namespace reservation and registration state, all controllers
associated with any host whose reservation or registration is preempted by that atomic operation
are requested to abort all commands being processed that were addressed to the specified
namespace in the NSID field in the Reservation Acquire command (refer to section 3.4.4 for the
definition of “being processed”); and

  - Completion of the Reservation Acquire command shall not occur until all commands that are
requested to be aborted are completed, regardless of whether or not each command is actually
aborted.


As with the Abort command (refer to section 5.1), aborting a command as a side effect of preempting a
reservation is best effort; as a command that is requested to be aborted may currently be at a point in
execution where that command is no longer able to be aborted or may have already completed, when a
Reservation Acquire or Abort Admin command is submitted. Although prompt execution of abort requests
reduces delay in completing the Reservation Acquire command, a command which is requested to be
aborted shall either be aborted or otherwise completed before the completion of the Reservation Acquire
command.


When a registrant is unregistered as a result of actions described in this section, then a registration
preempted notification occurs on all controllers associated with a host that was unregistered other than the
host that issued the Reservation Acquire command.


When the type of reservation held on a namespace changes as a result of actions described in this section,
then a reservation released notification occurs on all controllers associated with hosts that remain
registrants of the namespace except the host that issued the Reservation Acquire command.


**Clearing a Reservation**


A host that is a registrant may clear a reservation (i.e., force the release of a reservation held on the
namespace and unregister all registrants) by:


a) executing a Reservation Release command (refer to section 7.7);
b) setting the Reservation Release Action (RRELA) field to 001b (i.e., Clear); and
c) supplying the current reservation key associated with the host in the Current Reservation Key

(CRKEY) field.


If the value in the CRKEY field does not match the value used by the host to register with the namespace,
then the command shall be aborted with a status code of Reservation Conflict. If the host is not a registrant,
then the command is aborted with a status code of Reservation Conflict. When a command to clear a
reservation is executed the following occur as an atomic operation: the reservation held on the namespace,
if any, is released, and all registrants are unregistered from the namespace.


A reservation preempted notification occurs on all controllers in the NVM subsystem that are associated
with hosts that have their registrations removed as a result of actions taken in this section except those
associated with the host that issued the Reservation Release command.


**Reporting Reservation Status**


A host may determine the current reservation status associated with a namespace by executing a
Reservation Report command (refer to section 7.8).


**Rotational Media**


Rotational media has different operational, endurance and performance characteristics than non-rotational
media (e.g., NAND). Rotational media utilizes electromechanical methods for accessing data.


Rotational media contains one or more spinning platters containing the media, and one or more actuators
that provide physical access to the data on that media (e.g., a hard disk drive or a CD-ROM).


A controller that supports namespaces that store user data on rotational media shall:


562


NVM Express [®] Base Specification, Revision 2.2


a) set the Rotational Media bit to ‘1’ in the NSFEAT field of the I/O Command Set Independent Identify

Namespace data structure (refer to the NVM Command Set Specification) for any namespace that
stores data on rotational media;
b) support the Rotational Media Information log page (refer to section 5.1.12.1.22);
c) support the Spinup Control feature (refer to section 5.1.25.1.18);
d) support Endurance Groups (refer to section 3.2.3); and
e) set the EG Rotational Media bit to ‘1’ in the EGFEAT field in the Endurance Group Information log

page for each Endurance Group that stores data on rotational media.


If a namespace that stores data on rotational media is attached to a controller, and the spindle used by that
namespace is not spinning, then that controller shall be in a non-operational power state (i.e., NOPS is set
to ‘1’, refer to Figure 314).


If:


a) a domain contains an Endurance Group that stores data on rotational media;
b) that domain processes an NVM Subsystem Reset; and
c) the Spinup Control feature (refer to section 5.1.25.1.18) is:


a. disabled, then initial spinup for all such Endurance Groups in that domain shall be initiated;

and
b. enabled, then initial spinup for all such Endurance Groups in that domain shall be inhibited

during processing of the NVM Subsystem Reset until any controller within that domain
processes a Set Features (Power Management) command that specifies an operational
power state.


If the PCIe transport is used for a controller, then the PCIe Slot Power Control feature may affect the power
states supported (refer to the PCI Express Base Specification).


**Sanitize Operations**


A sanitize operation alters all user data in the sanitization target such that recovery of any previous user
data from any cache, the non-volatile storage media, or any Controller Memory Buffer is not possible. It is
implementation specific whether Submission Queues and Completion Queues within a Controller Memory
Buffer are altered by a sanitize operation; all other data stored in all Controller Memory Buffers is altered
by a sanitize operation. If a portion of the user data was not altered and the sanitize operation completed
successfully, then the NVM subsystem shall ensure permanent inaccessibility of that portion of the media
allocated for user data for any future use within the NVM subsystem (e.g., retrieval from NVM media,
caches, or any Controller Memory Buffer) and permanent inaccessibility of that portion of the media
allocated for user data via any interface to the NVM subsystem, including management interfaces as
defined by the NVM Express Management Interface Specification.


**Elements of Sanitize Operations**


A sanitize operation consists of:

  - sanitize processing, which may include:


`o` deallocation of all media allocated for user data; and

`o` additional media modification;

  - optional verification of media allocated for user data; and

  - post-verification deallocation of all media allocated for user data following media verification, if any.


Sanitize processing is performed in either restricted completion mode (i.e., in the Restricted Processing
state) or in unrestricted completion mode (i.e., in the Unrestricted Processing state), as specified by the
Allow Unrestricted Sanitize Exit (AUSE) bit in the Sanitize command (refer to Figure 373).


Additional media modification may be performed as part of sanitize processing (i.e., in the Restricted
Processing state or the Unrestricted Processing state) to prevent commands that access media after
completion of sanitize processing from encountering data integrity errors caused by that sanitize
processing.


563


NVM Express [®] Base Specification, Revision 2.2


Additional media modification shall be performed if the NODMMAS field is set to 10b (refer to Figure 313)
and the Sanitize command that started the sanitize operation specifies:


  - the Enter Media Verification State (EMVS) bit cleared to ‘0’; and

  - the No-Deallocate After Sanitize (NDAS) bit set to ‘1’.


Verification of media allocated for user data is able to be performed by the host if the Sanitize Operation
State Machine is in the Media Verification state. A Block Erase sanitize operation or Crypto Erase sanitize
operation may invalidate error correction codes on the media, causing subsequent reads to fail because of
media errors. In the Media Verification state, reads are successful regardless of such invalid error correction
codes which enables the host to perform an audit (refer to section 1.5.11) to verify that the media was
sanitized. Refer to the applicable I/O Command Set specification for details. Media verification is performed
if the Sanitize command that starts a sanitize operation specifies the EMVS bit set to ‘1’ and sanitize
processing completes successfully.


If a sanitize operation includes deallocation of all media allocated for user data, then that deallocation shall
be performed in exactly one of the following states:


  - Restricted Processing state;

  - Unrestricted Processing state; or

  - Post-Verification Deallocation state.


If the Sanitize command (refer to Figure 373) that starts a sanitize operation specifies:


  - the Enter Media Verification State (EMVS) bit cleared to ‘0’;

  - the AUSE bit cleared to ‘0’; and

  - the No-Deallocate After Sanitize (NDAS) bit is:


`o` cleared to ‘0’; or

`o` set to ‘1’ and the controller encounters a condition that results in unexpected deallocation
of all media allocated for user data (refer to section 5.1.25.1.15),


then deallocation of all media allocated for user data shall be performed in the Restricted Processing state.
If that deallocation fails, then sanitize processing fails.


If Media Verification state is canceled (i.e., the MVCNCLD bit is set to ‘1’) during the Restricted Processing
state, then deallocation of all media allocated for user data shall be performed in the Restricted Processing
state.


If the Sanitize command that starts a sanitize operation specifies:


  - the Enter Media Verification State (EMVS) bit cleared to ‘0’;

  - the AUSE bit set to ‘1’; and

  - the No-Deallocate After Sanitize (NDAS) bit is:


`o` cleared to ‘0’; or

`o` set to ‘1’ and the controller encounters a condition that results in unexpected deallocation
of all media allocated for user data (refer to section 5.1.25.1.15),


then deallocation of all media allocated for user data shall be performed in the Unrestricted Processing
state. If that deallocation fails, then sanitize processing fails.


If the Media Verification state is canceled (i.e., the MVCNCLD bit is set to ‘1’) during the Unrestricted
Processing state, then deallocation of all media allocated for user data shall be performed in the
Unrestricted Processing state.


In the Post-Verification Deallocation state the controller deallocates all user data.


In the Post-Verification Deallocation state, if the controller:


  - successfully completes deallocating all media allocated for user data, then the sanitization target
enters the Idle state; or


564


NVM Express [®] Base Specification, Revision 2.2


  - fails to deallocate all media allocated for user data, then the sanitization target enters the Restricted
Failure state or the Unrestricted Failure state, as described in section 8.1.24.3.7.


A Controller Level Reset may cause the sanitize operation not to include the Media Verification state and
the Post-Verification Deallocation state, as described in section 8.1.24.3.


**Sanitize Operation Types and Support**


The scope of a sanitize operation is all locations in the NVM subsystem that are able to contain user data,
including caches, Persistent Memory Regions, and unallocated or deallocated areas of the media.


If the composition of the NVM subsystem (refer to section 3.2.5) changes (e.g., a new domain is added, or
a division event occurs) and that change prevents the successful completion of a sanitize operation, then
the sanitize operation shall fail.


If the composition of the NVM subsystem changes (e.g., a new domain is added, or a division event occurs)
and that change prevents verification of media allocated for user data, then the Media Verification state is
canceled and the MVCNCLD bit is set to ‘1’.


Sanitize operations do not affect the Replay Protected Memory Block, boot partitions, or other media and
caches that do not contain user data. A sanitize operation also may alter log pages and features as
necessary (e.g., to prevent derivation of user data from log page information or feature information). A
sanitize operation is only able to be started if the NVM subsystem is not divided (refer to section 3.2.5). A
sanitize operation in the Restricted Processing state, the Unrestricted Processing state, the Media
Verification state, or the Post-Verification Deallocation state is not able to be aborted and continues after a
Controller Level Reset, including across power cycles. Refer to Annex A for further information about
sanitize operations.


The Sanitize command (refer to section 5.1.22) is used to start a sanitize operation, to recover from a
previously failed sanitize operation, or to exit the Media Verification state. All sanitize operations are
performed in the background (i.e., completion of the Sanitize command that starts a sanitize operation does
not indicate completion of that sanitize operation). The completion of a sanitize operation and the optional
transition into the Media Verification state are indicated in the Sanitize Status log page, and with:

  - the Sanitize Operation Completed asynchronous event,

  - the Sanitize Operation Completed With Unexpected Deallocation asynchronous event, or

  - the Sanitize Operation Entered Media Verification State asynchronous event.


If the Sanitize command that started a sanitize operation was submitted to a controller’s Admin Submission
Queue, then the asynchronous event shall be reported only by that controller. If the Sanitize command that
started a sanitize operation was submitted to a Management Endpoint (refer to the NVM Express
Management Interface Specification), then the asynchronous event shall not be reported by any controller
in the NVM subsystem.


The Sanitize Capabilities (SANICAP) field of the Identify Controller data structure (refer to Figure 313)
indicates the sanitize operation types supported and controller attributes specific to sanitize operations.


The sanitize operation types are:

  - the Block Erase sanitize operation, which alters user data with a low-level block erase method that
is specific to the media for all locations on the media within the sanitization target in which user
data may be stored;

  - the Crypto Erase sanitize operation, which alters user data by changing the media encryption keys
for all locations on the media within the sanitization target in which user data may be stored; and

  - the Overwrite sanitize operation, which alters user data by writing a fixed data pattern or related
patterns one or more times to all locations on the media within the sanitization target in which user
data may be stored. Figure 648 defines the data pattern or patterns that are written.


Controller attributes specific to sanitize operations include:

  - the No-Deallocate Modifies Media After Sanitize (NODMMAS) field, which indicates whether media
is modified by the controller as part of sanitize processing that had been requested with the No

565


NVM Express [®] Base Specification, Revision 2.2


Deallocate After Sanitize (NDAS) bit set to ‘1’ in the Sanitize command that started the sanitize
operation;

  - the No-Deallocate Inhibited (NDI) bit, which indicates if the controller supports the No-Deallocate
After Sanitize bit in the Sanitize command; and

  - the Verification Support (VERS) bit, which indicates if the controller supports the Media Verification
state and the Post-Verification Deallocation state for sanitization operations that perform block
erase or crypto erase.


If the NODMMAS field indicates a value of 10b in the Identify Controller data structure (refer to Figure 313)
and a Sanitize command that starts a sanitize operation specifies the No-Deallocate After Sanitize (NDAS)
bit set to ‘1’, then sanitize processing includes additional media modification. Refer to Annex A.3 for further
information about sanitize operations and interactions with integrity circuits.


The Overwrite sanitize operation is media specific and may not be appropriate for all media types. For
example, if the media is NAND, multiple pass overwrite operations may have an adverse effect on media
endurance.


If the NVM subsystem supports the Key Per I/O capability (refer to section 8.1.11), then a sanitize operation
shall alter all user data such that recovery of any previous user data using the KEYTAG values specified
when that previous user data was written (i.e., original KEYTAG values) is infeasible for a given level of
effort (refer to ISO/IEC 27040).


**Figure 648: Sanitize Operations – Overwrite Mechanism**
















|1<br>OIPBP|Overwrite<br>1<br>Pass Count|Overwrite<br>Pass Number|User Data except PI Metadata|2<br>Protection Information|
|---|---|---|---|---|
|‘0’|All|All|Overwrite Pattern1|Each byte set to FFh|
|‘1’|Even|First|Inversion of Overwrite Pattern1|Each byte cleared to 00h|
|‘1’|Even|Subsequent|Inversion of Overwrite Pattern1 from previous pass (i.e., each bit<br>XORed with ‘1’)|Inversion of Overwrite Pattern1 from previous pass (i.e., each bit<br>XORed with ‘1’)|
|‘1’|Odd|First|Overwrite Pattern1|Each byte set to FFh|
|‘1’|Odd|Subsequent|Inversion of Overwrite Pattern1 from previous pass (i.e., each bit<br>XORed with ‘1’)|Inversion of Overwrite Pattern1 from previous pass (i.e., each bit<br>XORed with ‘1’)|
|Notes:<br>1.<br>Parameters are specified in Command Dword 10 and Command Dword 11 of the corresponding Sanitize<br>command that started the Overwrite operation. The Overwrite Invert Pattern Between Passes (OIPBP) field is<br>defined in Command Dword 10. The Overwrite Pass Count field is defined in Command Dword 10. The<br>Overwrite Pattern field is defined in Command Dword 11. Refer to section 5.1.22.<br>2.<br>If Protection Information is present within the metadata.|Notes:<br>1.<br>Parameters are specified in Command Dword 10 and Command Dword 11 of the corresponding Sanitize<br>command that started the Overwrite operation. The Overwrite Invert Pattern Between Passes (OIPBP) field is<br>defined in Command Dword 10. The Overwrite Pass Count field is defined in Command Dword 10. The<br>Overwrite Pattern field is defined in Command Dword 11. Refer to section 5.1.22.<br>2.<br>If Protection Information is present within the metadata.|Notes:<br>1.<br>Parameters are specified in Command Dword 10 and Command Dword 11 of the corresponding Sanitize<br>command that started the Overwrite operation. The Overwrite Invert Pattern Between Passes (OIPBP) field is<br>defined in Command Dword 10. The Overwrite Pass Count field is defined in Command Dword 10. The<br>Overwrite Pattern field is defined in Command Dword 11. Refer to section 5.1.22.<br>2.<br>If Protection Information is present within the metadata.|Notes:<br>1.<br>Parameters are specified in Command Dword 10 and Command Dword 11 of the corresponding Sanitize<br>command that started the Overwrite operation. The Overwrite Invert Pattern Between Passes (OIPBP) field is<br>defined in Command Dword 10. The Overwrite Pass Count field is defined in Command Dword 10. The<br>Overwrite Pattern field is defined in Command Dword 11. Refer to section 5.1.22.<br>2.<br>If Protection Information is present within the metadata.|Notes:<br>1.<br>Parameters are specified in Command Dword 10 and Command Dword 11 of the corresponding Sanitize<br>command that started the Overwrite operation. The Overwrite Invert Pattern Between Passes (OIPBP) field is<br>defined in Command Dword 10. The Overwrite Pass Count field is defined in Command Dword 10. The<br>Overwrite Pattern field is defined in Command Dword 11. Refer to section 5.1.22.<br>2.<br>If Protection Information is present within the metadata.|



To start a sanitize operation, the host submits a Sanitize command specifying the SANACT field set to:

  - 010b (i.e., start a Block Erase type sanitize operation);

  - 011b (i.e., start a Overwrite type sanitize operation); or

  - 100b (i.e., start a Crypto Erase type sanitize operation).


The Sanitize command specifies other parameters, including:

  - the Allow Unrestricted Sanitize Exit (AUSE) bit;

  - the No-Deallocate After Sanitize (NDAS) bit; and

  - the Enter Media Verification State (EMVS) bit.


After validating the Sanitize command parameters, the controller starts the sanitize operation in the
background, updates the Sanitize Status log page and then completes the Sanitize command with
Successful Completion status.


566


NVM Express [®] Base Specification, Revision 2.2


If a Sanitize command is completed with any status code other than Successful Completion, then the
controller shall not start the sanitize operation and shall not update the Sanitize Status log page. The
controller shall ignore Critical Warning(s) in the SMART / Health Information log page (e.g., read only mode)
and shall attempt to complete the sanitize operation requested. Refer to section 5 for further information
about restrictions on Admin commands during the processing of a Sanitize command.


Following a successful sanitize operation, the values of user data (including protection information (PI), if
any, and non-PI metadata, if any) that result from an audit (refer to section 1.5.11) of the sanitization target
are defined in the I/O command set specifications.


The Sanitize Status log page (refer to section 5.1.12.1.33) indicates estimated times for sanitize operations
and a consistent snapshot of information about the most recently started sanitize operation, including
whether a sanitize operation is in progress, the sanitize operation parameters and the status of the most
recent sanitize operation. The controller shall report that a sanitize operation is in progress if:

  - sanitize processing is in progress (including additional media modification, if required);

  - the sanitization target is in the Media Verification state; or

  - the sanitization target is in the Post-Verification Deallocation state.


If a sanitize operation is not in progress, then the Global Data Erased (GDE) bit in the log page indicates
whether the sanitization target may contain any user data (i.e., whether the sanitization target has been
written to since the most recent successful sanitize operation).


The Sanitize Status log page shall be:

  - initialized before any controller in the NVM subsystem is ready as described in sections 3.5.3 and
3.5.4; and

  - updated when any state transition occurs (refer to section 8.1.24.3).


The Sanitize Status log page is updated periodically during a sanitize operation to make progress
information available to hosts.


During a sanitize operation, the host may periodically examine the Sanitize Status log page to check for
progress, however, the host should limit this polling (e.g., to at most once every several minutes) to avoid
interfering with the progress of the sanitize operation itself.


The Sanitize Progress (SPROG) field in the Sanitize Status log page indicates progress during states that
may take long times to complete (i.e., the Restricted Processing state, the Unrestricted Processing state,
and the Post-Verification Deallocation state). The SPROG field is cleared to 0h upon entry to any of those
states, and while in any of those states is updated as described in Figure 292. The SPROG field shall not
be modified under any conditions not explicitly permitted by this specification.


A sanitize operation completes when the sanitization target enters any of the following states (refer to
section 8.1.24.3):

  - the Idle state;

  - the Restricted Failure state; or

  - the Unrestricted Failure state.


Upon completion of a sanitize operation or upon entry to the Media Verification state, the host should read
the Sanitize Status log page with the Retain Asynchronous Event bit cleared to ‘0’ (which clears the
asynchronous event, if one was generated).


If a sanitize operation fails (i.e., the sanitization target enters the Restricted Failure state or the Unrestricted
Failure state), all controllers in the NVM subsystem shall abort any command not allowed during a sanitize
operation with a status code of Sanitize Failed (refer to section 8.1.24.3) until a subsequent sanitize
operation is started or successful recovery from the failed sanitize operation occurs. A subsequent
successful sanitize operation or the Exit Failure Mode action may be used to recover from a failed sanitize
operation. Refer to section 5.1.22 for recovery details.


If the Sanitize command is supported, then all controllers in the NVM subsystem shall:


567


NVM Express [®] Base Specification, Revision 2.2


  - support the Sanitize Status log page;

  - support the Sanitize Operation Completed asynchronous event;

  - support the Sanitize Operation Completed With Unexpected Deallocation asynchronous event, if
the Sanitize Config feature is supported;

  - support the Exit Failure Mode action for a Sanitize command;

  - support at least one of the following sanitize operation types: Block Erase, Overwrite, or Crypto
Erase;

  - support the same set of sanitize operation types;

  - indicate the supported sanitize operation types in the Sanitize Capabilities field in the Identify
Controller data structure; and

  - if the Verification Support (VERS) bit is set to ‘1’ in the Identify Controller data structure (refer to
Figure 313), support:


`o` the FAILS field in the Sanitize Status log page (refer to section 5.1.12.1.33);

`o` the SANS field in the Sanitize Status log page;

`o` the Media Verification state;

`o` the Post-Verification Deallocation state; and

`o` the Sanitize Operation Entered Media Verification State asynchronous event.


The Sanitize Config Feature Identifier (refer to section 5.1.25.1.15) contains the No-Deallocate Response
Mode (NODRM) bit that specifies the response of the controller to a Sanitize command specifying the NoDeallocate After Sanitize (NDAS) bit (refer to Figure 373) set to ‘1’ if the No-Deallocate Inhibited bit is set
to ‘1’ in the Sanitize Capabilities field of the Identify Controller data structure (refer to Figure 313). In the
No-Deallocate Error Response Mode, the controller aborts such Sanitize commands with a status code of
Invalid Field in Command. In the No-Deallocate Warning Response Mode, the controller processes such
Sanitize commands, and if a resulting sanitize operation is completed successfully, then the SOS field is
set to 100b (i.e., Sanitized Unexpected Deallocate) in the Sanitize Status log page (refer to Figure 292).


**Sanitize Operation State Machine**


The Sanitize Operation State Machine (refer to Figure 649) defines the state of sanitization of a sanitization
target. The label on each transition begins with a letter and may include a number. The letter indicates the
condition causing that transition, as described in the section for each state. The number differentiates
between different transitions that have the same transition condition.


568


NVM Express [®] Base Specification, Revision 2.2


**Figure 649: Sanitize Operation State Machine**

















































In the state transitions described in this section, asynchronous events are reported as described in section
8.1.24.2. In Completion Queue Entry Dword 0 (refer to Figure 148) for the Asynchronous Event Request
command:


a) the Log Page Identifier field shall be set to 81h (i.e., Sanitize Status log page);
b) the Asynchronous Event Information field (refer to section 5.1.2.1) shall be set to:

    - 01h (i.e., Sanitize Operation Completed);

    - 02h (i.e., Sanitize Operation Completed With Unexpected Deallocation); or

    - 03h (i.e., Sanitize Operation Entered Media Verification State);


and


c) the Asynchronous Event Type field shall be set to 110b (i.e., I/O Command specific status).


In each state transition described in this section, the controller shall set the Sanitize State (SANS) field to
the value corresponding to the state being entered.


**8.1.24.3.1 Idle State**


In this state, no sanitize operation is in process. This state applies in the following cases:


a) no sanitize operation has ever been performed on the NVM subsystem since the NVM subsystem

was manufactured;
b) the most recent sanitize operation on the NVM subsystem was successful; and
c) the most recent sanitize operation failed in unrestricted completion mode (i.e., the Sanitize

command specified the AUSE bit set to ‘1’) and then the Sanitize Operation State Machine
transitioned from the Unrestricted Failure state to the Idle state when any controller in the NVM
subsystem performed an Exit Failure Mode action.


In this state, any controller in the NVM subsystem processing a Sanitize command specifying the Sanitize
Action field set to 001b (i.e., Exit Failure Mode) shall not be considered an error.


In this state, all controllers in the NVM subsystem are permitted to resume any power management that
was suspended by any prior sanitize operation.


569


NVM Express [®] Base Specification, Revision 2.2


**Figure 650: Idle State Transition Conditions**









|State Transition|Col2|Col3|Transition Condition|
|---|---|---|---|
|**Starting**|**Ending**|**Label1 **|**Label1 **|
|Idle|Restricted<br>Processing|A1|The controller starts a sanitize operation in restricted completion mode (i.e.,<br>the Sanitize command specified the AUSE bit cleared to ‘0’).|
|Idle|Unrestricted<br>Processing|B1|The controller starts a sanitize operation in unrestricted completion mode<br>(i.e., the Sanitize command specified the AUSE bit set to ‘1’).|
|Notes:<br>1.<br>Refer to Figure 649.|Notes:<br>1.<br>Refer to Figure 649.|Notes:<br>1.<br>Refer to Figure 649.|Notes:<br>1.<br>Refer to Figure 649.|


**Transition Idle:Restricted Processing:**


The controller shall clear the:


a) Sanitize Progress (SPROG) field to 0h; and
b) Media Verification Canceled (MVCNCLD) bit to ‘0’.


**Transition Idle:Unrestricted Processing:**


The controller shall clear the:


a) Sanitize Progress (SPROG) field to 0h; and
b) Media Verification Canceled (MVCNCLD) bit to ‘0’.


**8.1.24.3.2 Restricted Processing State**


In this state, if the sanitize operation fails, then the sanitization target transitions to the Restricted Failure
state.


In this state:


a) the controller shall set the Sanitize Progress (SPROG) field as described in Figure 292;
b) the controller shall perform additional media modification, if required, as described in section

8.1.24.1;
c) the controller should deallocate all media allocated for user data, if permitted, as described in

section 8.1.24.1;
d) if a change in the composition of the NVM subsystem occurs then the MVCNCLD bit shall be set

to ‘1’;
e) if a Controller Level Reset of any controller in the NVM subsystem occurs that is caused by:

      - a transport-specific reset type (refer to the applicable NVMe Transport specification); or

      - an NVM Subsystem Reset,


then the MVCNCLD bit shall be set to ‘1; and
f) all controllers and Management Endpoints in the NVM subsystem shall process commands as
described in section 8.1.24.4.


570


NVM Express [®] Base Specification, Revision 2.2


**Figure 651: Restricted Processing State Transition Conditions**












|State Transition|Col2|Col3|Transition Condition|
|---|---|---|---|
|**Starting**|**Ending**|**Label1 **|**Label1 **|
|Restricted<br>Processing|Idle|C1|Sanitize processing completes successfully and the EMVS bit was:<br>a)<br>cleared to ‘0’ in the Sanitize command that started the sanitize<br>operation; or<br>b)<br>set to ‘1’ in the Sanitize command that started the sanitize<br>operation, the MVCNCLD bit is set to ‘1’, and deallocation of all<br>media allocated for user data completes successfully.|
|Restricted<br>Processing|Restricted<br>Failure|D1|Sanitize processing fails.|
|Restricted<br>Processing|Media<br>Verification|F1|The EMVS bit was set to ‘1’ in the Sanitize command that started the<br>sanitize operation, the sanitize processing completes successfully, and<br>the MVCNCLD bit is cleared to ‘0’.|
|Notes:<br>1.<br>Refer to Figure 649.|Notes:<br>1.<br>Refer to Figure 649.|Notes:<br>1.<br>Refer to Figure 649.|Notes:<br>1.<br>Refer to Figure 649.|



**Transition Restricted Processing:Idle:**


The controller shall:


a) report the Sanitize Operation Completed asynchronous event or the Sanitize Operation Completed

With Unexpected Deallocation asynchronous event as described in section 8.1.24.2.


**Transition Restricted Processing:Restricted Failure:**


The controller shall:


a) set the FAILS field to 1h (i.e., Restricted Processing state); and
b) report the Sanitize Operation Completed asynchronous event or the Sanitize Operation Completed

With Unexpected Deallocation asynchronous event as described in section 8.1.24.2.


**Transition Restricted Processing:Media Verification:**


The controller shall:


a) report the Sanitize Operation Entered Media Verification State asynchronous event as described

in section 8.1.24.2.


**8.1.24.3.3 Restricted Failure State**


This state is entered if sanitize processing was performed in the Restricted Processing state and:


a) sanitize processing failed; or
b) a failure occurred during deallocation of media allocated for user data in the Post-Verification

Deallocation state.


In this state:


a) all controllers and Management Endpoints in the NVM subsystem shall process commands as

described in section 8.1.24.4;
b) failure recovery requires the host to issue a subsequent Sanitize command specifying the AUSE

bit cleared to ‘0’ (i.e., restricted completion mode);
c) all controllers in the NVM subsystem shall abort a Sanitize command specifying:


    - the SANACT field set to 001b (i.e., Exit Failure Mode), with a status code of Sanitize Failed;

    - the SANACT field set to 101b (i.e., Exit Media Verification State), with a status code of Invalid
Field in Command; or

    - the USE bit set to ‘1’ (i.e., unrestricted completion mode), with a status code of Sanitize Failed;


571


NVM Express [®] Base Specification, Revision 2.2


and


d) the Persistent Memory Region shall behave as described in section 8.1.24.4.


**Figure 652: Restricted Failure State Transition Conditions**













|State Transition|Col2|Col3|Transition Condition|
|---|---|---|---|
|**Starting**|**Ending**|**Label**<br>**1 **|**Label**<br>**1 **|
|Restricted<br>Failure|Restricted<br>Processing|A2|The controller starts a sanitize operation in restricted completion mode<br>(i.e., the Sanitize command specified the AUSE bit cleared to ‘0’).|
|Notes:<br>1.<br>Refer to Figure 649.|Notes:<br>1.<br>Refer to Figure 649.|Notes:<br>1.<br>Refer to Figure 649.|Notes:<br>1.<br>Refer to Figure 649.|


**Transition Restricted Failure:Restricted Processing:**


The controller shall start a sanitize operation in the Restricted Processing state. The controller shall:


a) clear the Sanitize Progress (SPROG) field to 0h; and
b) clear the Media Verification Canceled (MVCNCLD) bit to ‘0’.


**8.1.24.3.4 Unrestricted Processing State**


In this state, if the sanitize operation fails, then the sanitization target transitions to the Unrestricted Failure
state, from which it is able to transition to the Idle state without successful sanitization.


In this state:


a) the controller shall set the Sanitize Progress (SPROG) field as described in Figure 292;
b) the controller shall perform additional media modification, if required, as described in section

8.1.24.1;
c) the controller should deallocate all media allocated for user data, if permitted, as described in

section 8.1.24.1;
d) if a change in the composition of the NVM subsystem occurs, then the MVCNCLD bit shall be set

to ‘1;
e) if a Controller Level Reset of any controller in the NVM subsystem occurs that is caused by:


    - a transport-specific reset type (refer to the applicable NVMe Transport specification); or

    - an NVM Subsystem Reset,


then the MVCNCLD bit shall be set to ‘1; and


f) all controllers and Management Endpoints in the NVM subsystem shall process commands as
described in section 8.1.24.4.


572


NVM Express [®] Base Specification, Revision 2.2


**Figure 653: Unrestricted Processing State Transition Conditions**












|State Transition|Col2|Col3|Transition Condition|
|---|---|---|---|
|**Starting**|**Ending**|**Label1 **|**Label1 **|
|Unrestricted<br>Processing|Idle|C2|The sanitize processing completes successfully and the EMVS bit was:<br>a)<br>cleared to ‘0’ in the Sanitize command that started the sanitize<br>operation; or<br>b)<br>set to ‘1’ in the Sanitize command that started the sanitize<br>operation, the MVCNCLD bit is set to ‘1’, and deallocation of all<br>media allocated for user data completes successfully.|
|Unrestricted<br>Processing|Unrestricted<br>Failure|D2|The sanitize processing fails.|
|Unrestricted<br>Processing|Media<br>Verification|F2|The EMVS bit was set to ‘1’ in the Sanitize command that started the<br>sanitize operation, the sanitize processing completes successfully, and<br>the MVCNCLD bit is cleared to ‘0’.|
|Notes:<br>1.<br>Refer to Figure 649.|Notes:<br>1.<br>Refer to Figure 649.|Notes:<br>1.<br>Refer to Figure 649.|Notes:<br>1.<br>Refer to Figure 649.|



**Transition Unrestricted Processing:Idle:**


The controller shall:


a) report the Sanitize Operation Completed asynchronous event or the Sanitize Operation Completed

With Unexpected Deallocation asynchronous event as described in section 8.1.24.2.


**Transition Unrestricted Processing:Unrestricted Failure:**


The controller shall:


a) set the FAILS field to 3h (i.e., Unrestricted Processing state); and
b) report the Sanitize Operation Completed asynchronous event or the Sanitize Operation Completed

With Unexpected Deallocation asynchronous event as described in section 8.1.24.2.


**Transition Unrestricted Processing:Media Verification:**


The controller shall:


a) report the Sanitize Operation Entered Media Verification State asynchronous event as described

in section 8.1.24.2.


**8.1.24.3.5 Unrestricted Failure State**


This state is entered if sanitize processing was performed in the Unrestricted Processing state and:


a) sanitize processing failed; or
b) a failure occurred during deallocation of media allocated for user data in the Post-Verification

Deallocation state.


In this state:


a) all controllers and Management Endpoints in the NVM subsystem shall process commands as

described in section 8.1.24.4;
b) all controllers in the NVM subsystem shall abort a Sanitize command specifying the SANACT field

set to 101b (i.e., Exit Media Verification State) with a status code of Invalid Field in Command;
c) all controllers in the NVM subsystem shall abort a Sanitize command specifying the SANACT field

set to a value other than:


    - 001b (i.e., Exit Failure Mode);

    - 010b (i.e., Start a Block Erase sanitize operation);

    - 011b (i.e., Start an Overwrite sanitize operation); or

    - 100b (i.e., Start a Crypto Erase sanitize operation),


573


NVM Express [®] Base Specification, Revision 2.2


with a status code of Sanitize Failed; and


d) the Persistent Memory Region shall behave as described in section 8.1.24.4.


**Figure 654: Unrestricted Failure State Transition Conditions**







|State Transition|Col2|Col3|Transition Condition|
|---|---|---|---|
|**Starting**|**Ending**|**Label1 **|**Label1 **|
|Unrestricted<br>Failure|Restricted<br>Processing|A3|The controller starts a sanitize operation in restricted completion mode<br>(i.e., the Sanitize command specified the AUSE bit cleared to ‘0’).|
|Unrestricted<br>Failure|Unrestricted<br>Processing|B2|The controller starts a sanitize operation in unrestricted completion mode<br>(i.e., the Sanitize command specified the AUSE bit set to ‘1’).|
|Unrestricted<br>Failure|Idle|E|Any controller in the NVM subsystem performs an Exit Failure Mode<br>action.|
|Notes:<br>1.<br>Refer to Figure 649.|Notes:<br>1.<br>Refer to Figure 649.|Notes:<br>1.<br>Refer to Figure 649.|Notes:<br>1.<br>Refer to Figure 649.|


**Transition Unrestricted Failure:Restricted Processing:**


The controller shall start a sanitize operation in the Restricted Processing state. The controller shall:


a) clear the Sanitize Progress (SPROG) field to 0h; and
b) clear the Media Verification Canceled (MVCNCLD) bit to ‘0’.


**Transition Unrestricted Failure:Unrestricted Processing:**


The controller shall start a sanitize operation in the Unrestricted Processing state. The controller shall:


a) clear the Sanitize Progress (SPROG) field to 0h; and
b) clear the Media Verification Canceled (MVCNCLD) bit to ‘0’.


**Transition Unrestricted Failure:Idle:**


If any controller in the NVM subsystem performs an Exit Failure Mode action, then the controller shall
recover from the sanitization failure by transitioning the Sanitize Operation State Machine to the Idle state
and shall complete the Sanitize command that specified the Exit Failure Mode action with a status code of
Successful Completion.


**8.1.24.3.6 Media Verification State**


In this state, the sanitize processing completed successfully, and all media allocated for user data in the
sanitization target is readable by the host for purposes of verifying sanitization.


In this state:


a) the Sanitize Operation State Machine shall transition to the Post-Verification Deallocation state if

any controller in the NVM subsystem performs an Exit Media Verification State action;
b) all controllers in the NVM subsystem shall abort a Sanitize command specifying the SANACT field

not set to 101b (i.e., Exit Media Verification State) with a status code of Invalid Field in Command;
and
c) all controllers and Management Endpoints in the NVM subsystem shall process commands as

described in section 8.1.24.4, with exceptions as described in the appropriate I/O command set
specification (e.g., the Read command in the NVM Command Set is processed as described in the
Media Verification section of the NVM Command Set Specification).


574


NVM Express [®] Base Specification, Revision 2.2


**Figure 655: Media Verification State Transition Conditions**










|State Transition|Col2|Col3|Transition Condition|
|---|---|---|---|
|**Starting**|**Ending**|**Label1 **|**Label1 **|
|Media<br>Verification|Post-<br>Verification<br>Deallocation|G|Either:<br>a)<br>any controller in the NVM subsystem performs an Exit Media<br>Verification State action;<br>b)<br>an NVM Subsystem Reset occurs in any domain in the NVM<br>subsystem;<br>c)<br>a Controller Level Reset caused by a transport-specific reset<br>type (refer to the applicable NVMe Transport specification) of<br>any controller in the NVM subsystem occurs; or<br>d)<br>a change in the composition of the NVM subsystem prevents<br>media verification.|
|Notes:<br>1.<br>Refer to Figure 649.|Notes:<br>1.<br>Refer to Figure 649.|Notes:<br>1.<br>Refer to Figure 649.|Notes:<br>1.<br>Refer to Figure 649.|



**Transition Media Verification:Post-Verification Deallocation:**


The controller shall:


a) clear the Sanitize Progress (SPROG) field to 0h;
b) set the Media Verification Canceled (MVCNCLD) bit to ‘1’, if any controller in the NVM subsystem

processes a Controller Level Reset caused by:


    - an NVM Subsystem Reset; or

    - a transport-specific reset type (refer to the applicable NVMe Transport specification), if any;


c) set the Media Verification Canceled (MVCNCLD) bit to ‘1’, if a change in the composition of the

NVM subsystem prevents media verification; and
d) complete the Sanitize command with a status code of Successful Completion, if any controller in

the NVM subsystem performs an Exit Media Verification State action.


**8.1.24.3.7 Post-Verification Deallocation State**


In this state:


a) the controller shall deallocate all media allocated for user data in the sanitization target;
b) the Sanitize Progress (SPROG) field shall be set as described in Figure 292; and
c) all controllers and Management Endpoints in the NVM subsystem shall process commands as

described in section 8.1.24.4.


**Figure 656: Post-Verification Deallocation state Transition Conditions**
















|State Transition|Col2|Col3|Transition Condition|
|---|---|---|---|
|**Starting**|**Ending**|**Label1 **|**Label1 **|
|Post-<br>Verification<br>Deallocation|Idle|H|The controller completes deallocation of all media allocated for user<br>data.|
|Post-<br>Verification<br>Deallocation|Restricted<br>Failure|I1|The sanitize operation was started by a Sanitize command specifying<br>the AUSE bit cleared to ‘0’ (i.e., restricted completion mode), and a<br>failure occurs during deallocation of all media allocated for user data.|
|Post-<br>Verification<br>Deallocation|Unrestricted<br>Failure|I2|The sanitize operation was started by a Sanitize command specifying<br>the AUSE bit set to ‘1’ (i.e., unrestricted completion mode), and a failure<br>occurs during deallocation of all media allocated for user data.|
|Notes:<br>1.<br>Refer to Figure 649.|Notes:<br>1.<br>Refer to Figure 649.|Notes:<br>1.<br>Refer to Figure 649.|Notes:<br>1.<br>Refer to Figure 649.|



575


NVM Express [®] Base Specification, Revision 2.2


**Transition Post-Verification Deallocation:Idle:**


The controller shall:


a) report the Sanitize Operation Completed asynchronous event as described in section 8.1.24.2.


**Transition Post-Verification Deallocation:Restricted Failure:**


The controller shall:


a) report the Sanitize Operation Completed asynchronous event as described in section 8.1.24.2; and
b) set the FAILS field to 6h (i.e., Post-Verification Deallocation state).


**Transition Post-Verification Deallocation:Unrestricted Failure:**


The controller shall:


a) report the Sanitize Operation Completed asynchronous event as described in section 8.1.24.2; and
b) set the FAILS field to 6h (i.e., Post-Verification Deallocation state).


**Sanitize Operation Restrictions**


In the following states:

  - Restricted Processing;

  - Restricted Failure;

  - Unrestricted Processing;

  - Unrestricted Failure;

  - Media Verification; and

  - Post-Verification Deallocation,


all enabled controllers in the NVM subsystem are restricted to performing only a limited set of actions.


When a sanitize operation starts on any controller (i.e., a transition into the Restricted Processing state
occurs or a transition into the Unrestricted Processing state occurs), all controllers in the NVM subsystem
shall:


  - clear all of the following outstanding asynchronous events:


`o` Sanitize Operation Completed asynchronous event, if any;

`o` Sanitize Operation Completed With Unexpected Deallocation asynchronous event, if any;
and

`o` Sanitize Operation Entered Media Verification State asynchronous event, if any;


  - update the Sanitize Status log page (refer to section 5.1.12.1.33);

  - abort any command (submitted or in progress) not allowed during a sanitize operation (refer to
Figure 143) with a status code of Sanitize In Progress, unless otherwise specified;

  - abort device self-test operations in progress;

  - suspend autonomous power state management activities as described in section 8.1.17.2; and

  - release stream identifiers for any open streams.


If a sanitize operation is in any of the following states (i.e., is in progress):

  - Restricted Processing;

  - Unrestricted Processing;

  - Media Verification; or

  - Post-Verification Deallocation,


then for each controller in the NVM subsystem:

  - all I/O commands other than a Flush command shall be aborted with a status code of Sanitize In
Progress, unless otherwise specified;

  - processing of a Flush command is specified in section 7.2;


576


NVM Express [®] Base Specification, Revision 2.2


  - any command or command option that is not explicitly permitted in Figure 143 shall be aborted with
a status code of Sanitize In Progress if processed by the controller;

  - the Persistent Memory Region shall be prevented from being enabled (i.e., setting PMRCTL.EN to
‘1’ does not result in PMRSTS.NRDY being cleared to ‘0’); and

  - activation of new firmware is prohibited.


While the sanitization target is in the Restricted Failure state or the Unrestricted Failure state, then for each
controller in the NVM subsystem:

  - any command or command option that is not explicitly permitted in Figure 143 shall be aborted with
a status code of Sanitize In Progress if processed by the controller;

  - all I/O commands other than a Flush command (refer to section 7.2), shall be aborted with a status
code of Sanitize Failed;

  - the Sanitize command is permitted with action restrictions (refer to section 5.1.22); and

  - the Persistent Memory Region shall be prevented from being enabled (i.e., setting PMRCTL.EN to
‘1’ does not result in PMRSTS.NRDY being cleared to ‘0’).


When a sanitize operation starts on any controller in an NVM subsystem (i.e., a transition into the Restricted
Processing state occurs or a transition into the Unrestricted Processing state occurs), all Management
Endpoints in the NVM subsystem shall perform the sanitize operation as described in the NVM Express
Management Interface Specification.


**Sanitize Operation Effects on Exported NVM Subsystems**


Performing a sanitize operation on an Underlying NVM Subsystem (refer to section 8.3.3) sanitizes user
data in all Underlying Namespaces contained in that NVM subsystem, including any Underlying Namespace
that is associated with an Exported Namespace in any Exported NVM Subsystem (refer to section 5.3.7).


If an Exported NVM Subsystem contains an Exported Namespace that is associated with an Underlying
Namespace in an Underlying NVM Subsystem for which one of the following conditions exists:

  - a sanitize operation is in progress; or

  - the most recent sanitize operation has failed and successful recovery from the failed sanitize
operation has not occurred,


then, while that condition exists, that Exported NVM Subsystem shall enforce the I/O command sanitize
operation restrictions described in section 8.1.24.4 on I/O commands that specify that Exported Namespace
and may enforce additional sanitize operation restrictions described in that section.


**Submission Queue (SQ) Associations**


When Predictable Latency Mode is enabled, all I/O commands for namespaces in a given NVM Set have
the same quality of service attributes and shall exhibit predictable latencies as described in section 8.1.18.


The SQ Associations capability provides hints to the controller as to which specific I/O Queues are
associated with a given NVM Set. The controller uses this information to further enhance performance when
Predictable Latency Mode is enabled.


The SQ Associations capability is an optional capability. Predictable Latency Mode (refer to section 8.1.18)
is not dependent on the use of the SQ Associations capability.


If a controller supports SQ Associations, then the controller shall:

  - indicate support for the SQ Associations capability in the Controller Attributes (CTRATT) field in
the Identify Controller data structure;

  - indicate support for NVM Sets in the Controller Attributes (CTRATT) field in the Identify Controller
data structure; and

  - indicate support for Predictable Latency Mode in the Controller Attributes (CTRATT) field in the
Identify Controller data structure (refer to Figure 313).


577


NVM Express [®] Base Specification, Revision 2.2


The host enables the SQ Associations capability by creating an association between an NVM Set and a
Submission Queue at the time the Submission Queue is created (e.g., with a Create I/O Submission Queue
command (refer to section 5.2.2) or a Connect command (refer to section 6.3)).


For the SQ Associations capability to yield benefits, the host is required to:


a) create an association between each Submission Queue and some NVM Set; and
b) only issue I/O commands to Submission Queues that have an association with the NVM Set that

contains the namespace associated with the Namespace Identifier specified in that I/O command.


While this capability is enabled, failure to follow the specified operating rules may impact Predictable
Latency (refer to section 8.1.18).


**Standard Vendor Specific Command Format**


Controllers may support the standard Vendor Specific command format defined in Figure 82. Host storage
drivers may use the Number of Dwords fields to ensure that the application is not corrupting physical
memory (e.g., overflowing a data buffer). The controller indicates support of this format in the Identify
Controller data structure in Figure 313; refer to the Admin Vendor Specific Command Configuration field
and the I/O Command Set Vendor Specific Command Configuration field.


**Telemetry**


Telemetry enables manufacturers to collect internal data logs to improve the functionality and reliability of
products. The telemetry data collection may be initiated by the host or by the controller. The data is returned
in the Telemetry Host-Initiated log page or the Telemetry Controller-Initiated log page (refer to section
5.1.12.1.8 and 5.1.12.1.9). The data captured is vendor specific. The telemetry feature defines the
mechanism to collect the vendor specific data. The controller indicates support for the telemetry log pages
and for the Data Area 4 size in the Log Page Attributes (LPA) field in the Identify Controller data structure
(refer to Figure 313).


An important aspect to discovering issues by collecting telemetry data is the ability to qualify distinct issues
that are being collected. The ability to create a one to one mapping of issues to data collections is essential.
If a one to one mapping is not established, there is the risk that several payload collections appear distinct
but are actually all caused by the same issue. Conversely, a single payload collection may have payloads
caused by several issues mixed together creating additional complexity in determining the root cause. As
a result, flexibility in size is provided in the collection of telemetry payloads and a three phase process is
typically used.


The first phase establishes that an issue exists and is best accomplished by collecting a minimum set of
data to identify the issue as being distinct from other issues. Once the number of instances of an issue
establish an investigation, another phase may be necessary to collect actionable information. In the second
phase, a targeted collection of more in depth medium size payloads are gathered and analyzed to identify
the source of the problem.


If the small or medium sized telemetry data collection provides insufficient information, a third phase may
be employed to collect additional details. If the Data Area 4 Support (DA4S) bit is cleared to ‘0’ in the Log
Page Attributes field, then the third phase provides the largest and most complete payload to diagnose the
issue. If the DA4S bit is set to ‘1’ and the Extended Telemetry Data Area 4 Supported (ETDAS) field is set
to 1h in the Host Behavior Support feature (refer to section 5.1.25.1.14) then a fourth phase may be
employed to collect the largest and most complete payload to diagnose the issue. If Data Area 4 is created,
then Data Area 3 of non-zero length shall also be created and populated as part of data collection.


There are two telemetry data logs (i.e., Telemetry Host-Initiated log page and Telemetry Controller-Initiated
log page) defined. Each telemetry data log is made up of a single set of Telemetry Data Blocks. Each
Telemetry Data Block is 512 bytes in size. Telemetry data is returned (refer to section 5.1.12.1.8 and section
5.1.12.1.9) in units of Telemetry Data Blocks. Each telemetry data log is segmented into:


a) Three Telemetry Data Areas (i.e., small, medium, and large), if the DA4S bit is cleared to ‘0’; or


578


NVM Express [®] Base Specification, Revision 2.2


b) Four Telemetry Data Areas (i.e., small, medium, large and extra-large) If the DA4S bit is set to ‘1’

and the Extended Telemetry Data Area 4 Supported (ETDAS) field is set to 1h in the Host Behavior
Support feature (refer to section 5.1.25.1.14).


All telemetry data areas start at Telemetry Data Block 1.


Each Telemetry Data Area shall represent the controller’s internal state at the time the telemetry data was
captured.


Each Telemetry Data Area is intended to capture a richer set of data to aid in resolution of issues. Telemetry
Data Area 1 is intended to have a small size payload (i.e., the first phase), Telemetry Data Area 2 is intended
to have a medium size payload (i.e., the second phase), and Telemetry Data Area 3 is intended to have a
large size payload (i.e., the third phase). Telemetry Data Area 4 is intended to have an extra-large size
payload (i.e., the fourth phase). The size of each Telemetry Data Area is vendor specific and may change
on each data collection. When possible, the host should retrieve the payload for all supported Telemetry
Data Areas to enable the best diagnosis of the issue(s).


The preparation, collection, and submission of telemetry data is similar for host-initiated and controllerinitiated data; the primary difference is the trigger for the collection. The operational model for telemetry is:


1. The host identifies controller support for Telemetry log pages in the Identify Controller data

structure;
2. The host may indicate the support for the Telemetry Host-Initiated Data Area 4 and Telemetry

Controller-Initiated Data Area 4 by setting the Extended Telemetry Data Area 4 Supported (ETDAS)
field to 1h in the Host Behavior Support feature (refer to section 5.1.25.1.14);
3. The host prepares an area to store telemetry data if needed;
4. To receive notification that controller-initiated telemetry data is available, the host enables

Telemetry Log Notices using the Asynchronous Event Configuration feature (refer to section
5.1.25.1.5); and
5. If the host decides to collect host-initiated telemetry data or the controller signals that controller
initiated telemetry data is available:


a. The host reads the appropriate blocks of the Telemetry Data Area from the Telemetry Host
Initiated log page (refer to section 5.1.12.1.8) or the Telemetry Controller-Initiated log page
(refer to section 5.1.12.1.9). If possible, the host should collect Telemetry Data Area 1, 2, 3,
and 4. The host reads the log in 512 byte Telemetry Data Block units (i.e., a starting offset that
is a multiple of 512, and a length that is a multiple of 512). The host should set the Retain
Asynchronous Event bit to ‘1’;
b. The host re-reads the header of the log page and ensures that the Telemetry Host-Initiated

Data Generation Number field from the Telemetry Host-Initiated log page or the Telemetry
Controller-Initiated Data Generation Number field in the Telemetry Controller-Initiated log page
matches the original value read. If these values do not match, then the data captured is not
consistent and should be re-read from the log page with the Retain Asynchronous Event bit set
to ‘1’;
c. If the host is reading the controller-initiated log, then the host ensures that the Telemetry

Controller-Initiated Data Available field is still set to 1h after reading the appropriate blocks of
the Telemetry Data Area because the Telemetry Controller-Initiated Data Available field may
have been cleared to 0h by another entity while the log page was being read;
d. If the host is reading the Telemetry Controller-Initiated log page, then the host reads any portion

of that log page with the Retain Asynchronous Event bit cleared to ‘0’ to indicate to the controller
that the host has completed reading the Telemetry Controller-Initiated log page; and
e. When all telemetry data has been saved, the data should be forwarded to the manufacturer of

the controller.


The trigger for the collection for host-initiated data is typically a system crash, but may also be initiated
during normal operation. The host proceeds with a host-initiated data collection by submitting the Get Log
Page command for the Telemetry Host-Initiated log page with the Create Telemetry Host-Initiated Data bit


579


NVM Express [®] Base Specification, Revision 2.2


set to ‘1’ in the Log Specific Parameter field. The controller should complete the command quickly (e.g., in
less than one second) to avoid a user rebooting the system prior to completion of the data collection.


The NVM subsystem is allowed to provide a Telemetry Host-Initiated log page per controller or a shared
Telemetry Host-Initiated log page across all controllers in the NVM subsystem. If a shared Telemetry HostInitiated log page is implemented, the Telemetry Host-Initiated Data Generation Number field in the
Telemetry Host-Initiated log page is used to allow the host to detect that the Telemetry Host-Initiated log
page has been changed by:

  - a host through a different controller; or

  - a Management Controller through a Management Endpoint (refer to the NVM Express
Management Interface Specification).


The controller notifies the host to collect controller-initiated data through the completion of an Asynchronous
Event Request command with an Asynchronous Event Type of Notice that indicates a Telemetry Log
Changed event. The host may also determine controller-initiated data is available via the Telemetry
Controller-Initiated Data Available field in the Telemetry Host-Initiated or the Telemetry Controller-Initiated
log pages. The host proceeds with a controller-initiated data collection by submitting the Get Log Page
command for the Telemetry Controller-Initiated log page. Once the host has started reading the Telemetry
Controller-Initiated log page, the controller should avoid modifying the controller-initiated data until the host
has finished reading all controller-initiated data. The amount of time for the host to read the controllerinitiated data is vendor specific.


Since there is only one set of controller-initiated data, the controller is responsible for prioritizing the version
of the controller-initiated data that is available for the host to collect. When the controller replaces the
controller-initiated data with new controller-initiated data, the controller shall increment the Telemetry
Controller-Initiated Data Generation Number field. The host needs to ensure that the Telemetry ControllerInitiated Data Generation Number field has not changed between the start and completion of the controllerinitiated data collection to ensure the data captured is consistent.


**Telemetry Data Collection Examples (Informative)**


This section includes several examples of Telemetry Host-Initiated Data Areas for illustration. The same
concepts apply to the Telemetry Controller-Initiated Data Areas.


If a Telemetry Host-Initiated log page has no data for collection, then the following fields are all cleared to
0h:

  - Telemetry Host-Initiated Data Area 1 Last Block = 0;

  - Telemetry Host-Initiated Data Area 2 Last Block = 0; and

  - Telemetry Host-Initiated Data Area 3 Last Block = 0.


When all three telemetry data areas are populated, then the Telemetry Host-Initiated log page has different
values in each of the Telemetry Host-Initiated Data Area n Last Block fields. For example, the following
values correspond to the layout shown in Figure 657:

  - Telemetry Host-Initiated Data Area 1 Last Block = 65;

  - Telemetry Host-Initiated Data Area 2 Last Block = 1,000; and

  - Telemetry Host-Initiated Data Area 3 Last Block = 30,000.


As a result of telemetry data areas being made up of a single set of Telemetry Data Blocks starting at
Telemetry Data Block 1, the telemetry data contained in Telemetry Data Block 1 through Telemetry Data
Block 65 of data area 1, data area 2, and data area 3 is the same. In addition, the telemetry data contained
in Telemetry Data Block 66 through Telemetry Data Block 1,000 of data area 2 and data area 3 is the same.


580


NVM Express [®] Base Specification, Revision 2.2











|Figure 657: Telemetry Log Example – All Data Areas Populated|Col2|Col3|
|---|---|---|
|**Block Number**<br>**Telemetry Host-Initiated Data Areas**|**Block Number**<br>**Telemetry Host-Initiated Data Areas**|**Block Number**<br>**Telemetry Host-Initiated Data Areas**|
|1 <br> <br>65<br> <br>Data Area 1 *<br> <br> <br> <br> <br>1,000<br> <br> <br> <br> <br> <br> <br> <br>30,000<br>|<br>Data Area 2 *<br> <br>Data Area 2 +<br>continued<br>|<br>Data Area 3 *<br> <br>Data Area 3 +<br>continued<br> <br> <br>Data Area 3<br>continued|
|* Data Area 1, Data Area 2, and Data Area 3 contain the same telemetry data in blocks 1 through 65.<br>+ Data Area 2 and Data Area 3 contain the same telemetry data in blocks 66 through 1,000.|* Data Area 1, Data Area 2, and Data Area 3 contain the same telemetry data in blocks 1 through 65.<br>+ Data Area 2 and Data Area 3 contain the same telemetry data in blocks 66 through 1,000.|* Data Area 1, Data Area 2, and Data Area 3 contain the same telemetry data in blocks 1 through 65.<br>+ Data Area 2 and Data Area 3 contain the same telemetry data in blocks 66 through 1,000.|


When only the second data area is populated, then the Telemetry Host-Initiated log page has no data in
Telemetry Data Area 1 shown by having its corresponding last block value cleared to 0h, and no additional
data in Telemetry Data Area 3 shown by having its corresponding last block value set to the same value as
the last block value for Telemetry Data Area 2. For example, the following values correspond to the layout
shown in Figure 658:

  - Telemetry Host-Initiated Data Area 1 Last Block = 0;

  - Telemetry Host-Initiated Data Area 2 Last Block = 1,000; and

  - Telemetry Host-Initiated Data Area 3 Last Block = 1,000.


As a result of telemetry data areas being made up of a single set of Telemetry Data Blocks starting at
Telemetry Data Block 1, the telemetry data contained in Telemetry Data Block 1 through Telemetry Data
Block 1,000 of data area of data area 2 and data area 3 is the same.


581


NVM Express [®] Base Specification, Revision 2.2







|Figure 658: Telemetry Log Example – Data Area 2 Populated|Col2|Col3|
|---|---|---|
|**Block Number**<br>**Telemetry Host-Initiated Data Areas**|**Block Number**<br>**Telemetry Host-Initiated Data Areas**|**Block Number**<br>**Telemetry Host-Initiated Data Areas**|
|1 <br> <br> <br> <br> <br> <br> <br> <br> <br> <br> <br> <br> <br>1,000<br> <br>Data Area 1<br>_(empty)_|<br> <br> <br> <br> <br> <br> <br>Data Area 2 *|<br> <br> <br> <br> <br> <br> <br>Data Area 3 *|
|* Data Area 2, and Data Area 3 contain the same telemetry data in blocks 1 through 1,000.|* Data Area 2, and Data Area 3 contain the same telemetry data in blocks 1 through 1,000.|* Data Area 2, and Data Area 3 contain the same telemetry data in blocks 1 through 1,000.|


**Universally Unique Identifiers (UUIDs) for Vendor Specific Information**


**UUIDs for Vendor Specific Information Introduction**


Several commands send or receive information that contains fields described as Vendor Specific or that is
specified by a command field containing a value in a vendor specific range. Examples include the Set
Features command, which may specify a vendor specific feature identifier, and the Identify command, which
may retrieve a data structure having a vendor specific area.


The vendor specific information may have different definitions (e.g., a vendor specific log page identifier
with the contents of the page defined differently by different entities, such as an NVM subsystem vendor
and an NVM subsystem customer). By associating each definition of the information with a UUID specified
by the defining entity, a command is able to specify the particular definition of the information.


A command specifies a particular definition of the information by specifying an index into a list of UUIDs
supported by the controller (refer to section 5.1.13.2.14). The NVMe Invalid UUID (refer to section 8.1.28.2)
is used to replace a previously valid UUID in the UUID List (refer to Figure 321). This is done to keep the
values in the list at a static index, as that index is used by the Host to access the UUID List contents.


NVM subsystem vendors and customers communicate (by means outside the scope of this specification)
the UUID used for each definition of the information.


**UUIDs for Vendor Specific Information Requirements**


A UUID list is a list of non-zero UUID values, terminated by a 0h UUID value. Each non-zero UUID value
may be either a valid UUID or the NVMe Invalid UUID. The NVMe Invalid UUID is the hexadecimal value
FFFFFFFF_FFFFFFFF_7FFFFFFF_FFFFFFFFh. A valid UUID is any non-zero value other than the NVMe
Invalid UUID.


582


NVM Express [®] Base Specification, Revision 2.2


If a command supports selection of a UUID, then the UUID Selection Supported bit in the Commands
Supported and Effects data structure for that command (refer to Figure 211) shall be set to ‘1’. If a command
does not support selection of a UUID, then the UUID Selection Supported bit shall be cleared to ‘0’.


If the UUID Selection Supported bit is set to ‘1’ for one or more commands, then the UUID List bit in the
Controller Attributes field shall be set to ‘1’ (refer to Figure 313), and the controller shall support reporting
of a UUID List (refer to Figure 321).


If a command supports selection of a UUID, then that command contains a UUID Index field (refer to Figure
659).


**Figure 659: UUID Index Field**






|Bits|Description|
|---|---|
|6:0|**UUID Index (UIDX):** If this field is set to a non-zero value, then the value of this field is the index of a<br>UUID in the UUID List (refer to Figure 321) that is used by the command. If this field is cleared to 0h,<br>then no UUID index is specified.|



If the UUID Index field specifies a valid UUID (i.e., the UUID Index field is set to a non-zero value and the
UUID at that index indicates a valid UUID) (refer to section 5.1.13.2.14), then the controller shall process
the command using the vendor specific information specified by that UUID. If the UUID Index field is cleared
to 0h, then the command does not specify a UUID.


If no UUID is specified by the command, then the controller shall process the command, returning vendor
specific information.


The controller shall abort the command with a status code of Invalid Field in Command if:


a) The controller does not support the UUID specified by the UUID Index for the specified information;
b) The UUID specified by the UUID Index is cleared to 0h; or
c) The UUID specified by the UUID Index is the NVMe Invalid UUID.


If a firmware image is activated that has a UUID List in which an entry is different from that of the previouslyactive firmware image, then a host that is unaware of the change may issue a command with the UUID
index value for that entry. Such a command may produce unexpected results because the UUID specified
by that UUID Index has changed. To avoid this, vendors should follow the following revision guidelines for
UUID lists when constructing firmware images that support UUID selection:


a) Add UUIDs that are not supported in prior firmware image revisions to the end of the UUID List in

subsequent firmware image revisions;
b) Remove UUIDs that are supported in prior firmware image revisions by replacing the UUID with

the NVMe Invalid UUID in the same entry in the UUID list in subsequent firmware image revisions;
c) Do not replace the NVMe Invalid UUID with a valid UUID in the same UUID list entry in subsequent

firmware image revisions; and
d) Do not shorten or remove the UUID list in subsequent firmware image revisions.


In these guidelines, the terms “prior” and “subsequent” refer to a linear sequence of firmware versions (e.g.,
based on the date and time of the construction of the downloadable firmware image).


Following these guidelines prevents the host from inadvertently specifying the wrong UUID because there
is at most one valid UUID for each entry in the UUID list. Hence a command that specifies a UUID Index
either specifies the intended UUID or is aborted because that entry in the UUID list is empty or contains the
NVMe Invalid UUID.


The controller shall require a reset to activate a downloaded firmware image (refer to section 5.1.8) if the
downloaded image reports a UUID list with at least one slot in which a valid UUID replaces the NVMe
Invalid UUID or a different valid UUID in the existing image. All controllers that are affected by the UUID list
change caused by activation of a downloaded firmware image shall be reset as part of activating that
downloaded firmware image.


The above requirements for a reset to activate a downloaded firmware image do not require the controller
to directly compare the UUID lists in the current and downloaded firmware images. For example, a vendor


583


NVM Express [®] Base Specification, Revision 2.2


could use a vendor-specific major.minor firmware image revision numbering system (e.g., 3.5, 4.1) where
all downloadable firmware images with the same major revision number follow the above guidelines. In that
scenario, the controller is able to meet these reset requirements by requiring a reset if the downloaded
firmware image and the currently executing firmware have different major revision numbers.


**UUIDs for Vendor Specific Information Examples**


This section includes examples of the use of UUIDs to select vendor specific information.


**8.1.28.3.1 Vendor Specific Log Page Example**


If entity C and entity V create different definitions for a vendor specific log page having the same log page
identifier (e.g., D0h), then each assigns a UUID to distinguish their definition (e.g., entity V assigns UUID V
and entity C assigns UUID C).


A controller supporting both definitions of the log page:


a) Sets the UUID List bit to ‘1’ in the CTRATT field of the Identify Controller data structure (refer to

Figure 313);
b) Sets the UUID Selection Supported bit to ‘1’ in the Commands Supported and Effects data structure

(refer to Figure 211) corresponding to the Get Log Page command; and
c) Reports both UUID V and UUID C in the UUID list (refer to Figure 321).


A host requesting the log page defined by entity C:


1) Determines the index of UUID C in the UUID list;
2) Sets the Log Page Identifier field of the Get Log Page command to D0h; and
3) Sets the UUID Index field of the Get Log Page command to the index of UUID C.


A host requesting the log page defined by entity V:


1) Determines the index of UUID V in the UUID list;
2) Sets the Log Page Identifier field of the Get Log Page command to D0h; and
3) Sets the UUID Index field of the Get Log Page command to the index of UUID V.


A host not specifying the definition of the log page clears the UUID Index field to 0h. The selection of the
log page definition returned by the controller is vendor specific (e.g., the controller may select any definition
for the returned data).


**8.1.28.3.2 Vendor Specific Feature Example**


If entity C and entity V create different definitions for a vendor specific feature having the same Feature
Identifier (e.g., F1h), then each assigns a UUID to distinguish their definitions (e.g., entity V assigns UUID
V and entity C assigns UUID C).


A controller supporting both definitions of the feature for the Get Features command:


a) Sets the UUID List bit to ‘1’ in the CTRATT field of the Identify Controller data structure (refer to

Figure 313);
b) Sets the UUID Selection Supported bit to ‘1’ in the Commands Supported and Effects data structure

(refer to Figure 211) corresponding to the Get Features command;
c) Sets the UUID Selection Supported bit to ‘1’ in the FID Supported and Effects log page (refer to

Figure 263); and
d) Reports both UUID V and UUID C in the UUID list (refer to Figure 321).


A host retrieving the attributes of the feature defined by entity C:


1) Determines the index of UUID C in the UUID list;
2) Sets the Feature Identifier field of the Get Features command to F1h; and
3) Sets the UUID Index field of the Get Features command to the index of UUID C.


A host retrieving the attributes of the feature defined by entity V:


1) Determines the index of UUID V in the UUID list;


584


NVM Express [®] Base Specification, Revision 2.2


2) Sets the Feature Identifier field of the Get Features command to F1h; and
3) Sets the UUID Index field of the Get Features command to the index of UUID V.


**8.2** **Memory-Based Transport Extended Capabilities (PCIe)**


This section describes extended capabilities that are specific to the Memory-based transport model.


**Controller Memory Buffer**


The Controller Memory Buffer (CMB) is a region of general purpose read/write memory on the controller.
The controller indicates support for the CMB by setting CAP.CMBS to ‘1’. The host indicates intent to use
the CMB by setting CMBMSC.CRE to ‘1’. If this bit is set to ‘1’, the controller indicates the properties of the
CMB via the CMBLOC and CMBSZ properties (refer to section 3.1.4).


The CMB may be used for a variety of purposes. The controller indicates which purposes the memory may
be used for by setting support flags in the CMBSZ property.


The CMB’s PCI Express address range is used for external memory read and write requests to the CMB.
The PCI Express base address of the CMB is defined by the PCI Base Address Register (BAR) indicated
by CMBLOC.BIR, and the offset indicated by CMBLOC.OFST. The size of the CMB is indicated by
CMBSZ.SZ.


The controller uses the CMB’s controller address range to reference CMB with addresses supplied by the
host. The PCI Express address range and the controller address range of the CMB may differ, but both
ranges have the same size, and equivalent offsets within each range have a one-to-one correspondence.
The host configures the controller address range via the CMBMSC property.


The host enables the CMB’s controller memory space via the CMBMSC.CMSE bit. When controller memory
space is enabled, if the host supplies an address referencing the CMB’s controller address range, then the
controller directs memory read or write requests for this address to the CMB.


When the CMB’s controller memory space is disabled, the controller does not consider any host-supplied
address to reference the CMB’s controller address range, and memory read and write requests are directed
elsewhere (e.g., to memory other than the CMB).


To prevent possible misdirection of the controller’s memory requests, before host software enables the
CMB’s controller memory space, the host should configure the CMB’s controller address range so that the
addresses do not overlap any address that host software intends to use for DMA.


In versions prior to NVM Express Base Specification, Revision 1.4, for a controller that supports the CMB,
the CMB’s controller address range is fixed to be equal to its PCI Express address range, and the CMB’s
controller memory space is always enabled whenever the controller is enabled. To prevent misdirection of
controller memory requests when such a controller is assigned to a virtual machine, host software (on the
hypervisor or host OS) should not enable translation of the CMB’s PCI Express address range and should
ensure that this address range does not overlap any range of pre-translated addresses that the virtual
machine may use for DMA.


A host may configure the CMBMSC property so that CMB operates when the controller is assigned to a
virtual machine that only supports NVM Express Base Specification, Revision 1.3 and earlier. To prevent
that virtual machine from unintentionally clearing the CMBMSC property to 0h, the contents of the CMBSMC
property are preserved across Controller Reset and Function Level Reset (refer to the NVM Express NVMe
over PCIe Transport Specification).


Submission Queues in host memory require the controller to perform a PCI Express read from host memory
in order to fetch the submission queue entries. Submission Queues in controller memory enable host
software to directly write the entire submission queue entry to the controller's internal memory space,
avoiding one read from the controller to the host. This approach reduces latency in command execution
and improves efficiency in a PCI Express fabric topology that may include multiple switches. Similarly, PRP
Lists or SGLs require separate fetches across the PCI Express fabric, which may be avoided by writing the
PRP or SGL to the Controller Memory Buffer. Completion Queues in the Controller Memory Buffer may be
used for peer to peer or other applications. For writes of small amounts of data, it may be advantageous to


585


NVM Express [®] Base Specification, Revision 2.2


have the host write the data and/or metadata to the Controller Memory Buffer rather than have the controller
fetch it from host memory.


The contents of the Controller Memory Buffer are undefined as the result of:

  - the CMBMSC.CMSE bit transitioning from ‘0’ to ‘1’;

  - a Controller Reset; or

  - a Function Level Reset.


Host software should initialize any memory in the Controller Memory Buffer before being referenced (e.g.,
a Completion Queue shall be initialized by host software in order for the Phase Tag to be used correctly
(refer to section 4.2.4)).


A CMB implementation has a maximum sustained write throughput. The CMB implementation may also
have an optional write elasticity buffer used to buffer writes from CMB PCIe write requests. When the CMB
sustained write throughput is less than the PCI Express link throughput, then such a write elasticity buffer
allows PCIe write request burst throughput to exceed the CMB sustained write throughput without back
pressuring into the PCI Express fabric.


The time required to transfer data from the write elasticity buffer to the CMB is the amount of data written
to the elasticity buffer divided by the maximum CMB sustained write throughput (refer to section 3.1.4.19).
The time to transfer the entire contents of the write elasticity buffer is the size of the CMB elasticity buffer
(refer to section 3.1.4.18) divided by the maximum CMB sustained write throughput. The host is required
to account for any units differences in the CMB Elasticity Buffer Size Units field and the CMB Sustained
Write Throughput Units field.


A controller memory-based queue is used in the same manner as a host memory-based queue – the
difference is the memory address used is located within the controller’s own memory rather than in the host
memory. The Admin or I/O Queues may be placed in the Controller Memory Buffer. If the
CMBLOC.CQMMS bit (refer to Figure 47) is cleared to ‘0’, then for a particular queue, all memory
associated with it shall reside in either the Controller Memory Buffer or outside the Controller Memory
Buffer.


If the CMBLOC.CQPDS bit (refer to Figure 47) is cleared to ‘0’, then for all queues in the Controller Memory
Buffer, the queue shall be physically contiguous.


The controller may support PRP Lists and SGLs in the Controller Memory Buffer. If the CMBLOC.CDPMLS
bit (refer to Figure 47) is cleared to ‘0’, then for a particular PRP List or SGL associated with a single
command, all memory containing the PRP List or SGL shall be either entirely located in the Controller
Memory Buffer or entirely located outside the Controller Memory Buffer.


PRP Lists and SGLs associated with a command may be placed in the Controller Memory Buffer if that
command is present in a Submission Queue in the Controller Memory Buffer. If:


a) CMBLOC.CDPCILS bit (refer to Figure 47) is cleared to ‘0’; and
b) a command is not present in a Submission Queue in the Controller Memory Buffer,


then the PRP Lists and SGLs associated with that command shall not be placed in the Controller Memory
Buffer.


The controller may support data and metadata in the Controller Memory Buffer. If the CMBLOC.CDMMMS
bit (refer to Figure 47) is cleared to ‘0’, then all data and metadata, if any, associated with a particular
command shall be either entirely located in the Controller Memory Buffer or entirely located outside the
Controller Memory Buffer.


If the requirements for the Controller Memory Buffer use are violated by the host, the controller shall abort
the associated command with a status code of Invalid Use of Controller Memory Buffer.


The address region allocated for the CMB shall be 4 KiB aligned. It is recommended that a controller
allocate the CMB on an 8 KiB boundary. The controller shall support burst transactions up to the maximum
payload size, support byte enables, and arbitrary byte alignment. The host shall ensure that all writes to the
CMB that are needed for a command have been sent before updating the SQ Tail doorbell property. The


586


NVM Express [®] Base Specification, Revision 2.2


Memory Write Request to the SQ Tail doorbell property shall not have the Relaxed Ordering bit set to ‘1’
(refer to the PCI Express Base Specification), to ensure that prior writes to the CMB have completed.


**Doorbell Stride for Software Emulation**


The doorbell stride, specified in CAP.DSTRD (refer to Figure 36), may be used to separate doorbells by a
number of bytes in memory space. The doorbell stride is a number of bytes equal to (2 ^ (2 + CAP.DSTRD)).
This is useful in software emulation of an NVM Express controller. In this case, a software thread is
monitoring doorbell notifications. The software thread may be made more efficient by monitoring one
doorbell per discrete cacheline or utilize the monitor/mwait CPU instructions. For hardware implementations
of the NVM Express interface, the expected doorbell stride value is 0h.


**Host Memory Buffer**


The Host Memory Buffer (HMB) feature allows the controller to utilize an assigned portion of host memory
exclusively. The use of the host memory resources is vendor specific. Host software may not be able to
provide any or a limited amount of the host memory resources requested by the controller. The controller
shall function properly without host memory resources. Refer to section 5.1.25.2.4.


The controller may indicate limitations for the minimum usable descriptor entry size and the maximum
number of descriptor entries (refer to the HMMINDS and HMMAXD fields in the Identify Controller data
structure, Figure 313). If the host does not create the Host Memory Buffer within the indicated limits, then
the host memory allocated for use by the controller may not be fully utilized (e.g., descriptor entries beyond
the maximum number of entries indicated may be ignored by the controller).


During initialization, host software may provide a descriptor list that describes a set of host memory address
ranges for exclusive use by the controller. The host memory resources assigned are for the exclusive use
of the controller (host software should not modify the ranges) until host software requests that the controller
release the ranges and the controller completes the Set Features command. The controller is responsible
for initializing the host memory resources. Host software should request that the controller release the
assigned ranges prior to a shutdown event, a Runtime D3 event, or any other event that requires host
software to reclaim the assigned ranges. After the controller acknowledges that the ranges are no longer
in use, host software may reclaim the host memory resources. In the case of Runtime D3, host software
should provide the host memory resources to the controller again and inform the controller that the ranges
were in use prior to the RTD3 event and have not been modified.


The host memory resources are not persistent in the controller across a Controller Level Reset. Host
software should provide the previously allocated host memory resources to the controller after that reset
completes. If host software is providing previously allocated host memory resources (with the same
contents) to the controller, the Memory Return bit (refer to Figure 448) is set to ‘1’ in the Set Features
command.


The controller shall ensure that there is no data loss or data corruption in the event of a surprise removal
while the Host Memory Buffer feature is being utilized.


**Persistent Memory Region**


The Persistent Memory Region (PMR) is an optional region of general purpose PCI Express read/write
persistent memory that may be used for a variety of purposes. The controller indicates support for the PMR
by setting CAP.PMRS (refer to section 3.1.4.1) to ‘1’ and indicates whether the controller supports
command data and metadata transfers to or from the PMR by setting support flags in the PMRCAP property.
When command data and metadata transfers to or from PMR are supported, all data and metadata
associated with a particular command shall be either entirely located in the Persistent Memory Region or
outside the Persistent Memory Region.


The PMR’s PCI Express address range is used for external memory read and write requests to the PMR.
The PCI Express address range and size of the PMR is defined by the PCI Base Address Register (BAR)
indicated by PMRCAP.BIR. The PMR consumes the entire address region exposed by the BAR and
supports all the required features of the PCI Express programming model (i.e., it in no way restricts what is
otherwise permitted by PCI Express).


587


NVM Express [®] Base Specification, Revision 2.2


The controller uses the PMR’s controller address range to reference PMR with addresses supplied by the
host. The PCI Express address range and the controller address range of the PMR may differ, but both
ranges have the same size, and equivalent offsets within each range have a one-to-one correspondence.
The host configures the controller address range via the PMRMSCU and PMRMSCL properties.


The host enables the PMR’s controller memory space via the PMRMSCL.CMSE bit. When controller
memory space is enabled, if host supplies an address referencing the PMR’s controller address range, then
the controller directs memory read or write requests for this address to the PMR.


When the PMR’s controller memory space is disabled, the controller does not consider any host-supplied
address to reference the PMR’s controller address range, and memory read and write requests are directed
elsewhere (e.g., to memory other than the PMR).


The contents of data written to the PMR while the PMR is ready persists across power cycles, Controller
Level Resets, and disabling of the PMR. The mechanism used to make a write to the PMR persistent is
implementation specific. For example, in one implementation this may mean that a write to non-volatile
memory has completed while in another implementation this may mean that the write has been stored in a
non-volatile write buffer and is written to non-volatile memory at some later point.


A PMR implementation has a maximum sustained write throughput. The PMR implementation may also
have an optional write elasticity buffer used to buffer writes from PMR PCIe write requests. When the PMR
sustained write throughput is less than the PCI Express link throughput, then such a write elasticity buffer
allows PCIe write request burst throughput to exceed the PMR sustained write throughput without back
pressuring into the PCI Express fabric.


The time required to transfer data from the write elasticity buffer to non-volatile media is the amount of data
written to the elasticity buffer divided by the maximum PMR sustained write throughput (refer to section
3.1.4.26). The time to transfer the entire contents of the write elasticity buffer is the size of the PMR elasticity
buffer (refer to section 3.1.4.25) divided by the maximum PMR sustained write throughput. The host is
required to account for any units differences in the PMR Elasticity Buffer Size Units field and the PMR
Sustained Write Throughput Units field.


The host enables the PMR by setting PMRCTL.EN to ‘1’. Once enabled, the controller indicates that the
PMR is ready by clearing PMRSTS.NRDY to ‘0’. It is not necessary to enable the controller to enable the
PMR. Restoring and saving the contents of the PMR may take time to complete. When the host modifies
the value of PMRCTL.EN, the host should wait for at least the time interval specified in PMRCAP.PMRTO
for PMRSTS.NRDY to reflect the change.


When the PMR is not ready, PMR reads complete successfully and return an undefined value while PMR
writes complete normally, but do not update memory (i.e., the contents of the PMR address written remains
unchanged). The undefined value returned by a PMR read following a sanitize operation is such that
recovery of any previous user data from any cache or the non-volatile storage media is not possible.


When the PMR becomes read-only or unreliable, then a critical warning is reported in the SMART/Health
Information Log which may be used to trigger an NVMe interface asynchronous event. Since reporting of
an asynchronous event may occur an unspecified amount of time after the PMR health status has changed,
the host should assume that all operations to the PMR have been affected since the last time normal
operation was reported in PMRSTS.HSTS.


PMRCAP.PMRWBM enumerates supported PMR write barrier mechanisms. At least one mechanism shall
be supported. An implementation may optionally support a mechanism where a PCI Express read of any
size to the PMR, including a “zero-length read,” ensures that all previous memory writes (i.e., Posted PCI
Express requests) to the PMR have completed and are persistent. An implementation may optionally
support a write barrier mechanism that utilizes a read of the PMRSTS property. When supported, a read of
the PMRSTS property allows a host to:

  - ensure that previously issued memory writes to the PMR have completed; and

  - determine whether the PMR updates associated with those writes have completed without error
and are persistent.


588


NVM Express [®] Base Specification, Revision 2.2


A PMR memory write error may be the result of a poisoned PCI Express TLP, an NVM subsystem internal
error, or a PMR health status issue.


Regardless of the supported PMR write barrier mechanisms, a host may periodically read the PMRSTS
property to ensure that reads to the PMR have returned valid data. For example, if a read to the PMRSTS
property indicates that the PMR is operating normally is then followed by a series of reads, and finally a
second read to the PMRSTS property that indicates the PMR is unreliable, then one or more of the reads
between the two PMRSTS property reads may have returned invalid data. Such polling of the PMRSTS
property may be unnecessary if the host handles poisoned TLPs and/or poisoned TLP error reporting is
enabled.


The PMR write elasticity buffer size along with the PMR sustained write throughput allows a host to
determine the amount of time for a read associated with a Persistent Memory Region write barrier
mechanism to complete.


Support for PRPs, SGL Lists, Completion Queues, and Submission Queues in the Persistent Memory
Region is outside the scope of this specification. If the host attempts to use the Persistent Memory Region
for a PRP, SGL List, Completion Queue, or Submission Queue, the controller may abort the command with
a status code of Invalid Field in Command.


**Power Loss Signaling**


Power Loss Signaling (PLS) is a capability that the host uses to inform all controllers in a domain of
impending power loss, and that each controller uses to inform the host that the controller is preparing for
that power loss.


There are two modes of Power Loss Signaling processing, Forced Quiescence Processing (refer to section
8.2.5.2) and Emergency Power Fail Processing (refer to section 8.2.5.3). All controllers in a domain support
the same modes (i.e., all controllers report the same value in the PLSFQ bit and all controllers report the
same value in the PLSEPF bit; refer to Figure 313).


Not more than one Power Loss Signaling mode is active at any time. The host uses the Power Loss
Signaling Config feature (refer to section 5.1.25.1.19) to select the mode of operation or to disable Power
Loss Signaling. All controllers in a domain use the same mode (i.e., the scope of the Power Loss Signaling
Config feature is domain). The selection persists across power cycles as defined in Figure 386.


Each controller contains two variables which are used by Power Loss Signaling to perform communication
between the host and controller:

  - The Power Loss Notification (PLN) variable is set by the NVMe Transport and has two values,
Asserted and Deasserted.

  - The Power Loss Acknowledge (PLA) variable is set by the controller and has four values, AssertedFQ, Asserted-EPF-Enabled, Asserted-EPF-Disabled, and Deasserted.


The values of the variables are described in Figure 660.


**Figure 660: Power Loss Signaling Variables**





|Variable<br>Name|1<br>Reset|Description|
|---|---|---|
|PLN|Deasserted|**PLN Value:**The PLN variable values are defined as follows:<br>**Value**<br>**Definition**<br>Asserted<br>A power loss is impending.<br>Deasserted<br>A power loss is not impending.<br>|


|Value|Definition|
|---|---|
|Asserted|A power loss is impending.|
|Deasserted|A power loss is not impending.|


589


NVM Express [®] Base Specification, Revision 2.2


**Figure 660: Power Loss Signaling Variables**







|Variable<br>Name|1<br>Reset|Description|
|---|---|---|
|PLA|Deasserted|**PLA Value:**The PLA variable values are defined as follows:<br>**Value**<br>**Definition**<br>Asserted-FQ<br>The controller is performing Forced Quiescence Processing<br>(refer to section 8.2.5.2).<br>Asserted-EPF-Enabled<br>The controller is performing Emergency Power Fail<br>processing and the port is enabled (refer to section 8.2.5.3).<br>Asserted-EPF-Disabled<br>The controller is performing Emergency Power Fail<br>Processing and the port is disabled (refer to section 8.2.5.3).<br>Deasserted<br>The controller is not performing Power Loss Signaling<br>processing.|
|Note:<br>1.<br>Following a Controller Level Reset, the variable shall be set to this value.|Note:<br>1.<br>Following a Controller Level Reset, the variable shall be set to this value.|Note:<br>1.<br>Following a Controller Level Reset, the variable shall be set to this value.|


|Value|Definition|
|---|---|
|Asserted-FQ|The controller is performing Forced Quiescence Processing<br>(refer to section 8.2.5.2).|
|Asserted-EPF-Enabled|The controller is performing Emergency Power Fail<br>processing and the port is enabled (refer to section 8.2.5.3).|
|Asserted-EPF-Disabled|The controller is performing Emergency Power Fail<br>Processing and the port is disabled (refer to section 8.2.5.3).|
|Deasserted|The controller is not performing Power Loss Signaling<br>processing.|


Transport-specific details of the PLN variable and the PLA variable, including effects on communication
connectivity between host and controller, are described in the Power Loss Signaling Support section of the
appropriate NVMe Transport specification and in the Power Loss Signaling Interactions section of the NVM
Express Management Interface Specification.


If the controller supports Power Loss Signaling, then the controller:

  - shall support the PLN variable as specified in this section;

  - may support the PLA variable as specified in this section;

  - shall support Forced Quiescence Processing (refer to section 8.2.5.2), Emergency Power Fail
Processing (refer to section 8.2.5.3), or both;

  - if Forced Quiescence Processing is supported, shall report a non-zero value in the Forced
Quiescence Vault Time field in the Power State Descriptor of one or more of the supported power
states (refer to Figure 314);

  - if Emergency Power Fail Processing is supported, shall report non-zero values in the Emergency
Power Fail Vault Time field and the Emergency Power Fail Recovery Time field in the Power State
Descriptor of one or more of the supported power states (refer to Figure 314);

  - shall support reporting of whether I/O performance is degraded in the I/O Impacted (IOI) field (i.e.,
reports values 10b and 11b) in the I/O Command Set Independent Identify Namespace data
structure (refer to Figure 320); and

  - shall support the Power Loss Signaling Config feature (refer to section 5.1.25.1.19).


If the PLN variable is set to Asserted, then the controller performs either Forced Quiescence or Emergency
Power Fail Processing, as determined by the setting of the Power Loss Signaling Config feature.


The controller shall ignore transitions in the PLN variable if:


a) a Controller Level Reset (refer to section 3.7.2) is in process; or
b) if the CSTS.SHST field is not cleared to 00b (i.e., the controller is in the process of shutting down

or has completed shutdown).


If the PLN variable is set to Asserted and the controller is in a power state for which:


a) the Emergency Power Fail Vault Time field is cleared to 0h;
b) the Forced Quiescence Vault Time field is cleared to 0h; or
c) the Emergency Power Fail Recovery Time field is cleared to 0h,


then the time to perform an action for which the corresponding value is cleared to 0h is vendor specific.


If the controller is in the EPF Complete Port Enabled state, the EPF Complete Port Disabled state, or the
FQ Complete state and power is lost, then during the first restoration of power following the power loss,


590


NVM Express [®] Base Specification, Revision 2.2


processing of commands may be affected while the controller performs internal recovery operations.
Examples of these effects include:


a) a namespace not being ready (i.e., the NRDY bit is cleared to ‘0’ in the NSTAT field; refer to Figure

320); and
b) commands to a namespace being processed at reduced performance, as indicated by the IOI field

in the NSTAT field (refer to Figure 320).


**Power Loss Signaling Processing State Machine**


Figure 661 illustrates how transitions in the PLN variable initiate Power Loss Signaling processing by the
controller. Each circle represents a processing state.


**Figure 661: Power Loss Signaling Processing State Machine**



























Note 1: EPF is Enabled & PLN is Asserted & EPF Processing Port Enabled state is supported.
Note 2: EPF is Enabled & PLN is Asserted & EPF Processing Port Disabled state is supported.
Note 3: FQ is Enabled & PLN is Asserted.


For all states, a power cycle causes a transition to the PLS Not Ready state.


The Power Loss Signaling processing state of the controller determines the value of the PLA variable and
whether communications on the port are processed (refer to Figure 662).


591


NVM Express [®] Base Specification, Revision 2.2


**Figure 662: PLS States**











|State Name|PLA Variable Value<br>(if supported)|Port<br>Communication<br>Processed|
|---|---|---|
|PLS Not Ready|Deasserted|Yes|
|PLS Ready|Deasserted|Yes|
|FQ Processing|Asserted-FQ|Yes|
|FQ Complete|Deasserted|Yes|
|EPF Processing Port Disabled1|Asserted-EPF-Disabled|No|
|EPF Complete Port Disabled|Deasserted|No|
|EPF Processing Port Enabled1|Asserted-EPF-Enabled|Yes|
|EPF Complete Port Enabled|Deasserted|Yes|
|Notes:<br>1.<br>The controller shall not implement both the EPF Processing Port Disabled state and<br>the EPF Processing Port Enabled state.|Notes:<br>1.<br>The controller shall not implement both the EPF Processing Port Disabled state and<br>the EPF Processing Port Enabled state.|Notes:<br>1.<br>The controller shall not implement both the EPF Processing Port Disabled state and<br>the EPF Processing Port Enabled state.|


Note: I/O command processing in all of the PLS states, other than the PLS Not Ready state, complies with
atomic operation requirements for power fail, if any, as specified in the appropriate I/O Command Set
specification.


The conditions which trigger state transitions are described in the following sections. If a transition between
two states can be caused by any one of multiple conditions, then those conditions are shown in a bullet list
with an “or” (e.g., the transition from the FQ Processing state to the PLS Not Ready state, refer to Figure
665). If a transition is caused by multiple conditions which all must occur, then those conditions are shown
as a single-item bullet list with an “and” (e.g., any of the transitions from the PLS Ready state, refer to Figure
664).


**8.2.5.1.1** **PLS Not Ready State**


In the PLS Not Ready state, the controller is not performing Power Loss Signaling processing. The controller
enters the PLS Not Ready state following any Controller Level Reset or if the CSTS.SHST field is not
cleared to 00b (i.e., the controller is in the process of shutting down or has completed shutdown).


Transitions out of this state are defined in Figure 663.


**Figure 663: PLS Not Ready State Transition Conditions**

|State Transitions|Col2|Transition Condition|
|---|---|---|
|**Starting**|**Ending**|**Ending**|
|PLS Not Ready|PLS Ready|• <br>CSTS.SHST field is 00b.|



**8.2.5.1.2** **PLS Ready State**


In the PLS Ready state, the controller is not performing Power Loss Signaling processing and is not
performing shutdown processing. The controller enters the PLS Ready state when the CSTS.SHST field is
00b


Transitions out of this state are defined in Figure 664. If the controller is in this state and the CSTS.RDY bit
is cleared to ‘0’, then it is implementation specific whether the controller responds to a transition of the PLN
variable from Deasserted to Asserted.


**Figure 664: PLS Ready State Transition Conditions**

|State Transitions|Col2|Transition Condition|
|---|---|---|
|**Starting**|**Ending**|**Ending**|
|PLS Ready|FQ Processing|• <br>The controller is configured for FQ processing; and<br>• <br>the PLN variable transitions from Deasserted to Asserted.|



592


NVM Express [®] Base Specification, Revision 2.2


**Figure 664: PLS Ready State Transition Conditions**







|State Transitions|Col2|Transition Condition|
|---|---|---|
|**Starting**|**Ending**|**Ending**|
||EPF Processing<br>Port Disabled|• <br>The controller is configured for EPF processing;<br>• <br>the controller implements the EPF Processing Port Disabled state;<br>and<br>• <br>the PLN variable transitions from Deasserted to Asserted.|
||EPF Processing<br>Port Enabled|• <br>The controller is configured for EPF processing;<br>• <br>the controller implements the EPF Processing Port Enabled state;<br>and<br>• <br>the PLN variable transitions from Deasserted to Asserted.|
||PLS Not Ready|• <br>The controller processes a Controller Level Reset; or<br>• <br>CSTS.SHST is not cleared to 00b.|


**8.2.5.1.3** **FQ Processing State**


In the FQ Processing state, the controller is performing Forced Quiescence Processing, as described in
section 8.2.5.2.


Transitions out of this state are defined in Figure 665.


**Figure 665: FQ Processing State Transition Conditions**






|State Transitions|Col2|Transition Condition|
|---|---|---|
|**Starting**|**Ending**|**Ending**|
|FQ Processing|FQ Complete|• <br>The controller completes FQ processing.|
|FQ Processing|PLS Not Ready|• <br>The controller processes a Controller Level Reset; or<br>• <br>CSTS.SHST is not cleared to 00b.|



**8.2.5.1.4** **FQ Complete State**


In the FQ Complete state, the controller has completed Forced Quiescence Processing.


Transitions out of this state are defined in Figure 666.


**Figure 666: FQ Complete State Transition Conditions**

|State Transitions|Col2|Transition Condition|
|---|---|---|
|**Starting**|**Ending**|**Ending**|
|FQ Complete|PLS Not Ready|• <br>The controller processes a Controller Level Reset; or<br>• <br>CSTS.SHST is not cleared to 00b.|
|FQ Complete|PLS Ready|• <br>The PLN variable is set to Deasserted.|



**8.2.5.1.5** **EPF Processing Port Disabled State**


In the EPF Processing Port Disabled state, the controller is performing Emergency Power Fail Processing,
as described in section 8.2.5.3. The port is disabled. The following are not able to be initiated through the
port:


a) Controller Level Reset;
b) controller shutdown;
c) NVM Subsystem Reset; and
d) NVM Subsystem Shutdown.


Transitions out of this state are defined in Figure 667.


593


NVM Express [®] Base Specification, Revision 2.2


**Figure 667: EPF Processing Port Disabled State Transition Conditions**










|State Transitions|Col2|Transition Condition|
|---|---|---|
|**Starting**|**Ending**|**Ending**|
|EPF Processing<br>Port Disabled|EPF Complete<br>Port Disabled|• <br>The controller completes EPF processing.|



**8.2.5.1.6** **EPF Complete Port Disabled State**


In the EPF Complete Port Disabled state, the controller has completed Emergency Power Fail Processing.
The port is disabled. The following are not able to be initiated through the port:


a) Controller Level Reset;
b) controller shutdown;
c) NVM Subsystem Reset; and
d) NVM Subsystem Shutdown.


Transitions out of this state are defined in Figure 668.


**Figure 668: EPF Complete Port Disabled State Transition Conditions**

|State Transitions|Col2|Transition Condition|
|---|---|---|
|**Starting**|**Ending**|**Ending**|
|EPF Complete Port<br>Disabled|PLS Not Ready|• <br>Power is cycled.|



**8.2.5.1.7** **EPF Processing Port Enabled State**


In the EPF Processing Port Enabled state, the controller is performing Emergency Power Fail Processing,
as described in section 8.2.5.3. The port is enabled.


Transitions out of this state are defined in Figure 669.


**Figure 669: EPF Processing Port Enabled State Transition Conditions**






|State Transitions|Col2|Transition Condition|
|---|---|---|
|**Starting**|**Ending**|**Ending**|
|EPF Processing<br>Port Enabled|EPF Complete<br>Port Enabled|• <br>The controller completes EPF processing.|
|EPF Processing<br>Port Enabled|PLS Not Ready|• <br>The controller processes a Controller Level Reset; or<br>• <br>CSTS.SHST is not cleared to 00b.|



**8.2.5.1.8** **EPF Complete Port Enabled State**


In the EPF Complete Port Enabled state, the controller has completed Emergency Power Fail Processing.
The port is enabled.


Transitions out of this state are defined in Figure 670.


**Figure 670: EPF Complete Port Enabled State Transition Conditions**

|State Transitions|Col2|Transition Condition|
|---|---|---|
|**Starting**|**Ending**|**Ending**|
|EPF Complete Port<br>Enabled|PLS Not Ready|• <br>The controller processes a Controller Level Reset; or<br>• <br>CSTS.SHST is not cleared to 00b.|



**Forced Quiescence Processing**


This section describes the behavior of each controller in the domain when the domain is configured for
Power Loss Signaling with Forced Quiescence (refer to section 5.1.25.1.19).


594


NVM Express [®] Base Specification, Revision 2.2


If the controller enters the FQ Processing state, then the controller shall perform the following actions in
sequence:


1. set the PLA variable, if supported, to Asserted-FQ (refer to Figure 662);
2. stop fetching commands on all submission queues;
3. perform the following actions in parallel or in any sequence:


a) process commands received out-of-band on a Management Endpoint as described in the

Power Loss Signaling Interactions section of the NVM Express Management Interface
Specification;
b) if a command was fetched prior to entering this state, then process that command as described

in this section; and
c) prepare for power loss;


4. enter the FQ Complete state (refer to Figure 665); and
5. set the PLA variable to Deasserted (refer to Figure 662).


Entry to the FQ Processing state should cause the controller to complete processing of all previously
fetched commands (e.g., to post a CQE with a status code of Successful Completion, to abort the command
and post a CQE with an appropriate status code). If a background operation is in progress (e.g., a device
self-test operation or a sanitize operation), then that background operation should be suspended until the
PLN variable is set to Deasserted and fetching and processing commands resumes.


While in the FQ Processing state, the controller shall abort a previously-fetched Set Features command
specifying the Power Loss Signaling Config feature identifier with a status code of Commands Aborted due
to Power Loss Notification.


While in the FQ Processing state, if power is lost and subsequently restored, then resumption of command
processing:


a) may take more time than resumption of command processing after a normal shutdown completes

and then power is cycled; and
b) typically takes less time than resumption of command processing after an abrupt shutdown

completes and then power is cycled.


If the controller transitions from the FQ Processing state to the PLS Not Ready state, then the controller
shall abort Forced Quiescence Processing.


Forced Quiescence Processing shall not cause a loss of communication connectivity between the host and
the controller.


If the PLN variable is set to Asserted and is then set to Deasserted without an intervening loss of main
power, Controller Level Reset, or shutdown (refer to Figure 661), then the controller resumes fetching and
processing commands.


**Emergency Power Fail Processing**


This section describes the behavior of each controller in the domain when the domain is configured for
Power Loss Signaling with Emergency Power Fail (refer to section 5.1.25.1.19).


If the controller enters the EPF Processing Port Disabled state or the EPF Processing Port Enabled state
as described in Figure 664, then the controller shall perform the following actions in sequence:


1. set the PLA variable, if supported, to the value specified in Figure 662 for that state (i.e., Asserted
EPF-Disabled or Asserted-EPF-Enabled);
2. stop fetching commands on all submission queues;
3. perform the following actions in parallel or in any sequence:


a) process port communications as described in Figure 662; and
b) prepare for power loss in a manner that may or may not allow command processing to resume

quickly in the event of power loss and then power resumption;


595


NVM Express [®] Base Specification, Revision 2.2


4. enter either the EPF Complete Port Enabled state (refer to Figure 669) or the EPF Complete Port

Disabled state (refer to Figure 668); and
5. set the PLA variable, if supported, to Deasserted (refer to Figure 662).


Entry to the EPF Processing Port Disabled state or the EPF Processing Port Enabled state shall cause the
controller to discard commands that were fetched from a submission queue prior to entry to the state, and
to discard commands that were received out-of-band on a Management Endpoint prior to entry to the state.


The controller may implement the EPF Processing Port Disabled state or the EPF Processing Port Enabled
state. The controller shall not implement both states. All controllers in the domain shall implement the same
state.


The Emergency Power Fail Recovery Time (EPFRT) field and the Emergency Power Fail Recovery Time
Scale (EPFRTS) field (refer to Figure 314) indicate the time that the controller requires to complete recovery
during the first initialization following successful completion of Emergency Power Fail Processing. It is
implementation specific whether the controller begins recovery before or after the host sets the CC.EN bit
to ‘1’. Recovery may or may not be complete when the controller sets the CSTS.RDY bit to ‘1’.


If Emergency Power Fail Processing does not complete successfully (e.g., main power was lost before
completion of processing), then the recovery time may exceed the Emergency Power Fail Recovery Time.


**Virtualization Enhancements**


Virtualized environments may use an NVM subsystem with multiple controllers to provide virtual or physical
hosts direct I/O access. The NVM subsystem is composed of primary controller(s) and secondary
controller(s), where the secondary controller(s) depend on primary controller(s) for dynamically assigned
resources. A host may issue the Identify command to a primary controller specifying the Secondary
Controller List to discover the secondary controllers associated with that primary controller. All secondary
controllers shall be part of the same domain as the primary controller with which they are associated.


Controller resources may be assigned or removed from a controller using the Virtualization Management
command (refer to section 5.2.6) issued to a primary controller. The following types of controller resources
are defined:

  - Virtual Queue Resource (VQ Resource): a type of controller resource that manages one
Submission Queue (SQ) and one Completion Queue (CQ) (refer to section 8.2.6.1); and

  - Virtual Interrupt Resource (VI Resource): a type of controller resource that manages one interrupt
vector (refer to section 8.2.6.2).


Flexible Resources are controller resources that may be assigned to the primary controller or one of its
secondary controllers. The Virtualization Management command is used to provision the Flexible
Resources between a primary controller and one of its secondary controller(s). A primary controller’s
allocation of Flexible Resources may be modified using the Virtualization Management command and the
change takes effect after any Controller Level Reset other than a Controller Reset. A secondary controller
only supports having Flexible Resources assigned or removed when in the Offline state.


Private Resources are controller resources that are permanently assigned to a primary or secondary
controller. These resources are not supported by the Virtualization Management command.


The primary controller is allowed to have a mix of Private and Flexible Resources for a particular controller
resource type. If there is a mix, then the Private Resources occupy the lower contiguous range of resource
identifiers starting with 0. Secondary controllers shall have all Private or all Flexible Resources for a
particular resource type. Controller resources assigned to a secondary controller always occupy a
contiguous range of identifiers with no gaps, starting with 0. If a particular controller resource type is
supported as indicated in the Controller Resource Types field of the Primary Controller Capabilities
Structure, then all secondary controllers shall have that controller resource type assigned as a Flexible
Resource. Figure 671 shows the controller resource allocation model for a controller resource type that is
assignable as a Flexible Resource.


596


NVM Express [®] Base Specification, Revision 2.2


**Figure 671: Controller Resource Allocation**


For each controller resource type supported, the Primary Controller Capabilities Structure (refer to Figure
331) defines:

   - The total number of Flexible Resources;

   - The total number of Private Resources for the primary controller;

   - The maximum number of Flexible Resources that may be assigned to a secondary controller using
the Virtualization Management command; and

   - The assignment of resources to the primary controller.


Primary and secondary controllers may implement all features of this specification, except where
commands are defined as being only supported by a primary controller. It is recommended that only primary
controllers support the privileged actions described in section 3.10 so that untrusted hosts using secondary
controllers do not impact the entire NVM subsystem state.


The Secondary Controller List structure returned by the Identify command is used to determine the topology
of secondary controllers and the resources assigned. The secondary controller shall be in the Offline state
to configure resources. The Virtualization Management command is used to transition the secondary
controller between the Online state and the Offline state. Refer to section 8.2.6.3 for details on the Online
and Offline states.


To support the Virtualization Enhancements capability, the NVM subsystem shall support the following:

  - One or more primary controllers, each of which supports:


`o` One or more secondary controllers;

`o` A pool of unassigned Flexible Resources that supports allocation to a primary controller and
dynamic assignment to its associated secondary controllers;

`o` Two or more Private Resource queue pairs;


597


NVM Express [®] Base Specification, Revision 2.2


`o` Indicate support for the Virtualization Management command by setting the VMS bit to ‘1’ in
the Optional Admin Command Support (OACS) field in the Identify Controller data structure;

`o` The Virtualization Management command;

`o` The Primary Controller Capabilities Structure defined in Figure 331 (Identify command with
CNS value of 14h);

`o` The Secondary Controller List defined in Figure 331 (Identify command with CNS value of 15h);
and

`o` The Namespace Management capability (refer to section 8.1.15);

  - One or more secondary controllers; and

  - Flexible Resources, each of which supports all of the following:


`o` Assignment and removal by exactly one primary controller; and

`o` Assignment to no more than one controller at a time.


Within an NVM subsystem that supports both the Virtualization Enhancements capability and SR-IOV (refer
to section 8.2.6.4), all controllers that are SR-IOV PFs shall be primary controllers, and all controllers that
are SR-IOV VFs shall be secondary controllers of their associated PFs.


**VQ Resource Definition**


A Virtual Queue Resource (VQ Resource) is a type of controller resource that manages one CQ and one
SQ. For a VQ Resource that is assigned to a controller, its resource identifier is equivalent to its Queue
Identifier.


The Controller Resource Types field of the Primary Controller Capabilities Structure indicates whether VQ
Resources are supported. If VQ Resources are unsupported, a primary controller and its associated
secondary controllers have all queues as Private Resources. The rest of this section assumes that VQ
Resources are supported.


The secondary controller is assigned VQ Resources using the Virtualization Management command. The
number of VQ Resources assigned is discoverable in the Secondary Controller List entry for the associated
secondary controller. The number of VQ Resources assigned may also be discovered using the Get
Features command with the Number of Queues Feature identifier (refer to section 5.1.25.2.1).


If a secondary controller has no assigned VQ Resources, then that controller remains in the Offline state.
A secondary controller is not able to transition to the Online state until VQ Resources for an Admin Queue
and one or more I/O Queues have been assigned to that controller (i.e., the minimum number of VQ
Resources that may be assigned is two).


A primary controller that supports VQ Resources shall have at least two queue pairs that are Private
Resources to ensure there is a minimum of an Admin Queue pair and one I/O queue pair for the primary
controller at all times. A primary controller may be allocated VQ Resources using the Primary Controller
Flexible Allocation action of the Virtualization Management command. The VQ resources allocated take
effect after a Controller Level Reset and are persistent across power cycles and resets. The number of VQ
Resources currently allocated is discoverable in the Primary Controller Capabilities Structure. The number
of VQ Resources currently allocated may also be discovered using the Get Features command with the
Number of Queues Feature identifier (refer to section 5.1.25.2.1).


**VI Resource Definition**


A Virtual Interrupt Resource (VI Resource) is a type of controller resource that manages one interrupt
vector, such as an MSI-X vector. For a VI Resource that is assigned to a controller, its resource identifier
is equivalent to its interrupt vector number.


The Controller Resource Types field of the Primary Controller Capabilities Structure indicates whether VI
Resources are supported. If VI Resources are unsupported, a primary controller and its associated
secondary controllers have all interrupts as Private Resources. The rest of this section assumes that VI
Resources are supported.


598


NVM Express [®] Base Specification, Revision 2.2


The secondary controller is assigned VI Resources using the Virtualization Management command. The
number of VI Resources assigned is discoverable in the Secondary Controller List entry for the associated
secondary controller.


While a primary controller and/or its associated secondary controllers may concurrently support multiple
types of interrupt vectors (e.g., MSI and MSI-X), all the controllers’ VI Resources shall contain interrupt
resources for interrupt vectors of the same type. In this revision, MSI-X is the only supported type of VI
Resource.


For a secondary controller that supports VI Resources with MSI-X vectors, if at least one VI Resource is
assigned to that controller, MSIXCAP.MXC.TS (refer to the MSI-X Capability section of the NVMe over
PCIe Transport Specification) indicates the number of VI Resources assigned to the controller. Since
MSIXCAP.MXC.TS is read-only, the value shall only be updated when the secondary controller is in the
Offline state. MSI-X Table Entries on the secondary controller for newly assigned VI Resources shall be
reset to default values.


If a secondary controller that supports VI Resources has no assigned VI Resources, then that controller
remains in the Offline state. A secondary controller is not able to transition to the Online state until a VI
Resource for interrupt vector 0 has been assigned to that controller. For a secondary controller that supports
VI Resources with MSI-X vectors, if no VI Resources are assigned to that controller, then
MSIXCAP.MXC.TS is reserved.


A primary controller that supports VI Resources shall have at least one interrupt that is a Private Resource.
Interrupt vector 0 is always assigned to the primary controller. A primary controller may be allocated VI
Resources using the Primary Controller Flexible Allocation action of the Virtualization Management
command. The VI resources allocated take effect after a Controller Level Reset and are persistent across
power cycles and resets. The number of VI Resources currently allocated is discoverable in the Primary
Controller Capabilities Structure. For a primary controller that supports VI Resources with MSI-X vectors,
MSIXCAP.MXC.TS indicates an MSI-X Table size equal to the total number of Private Resources and the
Flexible Resources currently allocated following a Controller Level Reset.


When an I/O CQ is created, the controller supports mapping that I/O CQ to any valid interrupt vector,
regardless of whether they have the same resource identifier, as long as the I/O CQ and the interrupt vector
are attached to the same controller.


**Secondary Controller States and Resource Configuration**


A secondary controller shall be in one of the following states:

  - **Online:** The secondary controller may be in use by a host. Required resources have been
assigned. The secondary controller may be enabled in this state (CC.EN may be set to ‘1’ and
CSTS.RDY may then transition to ‘1’); or

  - **Offline:** The secondary controller may not be used by a host. CSTS.CFS shall be set to ‘1’.
Controller properties other than CSTS are undefined in this state.


The host may request a transition to the Online or Offline state using the Virtualization Management
command. When a secondary controller transitions from the Online state to the Offline state all Flexible
Resources are removed from the secondary controller.


To ensure that the host accurately detects capabilities of the secondary controller, the host should complete
the following procedure to bring a secondary controller Online:


1. Use the Virtualization Management command to set the secondary controller to the Offline state;
2. Use the Virtualization Management command to assign VQ resources and VI resources;
3. Perform a Controller Level Reset. If the secondary controller is a VF, then this should be a VF

Function Level Reset (refer to the NVM Express NVMe over PCIe Transport Specification); and
4. Use the Virtualization Management command to set the secondary controller to the Online state.


If VI Resources are supported, then following this process ensures the MSI-X Table size indicated by
MSIXCAP.MXC.TS is updated to reflect the appropriate number of VI Resources before the transition to
the Online state.


599


NVM Express [®] Base Specification, Revision 2.2


A primary controller or secondary controller is enabled when CC.EN and CSTS.RDY are both set to ‘1’ for
that controller. A secondary controller is able to be enabled only when in the Online state. If the primary
controller associated with a secondary controller is disabled or undergoes a Controller Level Reset, then
the secondary controller shall implicitly transition to the Offline state. A secondary controller shall transition
to the Offline state when a shutdown occurs (refer to section 3.6, section 3.1.4.5, and section 3.1.4.20) on
the primary controller associated with that secondary controller.


Resources shall only be assigned to a secondary controller when in the Offline state. If the minimum number
of resources are not assigned to a secondary controller, then a request to transition to the Online state shall
fail for that secondary controller. For implementations that support SR-IOV, if VF Enable is cleared to ‘0’ or
NumVFs specifies a value that does not enable the associated secondary controller, then the secondary
controller shall implicitly transition to the Offline state.


**Single Root I/O Virtualization and Sharing (SR-IOV)**


The PCI-SIG [®] PCI Express Base specification defines Single Root I/O Virtualization and Sharing
Specification (SR-IOV) extensions to PCI Express that allow multiple System Images (SIs), such as virtual
machines running on a hypervisor, to share PCI hardware resources. The primary benefit of SR-IOV is that
it eliminates the hypervisor from participating in I/O operations which may be a significant factor limiting
storage performance in some virtualized environments and allows direct SI access to PCI hardware
resources.


A Physical Function (PF) is a PCI Express Function that supports the SR-IOV Capability, which in turn
allows that PF to support one or more dependent Virtual Functions (VFs). These PFs and VFs may support
NVM Express controllers that share an underlying NVM subsystem with multi-path I/O and namespace
sharing capabilities (refer to section 2.4.1).


SR-IOV Virtual Functions (VFs) with an NVM Express Class Code (refer to the PCI Header section of the
NVMe over PCIe Transport Specification) shall implement fully compliant NVM Express controllers. This
ensures that the same host software developed for non-virtualized environments is capable of running
unmodified within an SI.


For hosts where SR-IOV is unsupported or not needed, a controller that is a PF shall support operation as
a stand-alone controller.


For a controller that is a PF, the requirements for SR-IOV Capability registers VF BAR0, VF BAR1, VF
BAR2, VF BAR4, and VF BAR5 are the same as the requirements for PCI registers BAR0, BAR1, BAR4,
and BAR5, respectively. For a controller that is a PF, SR-IOV Capability register VF BAR2 shall not support
Index/Data Pair. Refer to the PCI Header section of the NVMe over PCIe Transport Specification.


To accommodate SR-IOV address range isolation requirements, VF BAR2 and VF BAR3 may support a
64-bit prefetchable memory register space which shall only be used for MSI-X Tables and MSI-X PBAs of
VFs. MSI-X Table BIR = ‘2’ and MSI-X PBA BIR = ‘2’ are valid for controllers that are VFs. Refer to the
MSI-X Capability section of the NVMe over PCIe Transport Specification.


While the controller properties of a controller that is a VF are accessible only if SR-IOV Control.VF MSE is
set to ‘1’, clearing VF MSE from ‘1’ to ‘0’ does not cause a reset of that controller. In this case, controller
properties are hidden, but their values are not reset.


**8.3** **Message-Based Transport Extended Capabilities (Fabrics)**


This section describes extended capabilities that are specific to the Message-based transport model.


**Automated Discovery of NVMe-oF Discovery Controllers for IP Based Fabrics**


When operating in an IP based fabric, before transmitting a Fabrics Connect command, the IP address of
the fabric interface of the Discovery controller is determined by one of the following methods:


a) administrative configuration;
b) discovered using DNS-SD (refer to RFC 6763); or
c) obtained by some means not defined in this specification.


600


NVM Express [®] Base Specification, Revision 2.2


DNS-SD information may be retrieved using mDNS (refer to RFC 6762) or from a DNS server (refer to RFC
1034 and RFC 1035).


When DNS-SD is used as described in this section, hosts, CDCs and DDCs may use DNS-SD to perform
automated discovery of Discovery controllers in IP fabrics consisting of:


a) Two IP interfaces (i.e., a host and an NVM subsystem) physically connected to one another (refer

to Figure 672);
b) Many IP interfaces participating in one or more Broadcast Domains (refer to Figure 673); or
c) A Centralized Discovery controller and many IP interfaces that may reside in multiple Broadcast

Domains (refer to Figure 674).


mDNS is a multicast protocol that allows discovery of IP interfaces within the same Broadcast Domain.
Discovering IP interfaces outside of the Broadcast Domain using mDNS requires either the use of RFC
8766 or an mDNS NVMe-oF proxy. An mDNS NVMe-oF proxy is an mDNS responder that is responsive to
queries for either the “_nvme-disc” service or the “_cdc._sub._nvme-disc” service and responds with the
information defined in section 8.3.1.1.2.


**Figure 672: Configuration A - Two IP Interfaces**











**Figure 673: Configuration B – Multiple IP Interfaces without a CDC**















**Figure 674: Configuration C – Multiple IP interfaces with a CDC**















**Discovery of NVMe-oF Discovery Controllers**


**8.3.1.1.1** **Query**


To facilitate the discovery of Discovery controller IP fabric interface addresses, hosts, CDCs and DDCs
may transmit an mDNS query (refer to RFC 6762) or a DNS query (refer to RFC 1034 and RFC 1035) that
includes a DNS PTR record (refer to RFC 6763) with the name in the form of:


“<Service>.<Domain>”.


The <Service> portion of the name can be further broken down into:


601


NVM Express [®] Base Specification, Revision 2.2


“<service name>.<protocol>”.


For NVMe over Fabrics, the DNS PTR record included in the mDNS or DNS query shall be in the form of:


“_nvme-disc.<protocol>.<domain>”; or


“_<subtype>._sub._nvme-disc.<protocol>.<domain>”.


The protocol field shall be set as shown in Figure 675.


The subtype field shall be set as shown in Figure 676.


The domain field shall be set as shown in Figure 677.


**Figure 675: mDNS Protocol Field**

|NVMe-oF Transport|Fabric Protocol|mDNS <protocol> Field|
|---|---|---|
|TCP|TCP|“_tcp”|
|RDMA|RoCE|“_udp”|
|RDMA|iWARP|“_tcp”|



**Figure 676: mDNS Subtype**

|Subtype|Usage|
|---|---|
|“_cdc”|Used by CDC and DDC instances to detect the presence of a CDC service.|
|“_ddcpull”|Obsolete.|



**Figure 677: mDNS Domain**

|Domain|Usage|
|---|---|
|“local”|Used for mDNS|
|<FQDN>|A fully qualified domain name may be used when DNS-SD information is retrieved from a DNS<br>server.|



**8.3.1.1.2** **Response**


The responses that may be received for an mDNS or DNS query include the following records as described
in DNS-Based Service Discovery (refer to RFC 6763):

  - A DNS PTR record (refer to section 3.3.12 in RFC 1035);

  - a DNS SRV record (refer to RFC 2782);

  - a DNS TXT record (refer to section 3.3.14 in RFC 1035); and

  - an A record and/or AAAA record providing the IPv4 and IPv6 IP addresses respectively.


**DNS PTR record**


The DNS PTR record included in the mDNS or DNS response shall be in the form of:


“<Service>.<Domain>”.


The <Service> portion of the name can be further broken down into:


“<service name>.<protocol>”.


For NVMe over Fabrics, the DNS PTR record included in the mDNS or DNS response shall be in the form
of:


“_nvme-disc.<protocol>.<domain>”; or


“_<subtype>._sub._nvme-disc.<protocol>.<domain>”


The protocol field shall be set as shown in Figure 675.


The subtype field shall be set as shown in Figure 676.


602


NVM Express [®] Base Specification, Revision 2.2


The domain field shall be set as shown in Figure 677.


**DNS SRV record**


The DNS SRV record provides the TCP port where the service instance can be reached and shall have a
name in the form of:


“<Instance>.<Service>.<Domain>”.


Instance (Instance name) is a vendor defined human readable string. Although use of a serial number is
discouraged in DNS-Based Service Discovery (refer to RFC 6763), an instance name that may be
meaningful to an IT administrator is a combination of the Model Number (MN), Serial Number (SN) and
Physical Fabric Interface (Physical Ports). For example:


“SubsystemIF-SerialNumber-SubsystemModel”.


The maximum length of the Instance Name field is 63 bytes (refer to RFC 6763).


The <Service> portion of the name (refer to section 4.1 of RFC 6763) can be further broken down into:


“<service name>.<protocol>”.


**DNS TXT record**


The DNS TXT record provides additional information about the instance using key/value pairs in the form
of “key=value” separated by commas (refer to section 6.4 in RFC 6763).


For NVMe over Fabrics, the DNS TXT record shall include a key/value pair for protocol (p) and may include
a key/value pair describing an NQN.


DNS TXT record key/value pairs:


**Protocol (p)** : the protocol field shall indicate the IP transport protocols that are supported by the
Discovery controller being advertised. For example:


“p=tcp”, “p=roce”, or “p=iwarp”.


**NQN:** the DNS TXT record may contain an nqn key/value pair. When it is included the NQN
provided shall be set to the unique NQN of the Discovery subsystem if one is available for use.
Otherwise, the well-known Discovery Service NQN (nqn.2014-08.org.nvmexpress.discovery) may
be used.


As described in RFC 6763, the format of the data within a DNS TXT record is one or more strings, packed
together without any intervening gaps or padding bytes for word alignment.


The format of a TXT record that may be provided in a response is:


“<length byte>p=tcp<length byte>nqn=NQN.of.Discovery.subsystem”.


Using this format, an example of a TXT record that may be provided in a response is:


“05p=tcp1Enqn=NQN.of.Discovery.subsystem”.


**Host Operation**


**8.3.1.2.1** **Host Query**


As described in section 8.3.1.1.1, a host may transmit an mDNS or DNS query to discover CDC and DDC
instances that are present on the transport network. When used, the mDNS or DNS query shall include a
DNS PTR record (refer to RFC 6763) with the name in the form of:


“_nvme-disc.<protocol>.<domain>”.


The protocol field shall be set as shown in Figure 675.


The domain field shall be set as shown in Figure 677.


603


NVM Express [®] Base Specification, Revision 2.2


**8.3.1.2.2** **Host Processing of DNS-SD Records**


Upon reception of an mDNS or DNS response that contains a DNS SRV record with the service name set
to “_nvme-disc.<protocol>.local”. The host interface may use the IP address in the A or AAAA record as
the destination IP address for a subsequent Fabrics Connect command and attempt to perform Discovery
Information Registration (refer to section 8.3.2.2).


**DDC Operation**


**8.3.1.3.1** **DDC mDNS Initialization**


During initialization (e.g., following a link transition or power cycle), before the DDC’s mDNS responder
function is enabled, the DDC shall probe to ensure the unique resource records the DDC are responsible
for are unique on the local link (refer to section 8.1 in RFC 6762).


Upon successful completion of the probe, the DDC shall Announce (refer to section 8.2 in RFC 6762) its
newly registered resource records.


Upon announcing its resource records, if a DDC:


a. has not been configured to perform push registration (refer to section 8.3.2.2.1), or has not been

configured to request a pull registration (refer to section 8.3.2.2.2) from a CDC, it may respond to
mDNS queries for the service name of “_nvme-disc.<protocol>.local”; or
b. has been configured to perform push registration (refer to section 8.3.2.2.1) with a CDC, it should

not respond to mDNS queries for the service name of “_nvme-disc.<protocol>.local”, unless it has
been administratively configured to do so or until it has performed a query and determined a CDC
is not present as defined in section 8.3.1.3.3.


**8.3.1.3.2** **DDC DNS Initialization**


During initialization (e.g., following a link transition or power cycle), a DDC may dynamically update DNS
records (refer to RFC 2136) by providing an update that includes the Resource Records defined in section
8.3.1.1.2.


**8.3.1.3.3** **DDC Query**


A DDC may determine if a CDC is present by transmitting a query that includes a DNS PTR record (refer
to RFC 6763) with the name in the form of:


“_cdc._sub._nvme-disc.<protocol>.<domain>”.


The protocol field shall be set as shown in Figure 675.


The domain field shall be set as shown in Figure 677.


**8.3.1.3.4** **DDC Processing of DNS-SD records**


Upon reception of an mDNS or DNS response that contains a DNS SRV record with the service name set
to “_cdc._sub._nvme-disc”, the DDC may use the IP address in the A or AAAA record as the destination IP
address to either:


a. Perform push registration (refer to section 8.3.2.2.1) with the CDC; or
b. Request a pull registration (refer to section 8.3.2.2.2) from the CDC (e.g., using Kickstart Discovery

Request PDU (KDReq) section in the NVMe Transport Specification).


If a DDC supports mDNS and has been configured to perform push registration (refer to section 8.3.2.2.1),
or has been configured to request a pull registration (refer to section 8.3.2.2.2) from a CDC, the DDC should
cease responding to mDNS requests for the service name of “_nvme-disc.<protocol>.local” if a CDC is
detected as defined in section 8.3.1.3.3.


604


NVM Express [®] Base Specification, Revision 2.2


**8.3.1.3.5** **DDC response to mDNS queries**


A DDC may respond to mDNS queries for the service names of:


“_nvme-disc.<protocol>.local”


mDNS responses to queries for these service names shall contain the information described in section
8.3.1.1.2.


DDCs should ignore mDNS queries for the service name of “_ddcpull._sub._nvme-disc.<protocol>.local”
(refer to Figure 676), as the subtype “_ddcpull._sub” is obsolete.


**CDC Operation**


**8.3.1.4.1** **CDC mDNS Initialization**


During initialization (e.g., following a link transition or power cycle), before the CDC’s mDNS responder
function is enabled, the CDC shall probe to ensure the unique resource records the CDC are responsible
for are unique on the local link (refer to section 8.1 in RFC 6762).


Upon successful completion of the probe, the CDC shall announce (refer to section 8.2 in RFC 6762) its
newly registered resource records.


Upon announcing its resource records, the CDC’s mDNS responder function may be enabled and respond
to queries for the service name of “_cdc._sub._nvme-disc._<protocol>.local” as described in section
8.3.1.4.5.


A CDC should query for the presence of another CDC as defined in section 8.3.1.4.3 and process
responses as defined in section 8.3.1.4.4.


**8.3.1.4.2** **CDC DNS Initialization**


During initialization (e.g., following a link transition or power cycle), a CDC may dynamically update DNS
records (refer to RFC 2136) by providing an update that includes the Resource Records defined in section
8.3.1.1.2.


**8.3.1.4.3** **CDC Query**


A CDC may query for other CDC instances. When performed the mDNS or DNS query shall include a DNS
PTR record (refer to RFC 6763) with the name in the form of:


“_cdc._sub._nvme-disc.<protocol>.<domain.


The protocol field shall be set as shown in Figure 675.


The domain field shall be set as shown in Figure 677.


**8.3.1.4.4** **CDC Processing of DNS-SD records**


Upon reception of an mDNS or DNS response that contains a DNS SRV record with the service name set
to “_cdc._sub._nvme-disc.<protocol>.local” the CDC may provide an alert to the administrator to indicate
the presence of more than one CDC in a broadcast domain.


A CDC should ignore an mDNS or DNS response that contains a DNS SRV record with the service name
set to “_ddcpull._sub._nvme-disc.<protocol>.local”.


**8.3.1.4.5** **CDC response to mDNS queries**


A CDC may respond to mDNS queries for the service names of either:


“_nvme-disc.<protocol>.local”; or


“_cdc_sub._nvme-disc.<protocol>.local”.


mDNS responses to this query shall contain the information described in section 8.3.1.1.2.


605


NVM Express [®] Base Specification, Revision 2.2


**Centralized Discovery for IP-based Fabrics**


**Overview**


In configurations that consist of multiple NVM subsystems, the burden on administrators is reduced by
enabling hosts to automatically retrieve the list of NVM subsystem ports the host has been allowed to
access from a centralized location. This centralized location is referred to as a Centralized Discovery
controller (CDC).


Hosts and NVM subsystems may become known to the CDC by explicitly registering their discovery
information as the result of a push registration (refer to section 8.3.2.2.1). If a host or Direct Discovery
controller (DDC) detects the presence of multiple CDCs, then that host or DDC should register their
discovery information with each CDC. Alternatively, the CDC may implicitly register discovery information
as a result of processing a Connect command from a host, or as a result of receiving a pull registration
request from a DDC (refer to section 8.3.2.2.2).


The CDC may filter the list of NVM subsystem ports returned in response to a Get Log Page command
from the host that requests the Discovery log page to include only the NVM subsystem ports that provide
access to namespaces allocated to that host. The process used to configure this filtering function is known
as Fabric Zoning (refer to section 8.3.2.3.


An overview of the registration and discovery process is described in section 8.3.2.1.1.


**8.3.2.1.1** **Registration and Discovery Example**


The following example assumes the CDC’s effective Fabric Zoning configuration allows Host A to access
both NVM subsystem A and NVM subsystem B.


**Figure 678: Registration and Discovery Example**


606


NVM Express [®] Base Specification, Revision 2.2


Each of the numbered steps in Figure 678 are described below:


1. A fabric interface on NVM subsystem A is registered with the CDC. This is accomplished by either:


a. using the Discovery Information Management command (refer to section 5.3.3) to perform a

push registration (refer to section 8.3.2.2.1);
b. notifying the CDC that a pull registration (refer to section 8.3.2.2.2) is required and the NVM

subsystem port must be implicitly registered by the CDC; or
c. administrative configuration (e.g., the NVM subsystem port was manually configured on the

CDC).


2. Host A should establish an explicit persistent connection with the CDC. The method that a host

uses to obtain the information necessary to connect to the CDC via the NVMe Transport may be:


a. implementation specific;
b. fabric specific;
c. known in advance (e.g., a well-known address);
d. administratively configured; or
e. for IP based fabrics, Automated Discovery of Discovery Controllers for IP Based Fabrics (refer

to section 8.3.1) may be used.


3. Host A uses the Discovery Information Management command to perform a push registration and

explicitly register its discovery information with the CDC.
4. Host A should send one or more Asynchronous Event Request commands to the CDC in order to

be notified about any changes that occur to the Discovery log page.
5. Host A uses the Get Log Page command to retrieve the Discovery log page from the CDC.
6. The CDC responds to the Get Log Page command with a Discovery log page containing one

Discovery Log Page Entry for the interface on NVM subsystem A.
7. If the SUBTYPE field of the Discovery Log Page Entry for NVM subsystem A returned from the

CDC is set to 02h (i.e., NVM subsystem), then Host A should connect to the I/O controller on NVM
subsystem A.
8. A fabric interface on NVM subsystem B is registered with the CDC. This is accomplished by either:


a. using the Discovery Information Management command to perform a push registration;
b. notifying the CDC that a pull registration is required and the NVM subsystem port must be

implicitly registered by the CDC; or
c. administratively configured (e.g., the NVM subsystem port was manually configured on the

CDC).


9. The CDC sends a Discovery Log Page Change Asynchronous Event notification (Asynchronous

Event Information F0h) to notify Host A that the Discovery log page has changed.
10. Host A uses the Get Log Page command to retrieve the Discovery log page from the CDC.
11. The CDC responds to the Get Log Page command with a Discovery log page containing two

Discovery Log Page Entries: one for the interface on NVM subsystem A and another for the
interface on NVM subsystem B.
12. If the SUBTYPE field of the Discovery log page for NVM subsystem B returned from the CDC is

set to 02h (i.e., NVM subsystem), then Host A should connect to the I/O controller on NVM
subsystem B. The connection between Host A and NVM subsystem A remains unchanged.


**Discovery Information Registration and De-Registration**


Discovery information registration is the process of registering host or NVM subsystem discovery
information with a Centralized Discovery controller (CDC) or registering host discovery information with a
Direct Discovery controller (DDC).


Discovery information registration may be performed:

  - using a push registration (refer to section 8.3.2.2.1); or

  - using a pull registration (refer to section 8.3.2.2.21).


607


NVM Express [®] Base Specification, Revision 2.2


Information from a Connect command (e.g., Host NQN) may be retained by a Discovery controller to provide
a limited set of discovery information. If the Discovery controller determines that the host that submitted the
Connect command is the same as a host for which the Discovery controller has retained host discovery
information from a previous push registration, then the Discovery controller should continue to retain that
host discovery information.


A host:

  - should use push registrations to register host discovery information with a CDC or DDC; and

  - is not able to use pull registrations to register discovery information.


A CDC:

  - may use push registrations to register host discovery information with a DDC; and

  - shall not use pull registrations to register discovery information.


A DDC:

  - should use push registrations when registering NVM subsystem discovery information with a CDC;
or

  - may use pull registrations when registering NVM subsystem discovery information with a CDC.


Discovery information de-registration is the process of de-registering host or NVM subsystem discovery
information with a CDC or de-registering host discovery information with a DDC.


Discovery information de-registration may be performed using one of the following methods:

  - a push de-registration (refer to section 8.3.2.2.1); or

  - a pull de-registration (refer to section 8.3.2.2.2).


A host:

  - may use push de-registrations to de-register host discovery information with a CDC or DDC; and

  - is not able to use pull de-registrations to de-register discovery information.


A CDC:

  - may use push de-registrations to de-register host discovery information with a DDC; and

  - shall not use pull de-registrations to de-register discovery information.


A DDC:

  - should use push de-registrations to de-register NVM subsystem discovery information with a CDC;
or

  - may use pull de-registrations to de-register NVM subsystem discovery information with a CDC.


**8.3.2.2.1** **Push Registrations and Push De-Registrations**


A push registration is performed using the Discovery Information Management command (refer to section
5.3.3) with the Task (TAS) field (refer to Figure 497) cleared to 0h to explicitly register discovery information
for a host or NVM subsystem with a Centralized Discovery controller (CDC) or explicitly register discovery
information for a host with a Direct Discovery controller (DDC).


A push de-registration is performed using the Discovery Information Management command with the TAS
field set to 1h to explicitly de-register discovery information for a host or NVM subsystem with a CDC or
explicitly de-register discovery information for a host with a DDC.


A DDC that performs push registrations or push de-registrations implements host functionality (e.g.,
submitting commands, processing command completions, providing a Host NQN, etc.).


**8.3.2.2.2** **Pull Registrations and Pull De-Registrations**


A pull registration may be requested using a kickstart discovery request and response sequence (refer to
section 8.3.2.2.2).


608


NVM Express [®] Base Specification, Revision 2.2


Upon completion of acknowledging a pull registration request (e.g., after a KDResp NVMe/TCP PDU (refer
to the Kickstart Discovery Response PDU section in the NVMe TCP Transport Specification) has been sent
by the Centralized Discovery controller (CDC)), the CDC performs the pull registration by:


1. sending a Connect command to the Direct Discovery controller (DDC) to establish an NVMe

connection with that DDC; and
2. sending a Get Log Page command to the DDC with the Log Page Identifier (LID) field set to 70h to

retrieve NVM subsystem discovery information contained in the associated Discovery log page
from that DDC. The CDC may:


a. set the Port Local Entries Only (PLEO) bit to ‘1’ in the Log Specific Parameter (LSP) field in

that Get Log Page command to request that NVM subsystem discovery information entries for
only NVM subsystem ports that are presented through the same NVM subsystem port on the
DDC that received the Get Log Page command be returned; and
b. set the All NVM Subsystem Entries (ALLSUBE) bit to ‘1’ in the LSP field in that Get Log Page

command to request that records for all NVM subsystem ports be returned.


The DDC should match the NQN contained in the CDC NVMe Qualified Name (CDCNQN) field of the
KDResp NVMe/TCP PDU with the NQN contained in the Host NVMe Qualified Name (HOSTNQN) field in
the data portion of the Connect command to know that a CDC is performing a pull registration.


If the PLEO bit is cleared to ‘0’ and the ALLSUBE bit is set ‘1’ in the LSP field of the Get Log Page command,
then the DDC shall return all NVM subsystem discovery information entries in the resulting Discovery log
page sent to the CDC (i.e., the DDC shall not filter out any NVM subsystem discovery information entries).


If the PLEO bit is set to ‘1’ and the ALLSUBE bit is set ‘1’ in the LSP field of the Get Log Page command,
then the DDC shall return all NVM subsystem discovery information entries for NVM subsystem ports that
are presented through the same NVM subsystem port on the DDC that received the Get Log Page
command in the resulting Discovery log page sent to the CDC (i.e., the DDC shall not filter out any NVM
subsystem discovery information entries for NVM subsystem ports that are presented through the same
NVM subsystem port on the DDC that received the Get Log Page command).


An additional pull registration or a pull de-registration may be requested by either:

  - sending a Discovery Log Page Change Asynchronous Event notification (Asynchronous Event
Information F0h) (refer to section 3.1.3.3.2); or

  - requesting another pull registration.


If the CDC established an explicit persistent connection with the DDC when performing the previous pull
registration, then the DDC should request the additional pull registration or the pull de-registration by
sending a Discovery Log Page Change Asynchronous Event notification.


If the CDC did not establish an explicit persistent connection with the DDC when performing the previous
pull registration, then the DDC requests the additional pull registration or the pull de-registration by
requesting another pull registration.


Upon receiving a Discovery Log Page Change Asynchronous Event notification, the CDC performs the
additional pull registration or the pull de-registration by using the following sequence:


1. sending a Get Log Page command to the DDC with the LID field set to 70h to retrieve NVM

subsystem discovery information contained in the associated Discovery log page from that DDC.
The CDC may:


a. set the Port Local Entries Only (PLEO) bit to ‘1’ in the Log Specific Parameter (LSP) field in

that Get Log Page command to request that NVM subsystem discovery information entries for
only NVM subsystem ports that are presented through the same NVM subsystem port on the
DDC that received the Get Log Page command be returned; and
b. set the All NVM Subsystem Entries (ALLSUBE) bit to ‘1’ in the LSP field in that Get Log Page

command to request that records for all NVM subsystem ports be returned;


and


609


NVM Express [®] Base Specification, Revision 2.2


2. replacing all existing NVM subsystem discovery information from the previous pull registration with

the newly retrieved NVM subsystem discovery information (i.e., only the most recent NVM
subsystem discovery information from that DDC is retained by the CDC).


Upon receiving another pull registration request, the CDC performs the additional pull registration or the
pull de-registration by using the following sequence:


1. acknowledging that pull registration request (refer to section 8.3.2.2.2.1 for kickstart discovery);

and
2. sending a Connect command to the DDC to establish an NVMe connection with that DDC ; and
3. sending a Get Log Page command to the DDC with the LID field set to 70h to retrieve NVM

subsystem discovery information contained in the associated Discovery log page from that DDC.
The CDC may:


a. set the Port Local Entries Only (PLEO) bit to ‘1’ in the Log Specific Parameter (LSP) field of the

Get Log Page command to request that NVM subsystem discovery information entries for only
NVM subsystem ports that are presented through the same NVM subsystem port on the DDC
that received the Get Log Page command be returned; and
b. set the All NVM Subsystem Entries (ALLSUBE) bit to ‘1’ in the LSP field of the Get Log Page

command to request that records for all NVM subsystem ports be returned;


and


4. replacing all existing NVM subsystem discovery information from the previous pull registration with

the newly retrieved NVM subsystem discovery information (i.e., only the most recent NVM
subsystem discovery information from that DDC is retained by the CDC).


**Kickstart Discovery Pull Registration Requests**


Figure 679 illustrates the process used during a kickstart discovery request and response sequence. The
first step is to establish a TCP connection between a Direct Discovery controller (DDC) and a Centralized
Discovery controller (CDC). For kickstart discovery, the CDC acts as the passive side of the TCP connection
and is set to “listen” for DDC-initiated TCP connection establishment requests. The IP address used by the
DDC to establish the TCP connection with the CDC may be obtained from the A or AAAA record provided
in an mDNS response from the CDC, as described in section 8.3.1.3.4.


Once a TCP connection has been established, if an ICReq NVMe/TCP PDU (refer to the Initialize
Connection Request PDU section in the NVMe TCP Transport Specification) from a DDC with the Kickstart
Discovery Connection (KDCONN) bit set to ‘1’ in the FLAGS field is received by a CDC, then the CDC shall
respond with an ICResp NVMe/TCP PDU (refer to the Initialize Connection Response PDU section in the
NVMe TCP Transport Specification) to establish a kickstart discovery NVMe/TCP connection.


Once a kickstart discovery NVMe/TCP connection has been established, if a KDReq NVMe/TCP PDU (refer
to the Kickstart Discovery Request PDU section in the NVMe TCP Transport Specification) from a DDC is
received by a CDC, then the CDC shall respond with a KDResp NVMe/TCP PDU (refer to the Kickstart
Discovery Response PDU section in the NVMe TCP Transport Specification) to accept the pull registration
request and connection parameters. The KDResp NVMe/TCP PDU sent by the CDC shall include the NQN
of that CDC in the CDC NVMe Qualified Name (CDCNQN) field. After sending a KDResp NVMe/TCP PDU
to the DDC where the Kickstart Status (KSSTAT) field is set to SUCCESS, the kickstart discovery
NVMe/TCP connection should be torn down, and the CDC performs a pull registration with the DDC as
described in section 8.3.2.2.2 using the connection parameters obtained from the KDReq NVMe/TCP PDU.


If the total number of discovery information entries being registered by the pull registration (i.e., as specified
by the Number of Discovery Information Entries (NUMDIE) field in the KDReq NVMe/TCP PDU) exceeds
the available capacity for new discovery information entries on the CDC, then the CDC shall send a KDResp
NVMe/TCP PDU to the DDC where the KSSTAT field is set to FAILURE and the Failure Reason (FAILRSN)
field is set to Insufficient Discovery Resources.


610


NVM Express [®] Base Specification, Revision 2.2


**Figure 679: Kickstart Discovery Request and Response Sequence**


**DDC** **CDC**


**Fabric Zoning**


**8.3.2.3.1** **Model**


A Centralized Discovery controller (CDC) may provide centralized access control services (i.e., Fabric
Zoning) for an NVMe-oF IP-based fabric. CDC-based Fabric Zoning provides a way to control the Discovery
log pages provided in response to a Get Log Page command issued to the CDC. Fabric Zoning should be
based on a Zoning database maintained by the CDC and containing two fundamental data structures: the
ZoneDBConfig and the ZoneDBActive, as shown in Figure 680.


**Figure 680: Zoning DB Abstract Representation**


The ZoneDBActive is a list of enforced ZoneGroups. The enforcement actions include:

  - Discovery log page filtering;

  - Discovery Log Page Change Asynchronous Event notifications (refer to section 8.3.2.4); and

  - optionally, network level restrictions (refer to section 8.3.2.3.5.2).


The abstract representation of the ZoneDBActive is shown in Figure 681.


611


NVM Express [®] Base Specification, Revision 2.2


**Figure 681: ZoneDBActive Abstract Representation**









The ZoneDBConfig is a list of configured ZoneGroups and ZoneAliases, as shown in Figure 682.


**Figure 682: ZoneDBConfig Abstract Representation**

















**8.3.2.3.2** **ZoneGroup**


A ZoneGroup is the unit of activation (i.e., a set of access control rules enforceable by the CDC). The
detailed representation of a ZoneGroup is shown in Figure 683.


**Figure 683: ZoneGroup Detailed Representation**





|Bytes|Description|
|---|---|
|223:00|**ZoneGroup Originator (ZGORIG):** This field contains the NQN<br>(represented as a null-terminated string, NULL padded as<br>necessary to the 224-byte maximum length) of either:<br>• <br>the CDC, if this ZoneGroup was created on the CDC;<br>or <br>• <br>the DDC that created this ZoneGroup, if this<br>ZoneGroup was created by a DDC.|
|253:224|**ZoneGroup Name (ZGNAME):** This field contains an ASCII<br>encoded null-terminated string, NULL padded as necessary to<br>the 30-byte maximum length.|
|255:254|**Number of Zones (NUMZ):** This field specifies the number of<br>Zones contained in this ZoneGroup. The value of this field is<br>represented as n**. **|
|255+LenZ1:256|**Zone 1 (Z1):** This field contains the first Zone contained in this<br>ZoneGroup as defined in Figure 684. The length of this field is<br>represented as LenZ1.|


612


NVM Express [®] Base Specification, Revision 2.2


**Figure 683: ZoneGroup Detailed Representation**






|Bytes|Description|
|---|---|
|255+LenZ1+LenZ2:256+LenZ1|**Zone 2 (Z2):** This field contains the second Zone contained in<br>this ZoneGroup as defined in Figure 684 (if present). The length<br>of this field is represented as LenZ2.|
|…|…|
|255+LenZ1+…+LenZn:256+LenZ1+…+LenZn-1|**Zone N (ZN):** This field contains the Nth Zone contained in this<br>ZoneGroup as defined in Figure 684 (if present). The length of<br>this field is represented as LenZn.|



A ZoneGroup is uniquely identified by the pair {ZoneGroup Name, ZoneGroup Originator}. For each
ZoneGroup, the CDC shall maintain:

  - a unique ZoneGroup key, used as a compact ZoneGroup identifier in the FZS and FZR commands
(refer to sections 5.3.6 and 5.3.5 respectively). ZoneGroup keys should not be reused; and

  - a generation number, incremented each time a ZoneGroup is updated and used by the GAZ
operation (refer to section 8.3.2.3.8.2). If the value of the generation number is FFFFFFFFh, then
the generation number shall be set to 1h when incremented (i.e., rolls over to 1h).


**8.3.2.3.3** **Zone**


A Zone is the unit of access control. Zone members belonging to the same Zone are allowed to
communicate between each other, according to the rules specified in section 8.3.2.3.4.1. The detailed
representation of a Zone is shown in Figure 684.


**Figure 684: Zone Detailed Representation**





















|Bytes|Description|
|---|---|
|123:00|**Zone Name (ZNAME):** This field contains an ASCII encoded null-<br>terminated string, NULL padded as necessary to the 124-byte maximum<br>length.|
|125:124|**Number of Zone Members (NUMZM):** This field specifies the number<br>of Zone members contained in this Zone. The value of this field is<br>represented as n.|
|127:126|**Number of Zone Properties (NUMZP):** This field specifies the number<br>of Zone properties contained in this Zone. The value of this field is<br>represented as k.|
|383:128|**Zone Member 1 (ZM1):** This field contains the first Zone member<br>contained in this Zone.|
|639:384|**Zone Member 2 (ZM2):** This field contains the second Zone member<br>contained in this Zone.|
|…|…|
|256*n+127:256*n-128|**Zone Member n (ZMn):** This field contains the Nth Zone member<br>contained in this Zone (if present).|
|256*n+127+LenP1:256*n+128|**Zone Property 1 (ZP1):** This field contains the first Zone property<br>contained in this Zone (if present). The length of this field is represented<br>as LenP1.|
|256*n+127+LenP1+LenP2: <br>256*n+128+LenP1|**Zone Property 2 (ZP2):** This field contains the second Zone property<br>contained in this Zone (if present). The length of this field is represented<br>as LenP2.|
|…|…|
|256*n+127+LenP1+LenP2+…+LenPk: <br>256*n+128+LenP1+LenP2+…+LenPk-1|**Zone Property k (ZPk):** This field contains the Kth Zone property<br>contained in this Zone (if present). The length of this field is represented<br>as LenPk.|


613


NVM Express [®] Base Specification, Revision 2.2


**8.3.2.3.4** **Zone Members**


**Overview**


Zone members are represented as type-length-value (TLV) data structures. Figure 685 shows the defined
Zone member types. If a Zone member type does not include a particular element in the pairing for that
Zone member type, then the element values of that type shall not be used for enforcement of Zoning
restrictions for that Zone (e.g., Zone member type 1h does not include IP addresses in the enforcement of
that Zone member type).


**Figure 685: Zone Member Types**

|Type|Definition|Reference|
|---|---|---|
|1h|The pair {NQN, Role}|8.3.2.3.4.2|
|2h|The pair {(NQN, IP, Protocol), Role}|8.3.2.3.4.3|
|3h|The pair {(NQN, IP, Protocol, IP Protocol Port), Role}|8.3.2.3.4.4|
|4h|The pair {(NQN, IP, Protocol, IP Protocol Port, PortID), Role}|8.3.2.3.4.5|
|5h|The pair {(NQN, PortID), Role}|8.3.2.3.4.6|
|6h|The pair {(NQN, Protocol, PortID, ADRFAM), Role}|8.3.2.3.4.7|
|11h|The pair {(IP, Protocol), Role}|8.3.2.3.4.8|
|12h|The pair {(IP, Protocol, IP Protocol Port), Role}|8.3.2.3.4.9|
|EFh|A ZoneAlias name|8.3.2.3.4.10|
|F0h to FEh|Vendor specific|Vendor specific|
|All others|Reserved|Reserved|



The members of a Zone may communicate with each other using the following rules:

  - hosts may communicate with NVM subsystems;

  - NVM subsystems may communicate with hosts;

  - hosts shall not communicate with hosts; and

  - NVM subsystems shall not communicate with NVM subsystems.


A Zone of a ZoneGroup belonging to the ZoneDBConfig may use all defined Zone member types. When a
ZoneGroup belonging to the ZoneDBConfig is activated and becomes part of the ZoneDBActive, all
ZoneAlias name Zone members are resolved in the group of NVMe entities referenced by the ZoneAlias
name.


**{NQN, Role} Zone Member Type (Type 1h)**


This Zone member type identifies all fabric interfaces, all IP protocols (e.g., TCP or UDP), and all IP protocol
ports (e.g., TCP port 4420) that may be used by the NVMe-oF entity identified by the Zone member’s NQN.
The format of this Zone member type is shown in Figure 686.


**Figure 686: {NQN, Role} Zone Member Format**









|Bytes|Description|
|---|---|
|00|**Zone Member Type (ZMTYPE):** This field specifies the Zone member type and shall be set to 1h.|
|02:01|**Zone Member Length (ZMLEN**): This field specifies the length in bytes of this Zone member type and<br>shall be set to 100h.|
|03|**Zone Member Role (ZMROLE):**This field specifies what type of entity the Zone member is. This field<br>shall be set to one of the following values:<br>• <br>1h: host; or<br>• <br>2h: NVM subsystem**. **|
|31:04|Reserved|
|255:32|**Zone Member NQN (ZMNQN):** This field specifies the NQN (represented as a null-terminated string,<br>NULL padded as necessary to the 224-byte maximum length) of the referenced NVMe-oF entity.|


614


NVM Express [®] Base Specification, Revision 2.2


**{(NQN, IP, Protocol), Role} Zone Member Type (Type 2h)**


This Zone member type identifies a specific fabric interface (i.e., through the IP address) and the specific
IP protocol (e.g., TCP) used by the NVMe-oF entity identified by the Zone member’s NQN over that fabric
interface. The format of this Zone member type is shown in Figure 687.


**Figure 687: {(NQN+IP+Protocol), Role} Zone Member Format**














|Bytes|Description|
|---|---|
|15:00|**IPv6 Address (IPV6ADDR):** This field contains an IPv6 address.|



|Bytes|Description|
|---|---|
|00|**Zone Member Type (ZMTYPE):** This field specifies the Zone member type and shall be set to 2h.|
|02:01|**Zone Member Length (ZMLEN):** This field specifies the length in bytes of this Zone member type and<br>shall be set to 100h.|
|03|**Zone Member Role (ZMROLE):**This field specifies what type of entity the Zone member is. This field<br>shall be set to one of the following values:<br>• <br>1h: host; or<br>• <br>2h: NVM subsystem.|
|04|**Zone Member Address Family (ZMADRFAM):**This field specifies the IP address family. This field shall<br>be set to one of the following values:<br>• <br>1h: IPv4 address family; or<br>• <br>2h: IPv6 address family.|
|05|**Zone Member IP Protocol (ZMIPPROTO):**This field specifies the IP protocol. This field shall be set to<br>one of the following values:<br>• <br>6h: TCP; or<br>• <br>11h: UDP.|
|07:06|Reserved|
|23:08|**Zone Member Transport Address (ZMTRADDR):**This field specifies the IP address. An IPv6 address<br>is encoded in binary as follows:<br>**Bytes**<br>**Description**<br>15:00<br>**IPv6 Address (IPV6ADDR):** This field contains an IPv6 address.<br>An IPv4 address is encoded in binary as follows:<br>**Bytes**<br>**Description**<br>03:00<br>**IPv4 Address (IPV4ADDR):** This field contains an IPv4 address.<br>15:04<br>Reserved|
|31:24|Reserved|
|255:32|**Zone Member NQN (ZMNQN):** This field specifies the NQN (represented as a null-terminated string,<br>NULL padded as necessary to the 224-byte maximum length) of the referenced NVMe-oF entity.|


|Bytes|Description|
|---|---|
|03:00|**IPv4 Address (IPV4ADDR):** This field contains an IPv4 address.|
|15:04|Reserved|


**{(NQN, IP, Protocol, IP Protocol Port), Role} Zone Member Type (Type 3h)**


This Zone member type identifies a specific fabric interface (i.e., through the IP address), the specific IP
protocol (e.g., TCP), and IP protocol port (e.g., TCP port 4420) used by the NVMe-oF entity identified by
the Zone member’s NQN over that fabric interface. The format of this Zone member type is shown in Figure
688.


**Figure 688: {(NQN+IP+Protocol+IP Protocol Port), Role} Zone Member Format**





|Bytes|Description|
|---|---|
|00|**Zone Member Type (ZMTYPE):** This field specifies the Zone member type and shall be set to 3h.|
|02:01|**Zone Member Length (ZMLEN):** This field specifies the length in bytes of this Zone member type and<br>shall be set to 100h.|
|03|**Zone Member Role (ZMROLE):**This field specifies what type of entity the Zone member is. This field<br>shall be set to one of the following values:<br>• <br>1h: host; or<br>• <br>2h: NVM subsystem.|


615


NVM Express [®] Base Specification, Revision 2.2


**Figure 688: {(NQN+IP+Protocol+IP Protocol Port), Role} Zone Member Format**














|Bytes|Description|
|---|---|
|15:00|**IPv6 Address (IPV6ADDR):** This field contains an IPv6 address.|


|Bytes|Description|
|---|---|
|03:00|**IPv4 Address (IPV4ADDR):** This field contains an IPv4 address.|
|15:04|Reserved|



|Bytes|Description|
|---|---|
|04|**Zone Member Address Family (ZMADRFAM):**This field specifies the IP address family. This field shall<br>be set to one of the following values:<br>• <br>1h: IPv4 address family; or<br>• <br>2h: IPv6 address family.|
|05|**Zone Member IP Protocol (ZMIPPROTO):**This field specifies the IP protocol. This field shall be set to<br>one of the following values:<br>• <br>6h: TCP; or<br>• <br>11h: UDP.|
|07:06|**Zone Member Transport Service Identifier (ZMTRSVCID):** This field specifies the TCP or UDP port.|
|23:08|**Zone Member Transport Address (ZMTRADDR):**This field specifies the IP address. An IPv6 address<br>is encoded in binary as follows:<br>**Bytes**<br>**Description**<br>15:00<br>**IPv6 Address (IPV6ADDR):** This field contains an IPv6 address.<br>An IPv4 address is encoded in binary as follows:<br>**Bytes**<br>**Description**<br>03:00<br>**IPv4 Address (IPV4ADDR):** This field contains an IPv4 address.<br>15:04<br>Reserved<br>|
|31:24|Reserved|
|255:32|**Zone Member NQN (ZMNQN):** This field specifies the NQN (represented as a null-terminated string,<br>NULL padded as necessary to the 224-byte maximum length) of the referenced NVMe-oF entity.|


**{(NQN, IP, Protocol, IP Protocol Port, PortID), Role} Zone Member Type (Type 4h)**


This Zone member type identifies a specific fabric interface (i.e., through the IP address), the specific IP
protocol (e.g., TCP), IP protocol port (e.g., TCP port 4420), and PortID used by the NVMe-oF entity
identified by the Zone member’s NQN over that fabric interface. The format of this Zone member type is
shown in Figure 689.


**Figure 689: {(NQN+IP+Protocol+IP Protocol Port+PortID), Role} Zone Member Format**










|Bytes|Description|
|---|---|
|00|**Zone Member Type (ZMTYPE):** This field specifies the Zone member type and shall be set to 4h.|
|02:01|**Zone Member Length (ZMLEN):** This field specifies the length in bytes of this Zone member type and<br>shall be set to 100h.|
|03|**Zone Member Role (ZMROLE):**This field specifies what type of entity the Zone member is. This field<br>shall be set to one of the following values:<br>• <br>1h: host; or<br>• <br>2h: NVM subsystem.|
|04|**Zone Member Address Family (ZMADRFAM):**This field specifies the IP address family. This field shall<br>be set to one of the following values:<br>• <br>1h: IPv4 address family; or<br>• <br>2h: IPv6 address family.|
|05|**Zone Member IP Protocol (ZMIPPROTO):**This field specifies the IP protocol. This field shall be set to<br>one of the following values:<br>• <br>6h: TCP; or<br>• <br>11h: UDP.|
|07:06|**Zone Member Transport Service Identifier (ZMTRSVCID):** This field specifies the TCP or UDP port.|



616


NVM Express [®] Base Specification, Revision 2.2


**Figure 689: {(NQN+IP+Protocol+IP Protocol Port+PortID), Role} Zone Member Format**






|Bytes|Description|
|---|---|
|15:00|**IPv6 Address (IPV6ADDR):** This field contains an IPv6 address.|



|Bytes|Description|
|---|---|
|23:08|**Zone Member Transport Address (ZMTRADDR):**This field specifies the IP address. An IPv6 address<br>is encoded in binary as follows:<br>**Bytes**<br>**Description**<br>15:00<br>**IPv6 Address (IPV6ADDR):** This field contains an IPv6 address.<br>An IPv4 address is encoded in binary as follows:<br>**Bytes**<br>**Description**<br>03:00<br>**IPv4 Address (IPV4ADDR):** This field contains an IPv4 address.<br>15:04<br>Reserved|
|25:24|**Zone Member PortID (ZMPORTID):** This field specifies the NVM subsystem PortID.|
|31:26|Reserved|
|255:32|**Zone Member NQN (ZMNQN):** This field specifies the NQN (represented as a null-terminated string,<br>NULL padded as necessary to the 224-byte maximum length) of the referenced NVMe-oF entity.|


|Bytes|Description|
|---|---|
|03:00|**IPv4 Address (IPV4ADDR):** This field contains an IPv4 address.|
|15:04|Reserved|


**{(NQN, PortID), Role} Zone Member Type (Type 5h)**


This Zone member type identifies a specific PortID used by the NVMe-oF entity identified by the Zone
member’s NQN. The format of this Zone member type is shown in Figure 690.


**Figure 690: {(NQN+PortID), Role} Zone Member Format**









|Bytes|Description|
|---|---|
|00|**Zone Member Type (ZMTYPE):** This field specifies the Zone member type and shall be set to 5h.|
|02:01|**Zone Member Length (ZMLEN):** This field specifies the length in bytes of this Zone member type and<br>shall be set to 100h.|
|03|**Zone Member Role (ZMROLE):**This field specifies what type of entity the Zone member is. This field<br>shall be set to one of the following values:<br>• <br>1h: host; or<br>• <br>2h: NVM subsystem.|
|05:04|**Zone Member PortID (ZMPORTID):** This field specifies the NVM subsystem PortID.|
|31:06|Reserved|
|255:32|**Zone Member NQN (ZMNQN):** This field specifies the NQN (represented as a null-terminated string,<br>NULL padded as necessary to the 224-byte maximum length) of the referenced NVMe-oF entity.|


**{(NQN, Protocol, PortID, ADRFAM), Role} Zone Member Type (Type 6h)**


This Zone member type identifies the specific IP protocol (e.g., TCP), PortID, and Address Family used by
the NVMe-oF entity identified by the Zone member’s NQN over that fabric interface. The format of this Zone
member type is shown in Figure 691.


**Figure 691: {(NQN+Protocol+PortID+ADRFAM), Role} Zone Member Format**





|Bytes|Description|
|---|---|
|00|**Zone Member Type (ZMTYPE):** This field specifies the Zone member type and shall be set to 6h.|
|02:01|**Zone Member Length (ZMLEN):** This field specifies the length in bytes of this Zone member type and<br>shall be set to 100h.|
|03|**Zone Member Role (ZMROLE):**This field specifies what type of entity the Zone member is. This field<br>shall be set to one of the following values:<br>• <br>1h: host; or<br>• <br>2h: NVM subsystem.|
|04|**Zone Member Address Family (ZMADRFAM):**This field specifies the IP address family. This field shall<br>be set to one of the following values:<br>• <br>1h: IPv4 address family; or<br>• <br>2h: IPv6 address family.|


617


NVM Express [®] Base Specification, Revision 2.2


**Figure 691: {(NQN+Protocol+PortID+ADRFAM), Role} Zone Member Format**









|Bytes|Description|
|---|---|
|05|**Zone Member IP Protocol (ZMIPPROTO):**This field specifies the IP protocol. This field shall be set to<br>one of the following values:<br>• <br>6h: TCP; or<br>• <br>11h: UDP.|
|07:06|**Zone Member PortID (ZMPORTID):** This field specifies the NVM subsystem PortID.|
|31:08|Reserved|
|255:32|**Zone Member NQN (ZMNQN):** This field specifies the NQN (represented as a null-terminated string,<br>NULL padded as necessary to the 224-byte maximum length) of the referenced NVMe-oF entity.|


**{(IP, Protocol), Role} Zone Member Type (Type 11h)**


This Zone member type identifies the fabric interface (i.e., through the IP address) of an NVMe-oF entity
and the specific IP protocol (e.g., TCP) used by the NVMe-oF entity over that fabric interface. The format
of this Zone member type is shown in Figure 692.


**Figure 692: {(IP+Protocol), Role} Zone Member Format**














|Bytes|Description|
|---|---|
|15:00|**IPv6 Address (IPV6ADDR):** This field contains an IPv6 address.|



|Bytes|Description|
|---|---|
|00|**Zone Member Type (ZMTYPE):** This field specifies the Zone member type and shall be set to 11h.|
|02:01|**Zone Member Length (ZMLEN):** This field specifies the length in bytes of this Zone member type and<br>shall be set to 100h.|
|03|**Zone Member Role (ZMROLE):**This field specifies what type of entity the Zone member is. This field<br>shall be set to one of the following values:<br>• <br>1h: host; or<br>• <br>2h: NVM subsystem.|
|04|**Zone Member Address Family (ZMADRFAM):**This field specifies the IP address family. This field shall<br>be set to one of the following values:<br>• <br>1h: IPv4 address family; or<br>• <br>2h: IPv6 address family.|
|05|**Zone Member IP Protocol (ZMIPPROTO):**This field specifies the IP protocol. This field shall be set to<br>one of the following values:<br>• <br>6h: TCP; or<br>• <br>11h: UDP.|
|07:06|Reserved|
|23:08|**Zone Member Transport Address (ZMTRADDR):**This field specifies the IP address. An IPv6 address<br>is encoded in binary as follows:<br>**Bytes**<br>**Description**<br>15:00<br>**IPv6 Address (IPV6ADDR):** This field contains an IPv6 address.<br>An IPv4 address is encoded in binary as follows:<br>**Bytes**<br>**Description**<br>03:00<br>**IPv4 Address (IPV4ADDR):** This field contains an IPv4 address.<br>15:04<br>Reserved|
|255:24|Reserved|


|Bytes|Description|
|---|---|
|03:00|**IPv4 Address (IPV4ADDR):** This field contains an IPv4 address.|
|15:04|Reserved|


**{(IP, Protocol, IP Protocol Port), Role} Zone Member Type (Type 12h)**


This Zone member type identifies the fabric interface (i.e., through the IP address) of an NVMe-oF entity,
the specific IP protocol (e.g., TCP), and IP protocol port (e.g., TCP port 4420) used by the NVMe-oF entity
over that fabric interface. The format of this Zone member type is shown in Figure 693.


618


NVM Express [®] Base Specification, Revision 2.2


**Figure 693: {(IP+Protocol+IP Protocol Port), Role} Zone Member Format**














|Bytes|Description|
|---|---|
|15:00|**IPv6 Address (IPV6ADDR):** This field contains an IPv6 address.|



|Bytes|Description|
|---|---|
|00|**Zone Member Type (ZMTYPE):** This field specifies the Zone member type and shall be set to 12h.|
|02:01|**Zone Member Length (ZMLEN):** This field specifies the length in bytes of this Zone member type and<br>shall be set to 100h.|
|03|**Zone Member Role (ZMROLE):**This field specifies what type of entity the Zone member is. This field<br>shall be set to one of the following values:<br>• <br>1h: host; or<br>• <br>2h: NVM subsystem.|
|04|**Zone Member Address Family (ZMADRFAM):**This field specifies the IP address family. This field shall<br>be set to one of the following values:<br>• <br>1h: IPv4 address family; or<br>• <br>2h: IPv6 address family.|
|05|**Zone Member IP Protocol (ZMIPPROTO):**This field specifies the IP protocol. This field shall be set to<br>one of the following values:<br>• <br>6h: TCP; or<br>• <br>11h: UDP.|
|07:06|**Zone Member Transport Service Identifier (ZMTRSVCID):** This field specifies the TCP or UDP port.|
|23:08|**Zone Member Transport Address (ZMTRADDR):**This field specifies the IP address. An IPv6 address<br>is encoded in binary as follows:<br>**Bytes**<br>**Description**<br>15:00<br>**IPv6 Address (IPV6ADDR):** This field contains an IPv6 address.<br>An IPv4 address is encoded in binary as follows:<br>**Bytes**<br>**Description**<br>03:00<br>**IPv4 Address (IPV4ADDR):** This field contains an IPv4 address.<br>15:04<br>Reserved|
|255:24|Reserved|


|Bytes|Description|
|---|---|
|03:00|**IPv4 Address (IPV4ADDR):** This field contains an IPv4 address.|
|15:04|Reserved|


**{ZoneAlias} Zone Member Type**


This Zone member type is used to identify a ZoneAlias in a Zone definition. The format of this Zone member
type is shown in Figure 694.


**Figure 694: {ZoneAlias} Zone Member Format**

|Bytes|Description|
|---|---|
|00|**Zone Member Type (ZMTYPE):** This field specifies the Zone member type and shall be set to EFh.|
|02:01|**Zone Member Length (ZMLEN):** This field specifies the length in bytes of this Zone member type and<br>shall be set to 100h.|
|31:03|Reserved|
|155:32|**Zone Member ZoneAlias Name (ZMZANAME):** This field specifies an ASCII encoded null-terminated<br>string, NULL padded as necessary to the 124-byte maximum length.|
|255:156|Reserved|



**8.3.2.3.5** **Zone Properties**


**Overview**


Zone properties are represented as type-length-value (TLV) data structures. Unrecognized Zone properties
may be ignored. Figure 695 shows the defined Zone property types.


**Figure 695: Zone Property Types**

|Type|Definition|
|---|---|
|1h|Fabric Enforced Zone|



619


NVM Express [®] Base Specification, Revision 2.2


**Figure 695: Zone Property Types**

|Type|Definition|
|---|---|
|FEh to F0h|Vendor specific|
|All others|Reserved|



**Fabric Enforced Zone Property**


This Zone property specifies if a Zone is intended to be enforced through packet-by-packet network level
restrictions. The format of this Zone property is shown in Figure 696.


**Figure 696: Fabric Enforced Zone Property Format**






|Bytes|Description|
|---|---|
|00|**Zone Property Type (ZPTYPE):**This field specifies the Zone property type and shall be set to 1h.|
|02:01|**Zone Property Length (ZPLEN):** This field specifies the length in bytes of this Zone property type and<br>shall be set to 4h.|
|03|**Zone Property Value (ZPVAL):** This field specifies the value of this Zone property. This field shall be<br>set to the following value:<br>• <br>1h: Network level enforcement requested.<br>All other values are ignored.|



**8.3.2.3.6** **ZoneAlias**


A ZoneAlias is a convenient grouping of NVMe entities identified and is referenceable by a ZoneAlias name.
The detailed representation of a ZoneAlias is shown in Figure 697.


**Figure 697: ZoneAlias Detailed Representation**








|Bytes|Description|
|---|---|
|123:00|**ZoneAlias Name (ZANAME):** This field contains an ASCII encoded null-terminated string, NULL<br>padded as necessary to the 124-byte maximum length.|
|125:124|**Number of ZoneAlias Members (NUMZAM):** This field specifies the number of ZoneAlias members<br>contained in this ZoneAlias. The value of this field is represented as n.|
|127:126|Reserved|
|**ZoneAlias Member List**|**ZoneAlias Member List**|
|383:128|**ZoneAlias Member 1:** This field contains the first ZoneAlias member contained in this ZoneAlias.|
|639:384|**ZoneAlias Member 2:** This field contains the second ZoneAlias member contained in this ZoneAlias<br>(if present).|
|…|…|
|256*n+127:<br>256*n-128|**ZoneAlias Member n:** This field contains the last ZoneAlias member contained in this ZoneAlias (if<br>present).|



**8.3.2.3.7** **ZoneAlias Members**


**Overview**


ZoneAlias members are represented as type-length-value (TLV) data structures. ZoneAlias members may
be any of the Zone member types specified in Figure 685 except the ZoneAlias Zone member type (i.e.,
ZMTYPE field set to EFh).


**8.3.2.3.8** **Zoning Operations**


**Overview**


ZoneGroups are data structures maintained and managed (i.e., created, read, modified, or deleted) in the
Zoning database of the CDC. During access to a ZoneGroup (e.g., the ZoneGroup is created or modified)
through an administrative interface (e.g., an administrative interface on the CDC outside the scope of this


620


NVM Express [®] Base Specification, Revision 2.2


specification or the protocol defined in this specification), the ZoneGroup may become locked to access
from any other interface.


Management of ZoneGroups generally happens through an administrative interface on the CDC. Push
model Direct Discovery controllers (DDCs) may be able to manage their own ZoneGroups (i.e., ZoneGroups
having the DDC NQN as ZoneGroup Originator) as specified in section 8.3.2.3.8.2. Pull model DDCs may
be able to manage their own ZoneGroups (i.e., ZoneGroups having the DDC NQN as ZoneGroup
Originator) as specified in section 8.3.2.3.8.3.


By default, a ZoneGroup should be accessible only to an administrative interface outside the scope of this
specification on the CDC and to the ZoneGroup originator DDC through the protocol defined in this
specification.


If Fabric Zoning is not enabled on the CDC, then that CDC:

  - shall abort all Fabric Zoning commands (i.e., any Fabric Zoning command that is issued as part of
a Zoning operation) issued by a push model DDC with a status code of Requested Function
Disabled; and

  - shall not react to Pull Model DDC Request asynchronous event notifications issued by a pull model
DDC.


**Push Model DDC Operations**


**8.3.2.3.8.2.1 Get Active ZoneGroup (GAZ)**


The Get Active ZoneGroup (GAZ) operation allows a DDC to retrieve from the CDC an active ZoneGroup
associated with the DDC initiating the GAZ operation. For a push model DDC, the GAZ operation is mapped
to an FZL command to lookup the key of the ZoneGroup to retrieve in ZoneDBActive in that CDC, followed
by one or more FZR commands to retrieve that ZoneGroup from the CDC, as shown in Figure 698.


**Figure 698: GAZ for Push Model DDC**


The identifier of the ZoneGroup to get is provided in the FZL buffer, as shown in Figure 699.


**Figure 699: FZL Data for GAZ**

|Bytes|Description|
|---|---|
|00|**Operation Type (OTYP):** 1h (i.e., Lookup for Get Active ZoneGroup)|
|03:01|Reserved|
|227:04|**ZoneGroup Originator (ZGORIG)**|
|257:228|**ZoneGroup Name (ZGNAME)**|



621


NVM Express [®] Base Specification, Revision 2.2


The FZL command returns the key of the ZoneGroup to retrieve as a Zoning Data key value in the
Completion Queue. For the FZL command of a GAZ operation:

  - if the requested ZoneGroup does not exist on the CDC, then the CDC shall abort the command
with a status code of Zoning Data Structure Not Found; or

  - if the requested ZoneGroup is locked on the CDC (i.e., another administrative interface is modifying
that ZoneGroup), then the CDC shall abort the command with a status code of Zoning Data
Structure Locked.


The Zoning Data key value returned by the FZL command is used in Command Dword 10 of an FZR
command (refer to Figure 507) to retrieve that ZoneGroup or a fragment of that ZoneGroup. The ZoneGroup
definition is retrieved through one or more subsequent FZR commands and is returned in the FZR buffer,
as shown in Figure 700. The FZR completion queue entry sending the last fragment shall have the Last
Fragment (LF) bit set to ‘1’ in Completion Queue Entry Dword 0 (refer to Figure 511).


**Figure 700: FZR Data for GAZ**

|Bytes|Description|
|---|---|
|00|**Operation Type (OTYP):** 2h (i.e., Get Active ZoneGroup for a push model DDC)|
|03:01|Reserved|
|07:04|**ZoneGroup Generation Number (ZGGN)**|
|11:08|**ZoneGroup Fragment Length (ZGFL)**|
|15:12|Reserved|
|ZGFL+15:16|**ZoneGroup Fragment (ZGF)**|



For the FZR command of a GAZ response operation:

  - if the ZoneGroup identified by the specified ZoneGroup key does not exist on the CDC, then the
CDC shall abort the command with a status code of Zoning Data Structure Not Found; or

  - if the ZoneGroup identified by the specified ZoneGroup key is locked on the CDC (i.e., another
administrative interface is modifying that ZoneGroup), then the CDC shall abort the command with
a status code of Zoning Data Structure Locked.


When a ZoneGroup is transferred in multiple fragments, the receiver shall verify that the ZoneGroup
generation number stays constant across all FZR commands. If the ZoneGroup generation number
changes, then the GAZ operation shall be aborted. The DDC shall not process received ZoneGroup
information until the full ZoneGroup (i.e., all of the fragments of the ZoneGroup) is received.


The CDC may enforce access restrictions to the Zoning data structures. In this case, the CDC shall check
if the DDC issuing the FZL command or FZR command is authorized to read the ZoneGroup specified in
the FZL data (e.g., if the CDC allows access to a ZoneGroup only to the DDC that created that ZoneGroup,
verify that the ZoneGroup Originator field matches the NQN contained in the HOSTNQN field of the Connect
command sent from the DDC to that CDC). If that DDC is not authorized to access the specified ZoneGroup,
then the CDC shall abort the FZL command and the FZR command with a status code of ZoneGroup
Originator Invalid.


**8.3.2.3.8.2.2 Add/Replace Active ZoneGroup (AAZ)**


The Add/Replace Active ZoneGroup (AAZ) operation allows a DDC to add or replace in the CDC an active
ZoneGroup associated with the DDC initiating the AAZ operation. For a push model DDC, the AAZ
operation is mapped to an FZL command to lookup the key of the ZoneGroup to add or replace in
ZoneDBActive in that CDC, followed by one or more FZS commands to provide the CDC with the
ZoneGroup to add or replace, as shown in Figure 701.


622


NVM Express [®] Base Specification, Revision 2.2


**Figure 701: AAZ for Push Model DDC**


The identifier of the ZoneGroup to add or replace is provided in the FZL buffer, as shown in Figure 702.


**Figure 702: FZL Data for AAZ**

|Bytes|Description|
|---|---|
|00|**Operation Type (OTYP):** 3h (i.e., Lookup for Add/Replace Active ZoneGroup)|
|03:01|Reserved|
|227:04|**ZoneGroup Originator (ZGORIG)**|
|257:228|**ZoneGroup Name (ZGNAME)**|



The FZL command returns the key of the ZoneGroup to add or replace as a Zoning Data key value in the
Completion Queue. For the FZL command of an AAZ operation:

  - if the ZoneGroup that matches the specified FZL data exists in ZoneDBActive in that CDC and is
locked by another administrative interface, then the CDC shall abort the command with a status
code of Zoning Data Structure Locked;

  - if the ZoneGroup that matches the specified FZL data exists in ZoneDBActive in that CDC and is
not locked by another administrative interface, then that ZoneGroup should be locked by the
submitting DDC and its key shall be returned as the Zoning Data key in the Completion Queue; or

  - if the ZoneGroup that matches the specified FZL data does not exist in ZoneDBActive in that CDC,
then an empty ZoneGroup having the provided identifier shall be created in ZoneDBActive in that
CDC, that ZoneGroup should be locked by the submitting DDC, and its key shall be returned as
the Zoning Data key in the Completion Queue.


Successful completion of the FZL command for the AAZ operation results in the identified ZoneGroup on
the CDC being locked by the DDC performing the operation.


The ZoneGroup to add or replace is provided in the FZS buffer of subsequent FZS commands with the
appropriate Zoning Data key in Command Dword 10 (refer to Figure 513) and is transferred in one or more
fragments, as needed, as shown in Figure 703. The FZS command sending the last fragment shall have
the Last Fragment (LF) bit set to ‘1’ in Command Dword 12 (refer to Figure 515).


**Figure 703: FZS Data for AAZ**

|Bytes|Description|
|---|---|
|00|**Operation Type (OTYP):** 4h (i.e., Add/Replace Active ZoneGroup for a push model DDC)|
|03:01|Reserved|
|NUMD*4+03:04|**ZoneGroup Fragment (ZGF)**|



For the FZS command of an AAZ request operation:


623


NVM Express [®] Base Specification, Revision 2.2


  - if the ZoneGroup identified by the specified ZoneGroup key does not exist on the CDC, then the
CDC shall abort the command with a status code of Zoning Data Structure Not Found; or

  - if the ZoneGroup identified by the specified ZoneGroup key is locked by another entity on the CDC
(i.e., another administrative interface is modifying that ZoneGroup), then the CDC shall abort the
command with a status code of Zoning Data Structure Locked.


The CDC shall update a ZoneGroup and increment its generation number only upon successful reception
of the full ZoneGroup (i.e., all of the fragments of the ZoneGroup). Successful receipt of the full ZoneGroup
for the AAZ operation shall unlock the identified ZoneGroup on the CDC. If the full ZoneGroup is not
received within 30 seconds from the establishment of the lock (during processing of the related FZL
command), then all the received data shall be discarded and the lock shall be released (i.e., ZoneDBActive
in that CDC is not changed).


The CDC may enforce access restrictions to the Zoning data structures. In this case, the CDC shall check
if the DDC issuing the FZL command or FZS command is authorized to write the ZoneGroup specified in
the FZL data (e.g., if the CDC allows access to a ZoneGroup only to the DDC that created that ZoneGroup,
verify that the ZoneGroup Originator field matches the NQN contained in the HOSTNQN field of the Connect
command sent from the DDC to that CDC). If that DDC is not authorized to access the specified ZoneGroup,
then the CDC shall abort the FZL command and the FZS command with a status code of ZoneGroup
Originator Invalid.


**8.3.2.3.8.2.3 Remove Active ZoneGroup (RAZ)**


The Remove Active ZoneGroup (RAZ) operation allows a DDC to remove from the CDC an active
ZoneGroup associated with the DDC initiating the RAZ operation. For a push model DDC, the RAZ
operation is mapped to an FZL command to provide to the CDC with the identifier of the ZoneGroup to
remove, as shown in Figure 704.


**Figure 704: RAZ for Push Model DDC**


The identifier of the ZoneGroup to remove is provided in the FZL buffer, as shown in Figure 705.


**Figure 705: FZL Data for RAZ**

|Bytes|Description|
|---|---|
|00|**Operation Type (OTYP):** 5h (i.e., Lookup for Remove Active ZoneGroup)|
|03:01|Reserved|
|227:04|**ZoneGroup Originator (ZGORIG)**|
|257:228|**ZoneGroup Name (ZGNAME)**|



For the FZS command of an RAZ request operation:

  - if the requested ZoneGroup does not exist on the CDC, then the CDC shall abort the command
with a status code of Zoning Data Structure Not Found; or

  - if the requested ZoneGroup is locked on the CDC (i.e., another administrative interface is modifying
that ZoneGroup), then the CDC shall abort the command with a status code of Zoning Data
Structure Locked.


624


NVM Express [®] Base Specification, Revision 2.2


The CDC may enforce access restrictions to the Zoning data structures. In this case, the CDC shall check
if the DDC issuing the FZL command is authorized to remove the ZoneGroup specified in the FZL data
(e.g., if the CDC allows access to a ZoneGroup only to the DDC that created that ZoneGroup, verify that
the ZoneGroup Originator field matches the NQN contained in the HOSTNQN field of the Connect
command sent from the DDC to that CDC). If that DDC is not authorized to access the specified ZoneGroup,
then the CDC shall abort the FZL command with a status code of ZoneGroup Originator Invalid.


**Pull Model DDC Operations**


**8.3.2.3.8.3.1 Get Active ZoneGroup (GAZ)**


The Get Active ZoneGroup (GAZ) operation allows a DDC to retrieve from the CDC an active ZoneGroup
associated with that DDC. For a pull model DDC the GAZ operation is mapped to a Pull Model DDC Request
asynchronous event notification (refer to Figure 152). The CDC responds to that asynchronous event
notification with a Get Log Page command requesting the Pull Model DDC Request log page (refer to
section 5.1.12.3.4), to which the DDC responds with a log page requesting a GAZ operation for a specified
ZoneGroup. The GAZ operation is then completed by the CDC by issuing one or more FZS commands to
send that ZoneGroup and the operation status to the DDC, as shown in Figure 706.


**Figure 706: GAZ for Pull Model DDC**


The format of the operation specific parameters of a Pull Model DDC Request log page requesting a GAZ
operation is shown in Figure 707.


**Figure 707: GAZ Operation Specific Parameters for Pull Model DDC Request Log Page**

|Bytes|Description|
|---|---|
|03:00|**Transaction ID (T_ID)**|
|227:04|**ZoneGroup Originator (ZGORIG)**|
|257:228|**ZoneGroup Name (ZGNAME)**|



The Transaction ID field is used to relate the Pull Model DDC Request log page for a pull model GAZ to the
subsequent FZS command(s). The Zoning Data Key in Command Dword 10 (refer to Figure 513) in the
FZS command(s) shall be set to the received Transaction ID value. The ZoneGroup definition is sent
through one or more subsequent FZS commands and is provided in the FZS buffer, as shown in Figure
708. The FZS command sending the last fragment shall have the Last Fragment (LF) bit set to ‘1’ in
Command Dword 12 (refer to Figure 515).


**Figure 708: FZS Data for Pull Model GAZ**

|Bytes|Description|
|---|---|
|00|**Operation Type (OTYP):** 7h (i.e., Get Active ZoneGroup for a pull model DDC)|



625


NVM Express [®] Base Specification, Revision 2.2


**Figure 708: FZS Data for Pull Model GAZ**

|Bytes|Description|
|---|---|
|03:01|Reserved|
|07:04|**GAZ Operation Status (GAZOS)**|
|11:08|**ZoneGroup Fragment Length (ZGFL)**|
|15:12|Reserved|
|ZGFL+15:16|**ZoneGroup Fragment (ZGF)**|



The GAZ Operation Status field is used to encode status information for the pull model GAZ operation, as
shown in Figure 716.


When a ZoneGroup is transferred in multiple fragments, if the CDC detects the ZoneGroup definition has
changed while sending the fragments, then the CDC shall issue an FZS command with a zero length
ZoneGroup fragment and GAZ operation status set to 5h (i.e., ZoneGroup Changed), and the GAZ
operation shall be aborted.


If the ZoneGroup indicated in the Pull Model DDC Request log page for a pull model GAZ operation does
not exist on the CDC, then the CDC shall issue an FZS command with a zero length ZoneGroup fragment
and GAZ operation status set to 2h (i.e., Zoning Data Structure Not Found), and the GAZ operation shall
be aborted.


If the ZoneGroup indicated in the Pull Model DDC Request log page for a pull model GAZ operation is
locked on the CDC (i.e., another administrative interface outside the scope of this specification is modifying
that ZoneGroup), then the CDC shall issue an FZS command with a zero length ZoneGroup fragment and
GAZ operation status set to 3h (i.e., Zoning Data Structure Locked), and the GAZ operation shall be
aborted.


If the ZoneGroup indicated in the Pull Model DDC Request log page for a pull model GAZ operation is not
locked on the CDC, then the CDC shall continue the GAZ operation by issuing one or more subsequent
FZS commands containing the fragments of the requested ZoneGroup. The last fragment shall specify GAZ
operation status cleared to 0h (i.e., Operation Successful), and the other fragments shall specify GAZ
operation status set to 1h (i.e., Operation in Progress).


The DDC shall not process received ZoneGroup information until the entire ZoneGroup (i.e., all of the
fragments of the ZoneGroup) is received.


The CDC may enforce access restrictions to the Zoning data structures. In this case, the CDC shall check
if the DDC requesting the GAZ operation is authorized to read the ZoneGroup indicated in Pull Model DDC
Request log page for Pull Model GAZ operation (e.g., if the CDC allows access to a ZoneGroup only to the
DDC that created that ZoneGroup, verify that the ZoneGroup Originator field matches the NQN contained
in the SUBNQN field of the Connect command sent from the CDC to that DDC). If that DDC is not authorized
to access the specified ZoneGroup, then the CDC shall issue an FZS command with a zero length
ZoneGroup fragment and GAZ operation status set to 4h (i.e., ZoneGroup Originator Invalid), and the GAZ
operation shall be aborted.


**8.3.2.3.8.3.2 Add/Replace Active ZoneGroup (AAZ)**


The Add/Replace Active ZoneGroup (AAZ) operation allows a DDC to add or replace in the CDC an active
ZoneGroup associated with that DDC. For a pull model DDC the AAZ operation is mapped to a Pull Model
DDC Request asynchronous event notification (refer to Figure 152). The CDC responds to that
asynchronous event notification with a Get Log Page command requesting the Pull Model DDC Request
log page (refer to section 5.1.12.3.4), to which the DDC responds with a log page requesting an AAZ
operation for a specified ZoneGroup. The AAZ operation is then completed by the CDC by issuing one or
more FZR commands to retrieve that ZoneGroup from the DDC, and one FZS command to provide an
operation status to the DDC, as shown in Figure 709.


626


NVM Express [®] Base Specification, Revision 2.2


**Figure 709: AAZ for Pull Model DDC**


The format of the operation specific parameters of a Pull Model DDC Request log page requesting an AAZ
is shown in Figure 710.


**Figure 710: AAZ Operation Specific Parameters for Pull Model DDC Request Log Page**

|Bytes|Description|
|---|---|
|03:00|**Transaction ID (T_ID)**|
|227:04|**ZoneGroup Originator (ZGORIG)**|
|257:228|**ZoneGroup Name (ZGNAME)**|



The Transaction ID field is used to relate the Pull Model DDC Request log page for a pull model AAZ
operation to the subsequent FZR and FZS command(s). The Zoning Data Key in Command Dword 10
(refer to Figure 507) of the FZR command(s) shall be set to the received Transaction ID value. The Zoning
Data Key in Command Dword 10 (refer to Figure 513) of the FZS command shall be set to the received
Transaction ID value.


If the specified ZoneGroup is locked on the CDC, then the AAZ operation shall be aborted by the CDC by
issuing one FZS command with AAZ operation status set to 3h (i.e., Zoning Data Structure Locked) to the
DDC. The Transaction ID value returned by the DDC in the Pull Model DDC Request log page for a pull
model AAZ operation shall be the same in the FZS command for this AAZ operation.


If the specified ZoneGroup:

  - does not exist in ZoneDBActive in that CDC; or

  - exists in ZoneDBActive in that CDC and is not locked by another administrative interface,


then the CDC shall lock the specified ZoneGroup in ZoneDBActive and complete the AAZ operation by
issuing one or more FZR commands to request from the DDC the ZoneGroup definition to add/replace,
followed by an FZS command to report status information to the DDC. The ZoneGroup definition is sent
through one or more FZR commands and is provided in the FZR buffer, as shown in Figure 711. The FZR
completion queue entry sending the last fragment shall have the Last Fragment (LF) bit set to ‘1’ in
Completion Queue Entry Dword 0 (refer to Figure 183).


627


NVM Express [®] Base Specification, Revision 2.2


**Figure 711: FZR Data for Pull Model AAZ**

|Bytes|Description|
|---|---|
|00|**Operation Type (OTYP):** 9h (i.e., Add/Replace Active ZoneGroup for a pull model DDC)|
|07:01|Reserved|
|11:08|**ZoneGroup Fragment Length (ZGFL)**|
|15:12|Reserved|
|ZGFL+15:16|**ZoneGroup Fragment (ZGF)**|



The CDC shall not process received ZoneGroup information until the entire ZoneGroup (i.e., all of the
fragments of the ZoneGroup) is received. Upon receiving the ZoneGroup information, the CDC shall update
that ZoneGroup in ZoneDBActive in that CDC, increment the ZoneGroup generation number, and issue an
FZS command with AAZ operation status cleared to 0h (i.e., Operation Successful) to the DDC.


The AAZ Operation Status is sent through the FZS command and is provided in the FZS buffer, as shown
in Figure 712.


**Figure 712: FZS Data for Pull Model AAZ**

|Bytes|Description|
|---|---|
|00|**Operation Type (OTYP):** Ah (i.e., AAZ status for a pull model DDC)|
|03:01|Reserved|
|07:04|**AAZ Operation Status (ZAAOS)**|



The AAZ Operation Status field is used to encode status information for the pull model AAZ operation, as
shown in Figure 716.


The CDC may enforce access restrictions to the Zoning data structures. In this case, the CDC shall check
if the DDC requesting the AAZ operation is authorized to write the ZoneGroup indicated in Pull Model DDC
Request log page for Pull Model AAZ operation (e.g., if the CDC allows access to a ZoneGroup only to the
DDC that created that ZoneGroup, verify that the ZoneGroup Originator field matches the NQN contained
in the SUBNQN field of the Connect command sent from the CDC to that DDC). If that DDC is not authorized
to access the specified ZoneGroup, then the CDC shall issue an FZS command with AAZ operation status
set to 4h (i.e., ZoneGroup Originator Invalid), and the AAZ operation shall be aborted.


**8.3.2.3.8.3.3 Remove Active ZoneGroup (RAZ)**


The Remove Active ZoneGroup (RAZ) operation allows a DDC to remove from the CDC an active
ZoneGroup associated with that DDC. For a pull model DDC the RAZ operation is mapped to a Pull Model
DDC Request asynchronous event notification (refer to Figure 152). The CDC responds to that
asynchronous event notification with a Get Log Page command requesting the Pull Model DDC Request
log page (refer to section 5.1.12.3.4), to which the DDC responds with a log page requesting an RAZ
operation for a specified ZoneGroup. The RAZ operation is then completed by the CDC by issuing one FZS
command to provide an operation status to the DDC, as shown in Figure 713.


628


NVM Express [®] Base Specification, Revision 2.2


**Figure 713: RAZ for Pull Model DDC**


The format of the operation specific parameters of a Pull Model DDC Request log page requesting an RAZ
operation is shown in Figure 714.


**Figure 714: RAZ Operation Specific Parameters for Pull Model DDC Request Log Page**

|Bytes|Description|
|---|---|
|03:00|**Transaction ID (T_ID)**|
|227:04|**ZoneGroup Originator (ZGORIG)**|
|257:228|**ZoneGroup Name (ZGNAME)**|



The RAZ operation is then completed by the CDC by issuing one FZS command to report status information
to the DDC. The Transaction ID field is used to relate the Pull Model DDC Request log page for a pull model
RAZ operation to the subsequent FZS command. The Zoning Data Key in Command Dword 10 (refer to
Figure 513) of the FZS command shall be set to the received Transaction ID value.


The RAZ Operation Status is sent through the FZS command and is provided in the FZS buffer, as shown
in Figure 715.


**Figure 715: FZS Data for Pull Model RAZ**

|Bytes|Description|
|---|---|
|00|**Operation Type (OTYP):** Ch (i.e., RAZ status for a pull model DDC)|
|03:01|Reserved|
|07:04|**RAZ Operation Status (RAZOS)**|



The RAZ Operation Status field is used to encode status information for the pull model RAZ operation, as
shown in Figure 716.


If the ZoneGroup indicated in the Pull Model DDC Request log page for a pull model RAZ operation does
not exist on the CDC, then the CDC shall issue an FZS command with RAZ operation status set to 2h (i.e.,
Zoning Data Structure Not Found), and the RAZ operation shall be aborted.


If the ZoneGroup indicated in the Pull Model DDC Request log page for a pull model RAZ operation is
locked on the CDC (i.e., another administrative interface is modifying that ZoneGroup), then the CDC shall
issue an FZS command with RAZ operation status set to 3h (i.e., Zoning Data Structure Locked), and the
RAZ operation shall be aborted


If the ZoneGroup indicated in the Pull Model DDC Request log page for a pull model RAZ operation is not
locked on the CDC, then the CDC shall continue the GAZ operation by removing the requested ZoneGroup


629


NVM Express [®] Base Specification, Revision 2.2


from ZoneDBActive in that CDC and by issuing one subsequent FZS command with RAZ operation status
cleared to 0h (i.e., Operation Successful).


The CDC may enforce access restrictions to the Zoning data structures. In this case, the CDC shall check
if the DDC requesting the RAZ operation is authorized to remove the ZoneGroup indicated in the Pull Model
DDC Request log page for Pull Model RAZ operation (e.g., if the CDC allows access to a ZoneGroup only
to the DDC that created that ZoneGroup, verify that the ZoneGroup Originator field matches the NQN
contained in the SUBNQN field of the Connect command sent from the CDC to that DDC). If that DDC is
not authorized to access the specified ZoneGroup, then the CDC shall issue an FZS command with RAZ
operation status set to 4h (i.e., ZoneGroup Originator Invalid), and the RAZ operation shall be aborted.


**8.3.2.3.8.3.4 Pull Model DDC Zoning Operations Status Values**


The Pull Model DDC Zoning operations status values are listed in Figure 716.


**Figure 716: Pull Model DDC Zoning Operations Status Values**

|Value|Definition|
|---|---|
|0h|Operation Successful|
|1h|Operation in Progress|
|2h|Zoning Data Structure Not Found|
|3h|Zoning Data Structure Locked|
|4h|ZoneGroup Originator Invalid|
|5h|ZoneGroup Changed|
|All others|Reserved|



**8.3.2.3.8.3.5 Pull Model DDC Discovery Log Page Request**


A Pull Model DDC retrieves a discovery log page from the CDC through a Pull Model DDC Request
asynchronous event notification (refer to Figure 152). The CDC responds to that asynchronous event
notification with a Get Log Page command requesting the Pull Model DDC Request log page (refer to
section 5.1.12.3.4), to which the DDC responds with a log page requesting a Discovery Log Page Request
operation. The Discovery Log Page Request operation is then completed by the CDC by issuing a SDLP
command (refer to section 5.1.20) to provide the requested discovery log page to the DDC, as shown in
Figure 717.


**Figure 717: Log Page Request Operation**


The format of the operation specific parameters of a Pull Model DDC Request log page requesting a Log
Page Request operation is shown in Figure 718.


630


NVM Express [®] Base Specification, Revision 2.2


**Figure 718: Log Page Request Operation Specific Parameters for Pull Model DDC Request Log**

**Page**

|Bytes|Description|
|---|---|
|00|**Log Page Request Log Page Identifier (LPRLID)**|
|01|**Log Page Request Log Specific Parameter (LPRLSP)**|
|03:02|Reserved|



The LPRLID field and the LPRLSP field have respectively the same format and semantics of the LID field
and the LSP field in Command Dword 10 of a Get Log Page command. For example, to retrieve the Host
Discovery log page, the LPRLID field is set to 71h.


**Asynchronous Events**


A Centralized Discovery controller (CDC) reports a Discovery Log Page Change Asynchronous Event
notification (Asynchronous Event Information field set to F0h) to each host that has requested
asynchronous event notifications of this type (refer to Figure 152) as specified in section 3.1.3.3.2 when a
Fabric Zoning configuration changes. In particular:

  - if a Zone member with the Role set to 2h (i.e., an NVM subsystem) is added or removed from a
Zone, then the CDC shall report an AEN to all Zone members of that Zone having the Role set to
1h (i.e., all hosts in that Zone);

  - if a Zone member with the Role set to 1h (i.e., a host) is added or removed from a Zone, then the
CDC shall report an AEN to all Zone members of that Zone having the Role set to 2h (i.e., all NVM
subsystems in that Zone); and

  - If a Zone is added or removed, then the CDC shall report an AEN to all Zone members of the added
or removed Zone.


**Exporting NVM Resources**


Exported Resource Management is a capability that may be supported in an NVM subsystem that only
contains controllers that use transports other than the Memory-Based Transport Model (e.g., the PCIe
transport).


Exporting an Underlying Namespace may be achieved by:

  - creating an Exported NVM Subsystem (refer to section 5.3.2);

  - assigning an Underlying Namespace to an Exported NVM Subsystem (refer to section 5.3.7.1.1);

  - attaching a transport to the Exported NVM Subsystem to enable remote access to the Exported
NVM Subsystem (refer to section 5.3.9.1.1); and

  - optionally assigning access control policies for the Exported NVM Subsystem (refer to sections
5.3.8.1.3 and 5.3.8.1.4).


Exported NVM Subsystems shall not expose information about Underlying NVM Subsystem resources or
entities that are not associated with Exported NVM Subsystem entities. This includes entities in Underlying
NVM Subsystems (e.g., NSID, NVM Set Identifiers, ANA Group Identifiers).


**Management of Exported NVM Resources (Informative)**


Commands for managing Exported NVM Resources are processed by a controller in an Underlying NVM
Subsystem.


This section describes example flows to manage Exported NVM Resources through the use of the:

  - Identify command with CNS set to 1Dh to retrieve the Underlying Namespace List;

  - Identify command with CNS set to 1Eh to retrieve the list of Underlying Ports that may be used to
export NVMe over Fabrics Subsystems;

  - Create Exported NVM Subsystem command to create an Exported NVM Subsystem;

  - Manage Exported NVM Subsystem command to manage access to an Exported NVM Subsystem;


631


NVM Express [®] Base Specification, Revision 2.2


  - Manage Exported Namespace command to configure an Exported NVM Subsystem with
namespaces;

  - Manage Exported Port command to manage fabric port configurations on an Exported NVM
Subsystem;

  - Manage Exported NVM Subsystem command to delete Exported NVM Subsystems; and

  - Clear Exported NVM Resource Configuration command to remove all configured Exported NVM
Resources.


**8.3.3.1.1** **Configuring an Exported NVM Subsystem**


Prior to configuring exported NVM resources and exposing them for access, an administrative entity (e.g.,
administrator, resource manager, orchestrator, administration console, centralized configuration manager)
must first determine what Underlying resources (e.g., namespaces, ports) are available; this may be
through a-priori knowledge or by using a Identify command with CNS set to 1Dh (refer to section 5.1.13.4.1
(refer to step ‘1’ in Figure 719, Figure 720, and in Figure 721) and Identify command with CNS set to 1Eh
(refer to section 5.1.13.4.2) (refer to step ‘2’ in Figure 719, Figure 720, and Figure 721). Figure 719 shows
collections of Underlying Namespaces and Underlying Ports and an empty collection of Exported NVM
resources.


**Figure 719: Example reference for retrieving Underlying Namespaces and Underlying Ports**






|NVMe<br>SSNDVM|Col2|Col3|Col4|
|---|---|---|---|
|NVMe<br>SSD<br>NVM|SSD<br>NVM|SSD<br>NVM|e|
|NVMe<br>SSD<br>NVM||SSD<br>NVM|SSD<br>NVM|



|NVM Storage<br>NVMe<br>Underlying Namespace<br>SSNDVMe<br>List<br>SSNDVMe<br>SSD<br>1<br>Underlying Namespace Underlying Namespace|NVM Storage<br>NVMe<br>SSNDVMe<br>SSNDVMe<br>SSD|
|---|---|
|**Underlying Namespace**|**Underlying Namespace**|


**Exported NVM resource collection**













Once the administrative entity has determined the available underlying resources (refer to step ‘1’ and step
‘2’ in Figure 719, Figure 720, and Figure 721), the administrative entity may create, configure, and expose
Exported NVM Subsystems. An example flow to configure an Exported NVM Subsystem:

  - Create an Exported NVM Subsystem by Issuing a Create Exported NVM Subsystem command
(refer to section 5.3.2) (refer to step ‘3’ in Figure 720 and Figure 721).


632


NVM Express [®] Base Specification, Revision 2.2


  - Associate individual Underlying Namespaces with an Exported NVM Subsystem by issuing a
Manage Exported Namespace command with an Associate Namespace operation (refer to section
5.3.7.1.1) (refer to step ‘4’ in Figure 720 and Figure 721).

  - Associate individual Underlying Ports with an Exported NVM Subsystem by issuing a Manage
Exported Port command with a Create operation (refer to section 5.3.9.1.1) (refer to step ‘5’ in
Figure 720 and Figure 721).


**Figure 720: Example reference for retrieving Underlying Namespaces and Underlying Ports**





























633


NVM Express [®] Base Specification, Revision 2.2


**Figure 721: Example steps for retrieving underlying resources and configuring an Exported**
**NVM Subsystem**

















**8.3.3.1.2** **Managing Host access to an Exported NVM Subsystem**


Exported NVM Subsystems are created with a specified Access Mode (i.e., restricted, unrestricted).


This section describes an example flow for changing an Exported NVM Subsystem configured for
unrestricted access to restricted access (where only hosts in the Allowed Host List associated to the
specified Exported NVM Subsystem have permissions to use the Exported Namespaces linked to that
Exported NVM Subsystem).


The access mode of Exported NVM Subsystems may be changed by issuing a Manage Exported NVM
Subsystem command with a Change Access Mode operation (refer to section 5.3.8.1.2) and specifying the
desired Access Mode (refer to step ‘6’ in Figure 722). The example Figure 722 shows changing the access
mode of an Exported NVM Subsystem to restricted access. The example Figure 722 also shows Exported
NVM Subsystem access to specific hosts (refer to step ‘7’ in Figure 722).


**Figure 722: Example steps for restricting access to an Exported NVM Subsystem to specific hosts**

|Controller<br>Administrator<br>6<br>7|Controller|Col3|
|---|---|---|
|Administrator|Administrator|Administrator|
|Administrator|Administrator||
||||



Similarly, hosts may be restricted from access to specified Exported NVM Subsystems configured for
restricted access, on specified ports, by issuing Manage Exported NVM Subsystem commands with the
Revoke Host Access operation (refer to section 5.3.8.1.4). Refer to step ‘8’ in Figure 723).


634


NVM Express [®] Base Specification, Revision 2.2


**Figure 723: Example steps for revoking specific hosts access to an Exported NVM Subsystem**









An example flow for removing an Exported NVM Subsystem and associated Namespaces would be issuing:


1. a Manage Exported NVM Port command with a Delete operation (refer to section 5.3.9.1.2) for
each port associated with the Exported NVM Subsystem to be removed (refer to step ‘9’ of Figure
724).
2. a Manage Exported Namespace command with a Disassociate Namespace operation (refer to
section 5.3.7.1.2) for each Exported Namespaces associated with the Exported NVM Subsystem
to be removed (refer to step ‘10’ of Figure 724).
3. a Manage Exported NVM Subsystem command with a Delete operation (refer to section 5.3.8.1.1)
of a Manage Exported NVM Subsystem command (refer to step ‘11’ of Figure 724).

|Figure 724: Example steps for removing an Exported NVM Subsystem|ystem|Col3|
|---|---|---|
|Administrator<br>Controller<br>10<br>9<br>11|Controller|Controller|
|Administrator|Administrator|Administrator|
|Administrator|Administrator||
||||



**8.3.3.1.3** **Clearing all Exported NVM Subsystems**


Issuing a Clear Exported NVM Resource Configuration command (refer to section 5.3.1) clears all Exported
NVM Subsystems (refer to Figure 725).

|Figure 725: Example steps for clearing all Exported NVM Subsystems|ems|Col3|
|---|---|---|
|Administrator<br>Controller|Controller|Controller|
|Administrator|Administrator|Administrator|
|Administrator|Administrator||
||||



Upon successful completion of a Clear Exported NVM Resource Configuration command there are no
Exported NVM Subsystems.


**NVMe over Fabrics Secure Channel and In-band Authentication**


NVMe over Fabrics supports both fabric secure channel (that includes authentication) and NVMe in-band
authentication. Fabric authentication is part of establishing a fabric secure channel via an NVMe Transport


635


NVM Express [®] Base Specification, Revision 2.2


specific protocol that provides authentication, encryption, and integrity checking (e.g., IPsec; refer to RFC
4301 or TLS; refer to RFC 8446). NVMe in-band authentication is performed immediately after a Connect
command (refer to section 6.3) succeeds using the Authentication Send and Authentication Receive
commands (refer to section 6.1 and section 6.2) to tunnel authentication protocol commands between the
host and the controller.


Enrollment of the host and controller in an authentication mechanism, including provisioning of
authentication credentials to the host and controller, is outside the scope of this specification.


If both fabric secure channel and NVMe in-band authentication are used, the identities for these two
instances of authentication may differ for the same NVMe Transport connection. For example, if an iWARP
NVMe Transport is used with IPsec as the fabric secure channel technology, the IPsec identities for
authentication are associated with the IP network (e.g., DNS host name or IP address), whereas NVMe inband authentication uses NVMe identities (i.e., Host NQNs). The NVMe Transport binding specification
may provide further guidance and requirements on the relationship between these two identities, but
determination of which NVMe Transport identities are authorized to be used with which NVMe identities is
part of the security policy for the deployed NVM subsystem.


**Fabric Secure Channel**


The Transport Requirements field in the Fabrics Discovery Log Page Entry (refer to Figure 295) indicates
whether a fabric secure channel shall be used for an NVMe Transport connection to an NVM subsystem.
The secure channel mechanism is specific to the type of fabric.


If establishment of a secure channel fails or a secure channel is not established when required by the
controller, the resulting errors are fabric-specific and may not be reported to the NVMe layer on the host.
Such errors may result in the controller being inaccessible to the host via the NVMe Transport connection
on which the failure to establish a fabric secure channel occurred.


An NVM subsystem that requires use of a fabric secure channel (i.e., as indicated by the TSC field in the
associated Discovery Log Page Entry) shall not allow capsules to be transferred until a secure channel has
been established for the NVMe Transport connection.


All Discovery Log Page Entries for an NVM subsystem should report the same value of TREQ to each host.
Discovery Log Page Entries for an NVM subsystem may report different values of TREQ to different hosts.


Figure 726 shows an example of secure channel establishment using TLS, the fabric secure channel
protocol for NVMe/TCP.


**Figure 726: Example of TLS secure channel establishment**


Host Controller









An NVMe/TCP-TLS transport session is
1.
established


The Connect exchange is performed to set up an
2.
NVMe Queue and associate host to controller


Secure channel and Queue are set up, ready
3.
for subsequent operations


636




NVM Express [®] Base Specification, Revision 2.2


**NVMe In-band Authentication**


The Authentication and Security Requirements (AUTHREQ) field in the Connect response capsule (refer
to Figure 548) indicates whether NVMe in-band authentication is required.


If one or more of the bits in the AUTHREQ field are set to ‘1’, then the controller requires that the host
authenticate on that queue in order to proceed with Fabrics, Admin, and I/O commands. Authentication
success is defined by the specific security protocol that is used for authentication. If any command other
than Connect, Authentication Send, or Authentication Receive is received prior to authentication success,
then the controller shall abort the command with Authentication Required status.


If all bits in the AUTHREQ field are cleared to ‘0’, then the controller does not require the host to
authenticate, and the NVM subsystem shall not abort any command with a status code value of
Authentication Required.


Refer to section 8.3.4.2.1 for considerations on Discovery subsystems.


The host may initiate a subsequent authentication transaction at any time for reauthentication purposes.
Initiating reauthentication shall not invalidate a prior authentication. If the reauthentication transaction
concludes with the controller sending an AUTH_Failure1 message (refer to section 8.3.4.4.2), then the
controller shall terminate all commands with a status code of Operation Denied and disconnect the NVMe
over Fabrics connection. If the reauthentication transaction concludes with the host sending an
AUTH_Failure2 message, then the host shall disconnect the NVMe over Fabrics connection.


The state of an in-progress authentication transaction is soft-state. If the subsequent command in an
authentication transaction is not received by the controller within a timeout equal to:

  - the Keep Alive Timeout value (refer to Figure 546), if the Keep Alive Timer is enabled; or

  - the default Keep Alive Timeout value (i.e., two minutes), if the Keep Alive Timer is disabled;


then the authentication transaction has timed out and the controller should discard the authentication
transaction state (including the T_ID value, refer to section 8.3.4.4.1).


For an initial authentication, an authentication transaction timeout should be treated as an authentication
failure with termination of the transport connection. For reauthentication, an authentication transaction
timeout should not be treated as an authentication failure. Authentication commands used to continue that
transaction after an authentication transaction timeout should be aborted with a status code of Command
Sequence Error.


Figure 727 shows an example of authentication transaction for NVMe/TCP.


**Figure 727: Example of authentication transaction for NVMe/TCP**


Host Controller









1. An NVMe/TCP transport session is established


The Connect exchange is performed to set up an
2.
NVMe Queue and associate host to controller


The host performs an authentication transaction
3.
with the controller to authenticate the end-points


4. Queue is set up, ready for subsequent operations


637






NVM Express [®] Base Specification, Revision 2.2


**8.3.4.2.1** **Special considerations for In-band Authentication of Discovery subsystems**


Hosts that have been configured to authenticate Discovery subsystems with an in-band authentication
protocol that supports both unidirectional authentication and bidirectional authentication (e.g., DH-HMACCHAP, refer to section 8.3.4.5) should behave as follows:

  - If the host connected to a Discovery subsystem using the well-known Discovery Service NQN (i.e.,
nqn.2014-08.org.nvmexpress.discovery) and the Discovery subsystem did not request
authentication, then the host should not perform an authentication transaction;

  - If the host connected to a Discovery subsystem using the well-known Discovery Service NQN (i.e.,
nqn.2014-08.org.nvmexpress.discovery) and the Discovery subsystem requested authentication,
then the host should perform only unidirectional authentication (i.e., the Discovery subsystem may
authenticate the host, but the host should not authenticate the well-known Discovery Service NQN);
or

  - If the host connected to a Discovery subsystem using the unique Discovery Service NQN for that
Discovery subsystem (refer to section 3.1.3.3), regardless of whether the Discovery subsystem
requested authentication, then the host may perform unidirectional authentication or bidirectional
authentication (i.e., the host may authenticate the unique Discovery Service NQN for that Discovery
subsystem).


Figure 728 illustrates a process that a host is able to use to retrieve the unique Discovery Service NQN and
perform in-band authentication for a Discovery subsystem if that host has been configured to authenticate
Discovery subsystems and the Discovery subsystem that the host connects to also requires authentication
(i.e., the AUTHREQ field is not cleared to zero) using DH-HMAC-CHAP for authentication. This process
includes:


1. connect to the Discovery subsystem using the well-known Discovery Service NQN (i.e., nqn.201408.org.nvmexpress.discovery);
2. perform unidirectional authentication with the Discovery subsystem;
3. perform controller initialization (refer to section 3.5);
4. retrieve the unique Discovery Service NQN (refer to section 3.1.3.3);
5. perform controller shutdown (refer to section 3.6);
6. reconnect to the Discovery subsystem using the unique Discovery Service NQN for that Discovery
subsystem; and
7. perform bidirectional authentication with the Discovery subsystem using the unique Discovery
Service NQN for that Discovery subsystem.


638


NVM Express [®] Base Specification, Revision 2.2


**Figure 728: Unique Discovery Service NQN retrieval for bidirectional authentication**



























**8.3.4.2.2** **NVMe In-band Authentication Protocol-Specific Requirements**


Authentication requirements for security commands are based on the security protocol indicated by the
SECP field in the command.


The authentication protocols defined by this specification use the security protocol identifier E9h (assigned
to NVMe by SPC-5, a SCSI standard). The messages of the defined authentication protocols are selfidentifying, therefore the SPSP0 field and the SPSP1 field of the Authentication Send and Authentication
Receive commands shall be set to 01h. Authentication messages are mapped to NVMe over Fabrics
command and response pairs. The mapping of authentication messages to the Authentication Send
command is shown in Figure 729.


**Figure 729: Mapping of authentication messages to the Authentication Send command**

|1<br>Field|Value|
|---|---|
|**SPSP0**|01h|
|**SPSP1**|01h|
|**SECP**|E9h|



639


NVM Express [®] Base Specification, Revision 2.2


**Figure 729: Mapping of authentication messages to the Authentication Send command**

|1<br>Field|Value|
|---|---|
|**TL**|Specifies the amount of data to transfer in bytes|
|Notes:<br>1.<br>Refer to section 6.2.|Notes:<br>1.<br>Refer to section 6.2.|



The mapping of authentication messages to the Authentication Receive command is shown in Figure 730.
Security processing requirements associated with the Authentication Receive command (e.g., delays in
third-party authentication verification) may result in delays in controller completion of an Authentication
Receive command. The host should consider these possible delays associated with the Authentication
Receive command.


**Figure 730: Mapping of authentication messages to the Authentication Receive command**

|1<br>Field|Value|
|---|---|
|**SPSP0**|01h|
|**SPSP1**|01h|
|**SECP**|E9h|
|**AL**|Specifies the amount of data to transfer in bytes2|
|Notes:<br>1.<br>Refer to section 6.1.<br>2.<br>The size of the largest authentication message that could be received.|Notes:<br>1.<br>Refer to section 6.1.<br>2.<br>The size of the largest authentication message that could be received.|



**Secure Channel Concatenation**


It is possible to leverage an authentication transaction to generate shared key material to use as pre-shared
key (PSK) to establish a secure channel (e.g., with IPsec or TLS). This PSK is generated by an
authentication transaction on an Admin Queue over an unsecure channel. Once the authentication
transaction is completed, that Admin Queue transport connection shall be disconnected by the host. The
generated PSK may then be used to set up secure channels for subsequent Admin Queue(s) and I/O
Queues.


The process of generating a PSK on an Admin Queue over an insecure channel, disconnecting that Admin
Queue transport connection, and setting up an Admin Queue over a secure channel established using that
generated PSK is called secure channel concatenation. Figure 731 shows an example of this process for
TLS with NVMe/TCP, where steps 1 to 7 show TLS secure channel concatenation for the Admin Queue
and steps 8 to 13 show the setup of TLS secure channels for the I/O Queues.


640


NVM Express [®] Base Specification, Revision 2.2


**Figure 731: Example of TLS secure channel concatenation with NVMe/TCP**


1. An NVMe/TCP transport session is established





2. The Connect exchange is performed to set up an
Admin Queue and associate host to controller


3. An authentication transaction generating a PSK
between host and controller is performed


4. The NVMe/TCP transport session is disconnected


5. An NVMe/TCP-TLS transport session is established
using the generated PSK


6. The Connect exchange is performed to set up an
Admin Queue and associate host to controller


7. Secure channel and Queue are set up


8. An NVMe/TCP-TLS transport session is established
using the generated PSK


9. The Connect exchange is performed to set up the
first I/O Queue of the established association


10. Secure channel and Queue are set up


11. An NVMe/TCP-TLS transport session is established

using the generated PSK


12. The Connect exchange is performed to set up the

Nth I/O Queue of the established association


13. Secure channel and Queue are set up



























Secure channel concatenation is prohibited over any secure channel that has been established in
compliance with the requirements of an NVMe transport specification (e.g., the NVM Express TCP
Transport Specification). The controller response to a host that requests secure channel concatenation in
this situation is specified in section 8.3.4.4.1. In contrast, replacing a PSK for such a secure channel is
permitted (refer to section 8.3.4.4.1.


**Common Authentication Messages**


**8.3.4.4.1** **AUTH_Negotiate Message**


The AUTH_Negotiate message is sent from the host to the controller and is used to indicate the
authentication protocols the host is able to use in this authentication transaction and which secure channel
protocol, if any, to concatenate to this authentication transaction. The AUTH_Negotiate message format is
shown in Figure 732.


641


NVM Express [®] Base Specification, Revision 2.2


**Figure 732: AUTH_Negotiate message format**

|Bytes|Description|
|---|---|
|0|**Authentication Type (AUTH_TYPE):**00h (i.e., common messages)|
|1|**Authentication Identifier (AUTH_ID):**00h (i.e., AUTH_Negotiate)|
|3:2|Reserved|
|5:4|**Transaction Identifier (T_ID):**16-bit transaction identifier|
|6|**Transaction Identifier (SC_C)**|
|7|**Number of Authentication Protocol Descriptors (NAPD):** This field<br>specifies the number of Authentication Protocol Descriptors are in the<br>Authentication Protocol Descriptor list.|
|**Authentication Protocol Descriptor List**|**Authentication Protocol Descriptor List**|
|71:8|**Authentication Protocol Descriptor 1**|
|135:72|**Authentication Protocol Descriptor 2**|
|…|…|
|NAPD*64+7:(NAPD-1)*64+8|**Authentication Protocol Descriptor NAPD**|



The SC_C field determines if a secure channel concatenation to the authentication transaction is requested
and with which secure channel protocol, as shown in Figure 733.


**Figure 733: Secure channel protocol identifiers**









|Value|Definition|Transport<br>Applicability|
|---|---|---|
|00h|**NOSC:** No secure channel concatenation|n/a|
|01h|Obsolete (refer to NVM Express Base Specification 2.0)||
|02h|**NEWTLSPSK:** Used on an Admin Queue over a TCP channel without TLS to<br>generate a PSK and associated PSK identity. This {PSK, PSK Identity} pair may be<br>used to set up TLS secure channels for subsequent Admin and I/O queues.|TCP|
|03h|**REPLACETLSPSK:** Used on an Admin Queue over a TLS secure channel to<br>generate a PSK and associated PSK identity. This {PSK, PSK Identity} pair replaces<br>the {PSK, PSK Identity} pair that was used to set up the TLS secure channel over<br>which the authentication transaction is performed.|TCP with TLS|
|All other<br>values|Reserved||


An authentication transaction with the SC_C field set to NOSC is allowed on any Admin or I/O Queue and
does not generate a PSK (i.e., it performs authentication only).


An authentication transaction with the SC_C field set to NEWTLSPSK:

  - is allowed on an Admin Queue over a TCP channel without TLS and generates a new PSK;

  - is prohibited on an I/O Queue over a TCP channel without TLS; and

  - is prohibited on an Admin Queue or I/O queue over a TLS secure channel.


An authentication transaction with the SC_C field set to REPLACETLSPSK:

  - is allowed on an Admin Queue over a TLS secure channel and replaces the association’s PSK;

  - is prohibited on an Admin Queue or I/O queue over a TCP channel without TLS; and

  - is prohibited on an I/O Queue over a TLS secure channel.


The AUTH_Negotiate message is structured as a list of 64-byte authentication protocol descriptors to
enable extensibility to define additional authentication protocols. Currently only one authentication protocol
is defined (i.e., DH-HMAC-CHAP), therefore the AUTH_Negotiate message carries only one authentication
protocol descriptor (i.e., NAPD=1). Implementations should support more than one descriptor to enable
protocol extensibility. The first byte of an authentication protocol descriptor identifies the specific
authentication protocol, as shown in Figure 734.


642


NVM Express [®] Base Specification, Revision 2.2


**Figure 734: Authentication protocol identifiers**

|Value|Definition|
|---|---|
|01h|DH-HMAC-CHAP (refer to section 8.3.4.5)|
|All other values|Reserved|



Upon receiving an AUTH_Negotiate message, if the SC_C value indicated by the host:

  - does not satisfy the security requirements of the controller (e.g., the host did not request secure
channel concatenation, but the controller’s security configuration requires secure channel
concatenation);

  - is prohibited for the Admin Queue or I/O Queue via which the AUTH_Negotiate message was
received, as specified in this section; or

  - requests secure channel concatenation and that value is contained in an AUTH_Negotiate
message received over a secure channel established in compliance with the requirements of an
NVMe transport specification (e.g., the NVM Express TCP Transport Specification),


then the controller shall:

  - reply to the AUTH_Negotiate message with an AUTH_Failure1 message having reason code
‘Authentication failure’ and reason code explanation ‘Secure channel concatenation mismatch’; and

  - disconnect the NVMe over Fabrics connection upon transmitting the AUTH_Failure1 message.


Upon receiving an AUTH_Negotiate message, if the protocol descriptors proposed by the host do not satisfy
the security requirements of the controller, then the controller shall:

  - reply to the AUTH_Negotiate message with an AUTH_Failure1 message having reason code
‘Authentication failure’ and reason code explanation ‘Authentication protocol not usable’; and

  - disconnect the NVMe over Fabrics connection upon transmitting the AUTH_Failure1 message.


**8.3.4.4.2** **AUTH_Failure Messages**


The AUTH_Failure1 message is sent from the controller to the host, the AUTH_Failure2 message is sent
from the host to the controller. The format of the AUTH_Failure1 message and of the AUTH_Failure2
message is shown in Figure 735.


**Figure 735: AUTH_Failure1 and AUTH_Failure2 message format**

|Bytes|Description|
|---|---|
|0|**Authentication Type (AUTH_TYPE):** 00h (i.e., common messages)|
|1|**Authentication Identifier (AUTH_ID):**<br>F0h (i.e., AUTH_Failure2)<br>F1h (i.e., AUTH_Failure1)|
|3:2|Reserved|
|5:4|**Transaction Identifier (T_ID):** 16-bit transaction identifier|
|6|**Reason Code (RCODE)**|
|7|**Reason Code Explanation (RCODEEX)**|



The AUTH_Failure reason codes are listed in Figure 736.


**Figure 736: AUTH_Failure reason codes**

|Value|Definition|
|---|---|
|01h|**Authentication failure:** The authentication transaction failed|
|All other values|Reserved|



The AUTH_Failure reason code explanations are listed in Figure 737.


643


NVM Express [®] Base Specification, Revision 2.2


**Figure 737: AUTH_Failure reason code explanations**

|Value|Definition|
|---|---|
|01h|**Authentication failed:** Authentication of the involved host or NVM subsystem failed.|
|02h|**Authentication protocol not usable:** The protocol descriptors proposed by the host do not<br>satisfy the security requirements of the controller (refer to section 8.3.4.4.1).|
|03h|**Secure channel concatenation mismatch:** The SC_C value indicated by the host does not<br>satisfy the security requirements of the controller (refer to section 8.3.4.4.1).|
|04h|**Hash function not usable:** The HashIDList proposed by the host does not satisfy the security<br>requirements of the controller (refer to section 8.3.4.5.2).|
|05h|**DH group not usable:** The DHgIDList proposed by the host does not satisfy the security<br>requirements of the controller (refer to section 8.3.4.5.2).|
|06h|**Incorrect payload:** The payload of the received message is not correct.|
|07h|**Incorrect protocol message:** The received message is not the expected next message in the<br>authentication protocol sequence.|
|All other values|Reserved|



**8.3.4.4.3** **Mapping of Common Authentication Messages to Authentication Commands**


The AUTH_Negotiate message and the AUTH_Failure2 message are sent from the host to the controller,
therefore they are mapped to the Authentication Send command. The AUTH_Failure1 message is sent
from the controller to the host, therefore it is mapped to the Authentication Receive command.


**DH-HMAC-CHAP Protocol**


**8.3.4.5.1** **Protocol Operations**


DH-HMAC-CHAP is a key based Authentication and key management protocol that uses the Challenge
Handshake Authentication Protocol (CHAP, refer to RFC 1994) enhanced to use the Hashed Message
Authentication Code (HMAC) mechanism (refer to RFC 2104) with stronger hash functions and augmented
with an optional Diffie-Hellman (DH) exchange (refer to RFC 2631, clause 2.2.1). DH-HMAC-CHAP
provides bidirectional or unidirectional Authentication between a host and a controller.


The Diffie-Hellman part of the protocol is optional. When the Diffie-Hellman part of the protocol is not used,
DH-HMAC-CHAP is referred to as HMAC-CHAP. If insufficiently random keys are used (refer to section
8.3.4.5.7), HMAC-CHAP potentially allows a passive eavesdropper to discover the key through an off-line
dictionary attack, so its usage should be minimized. DH-HMAC-CHAP provides strong protection from
passive eavesdroppers. However, an active attacker could reduce the operation of this protocol so that only
HMAC-CHAP is used, and as a result gain sufficient information to mount an off-line dictionary attack on
the HMAC-CHAP key.


An implementation that supports DH-HMAC-CHAP authentication shall support DH-HMAC-CHAP with a
NULL DH exchange. All implementations of DH-HMAC-CHAP shall be configurable to require a DH
exchange (i.e., to not use HMAC-CHAP).


In order to authenticate with the DH-HMAC-CHAP protocol, each host and NVM subsystem shall be
provided with a DH-HMAC-CHAP key that is associated with the entity’s NQN. Two entities may
impersonate one another if they have the same key, therefore when the assigned keys are not different for
each entity there is a security vulnerability (refer to section 8.3.4.5.7).


To authenticate another entity, an entity is required to either:


a) know the key associated with the entity to be authenticated; or
b) rely on a third party that knows the key to verify the authentication (refer to section 8.3.4.5.11).


An example of a DH-HMAC-CHAP authentication transaction is shown in Figure 738, with the notation
shown in Figure 739. The DH-HMAC-CHAP_Success2 message that is shown as a dashed line is used
only for bidirectional authentication.


644


NVM Express [®] Base Specification, Revision 2.2


**Figure 738: Example of DH-HMAC-CHAP authentication transaction**


Host Controller


**Figure 739: Mathematical notations for DH-HMAC-CHAP**

|Symbols|Description|
|---|---|
|NQNc, NQNh|NQN of the NVM subsystem that contains the controller and NQN of the host|
|Kc, Kh|DH-HMAC-CHAP key of the NVM subsystem that contains the controller and<br>DH-HMAC-CHAP key of the host|
|p, g|Modulus (p) and generator (g) of the chosen DH group (refer to Figure 742)|
|x, y|Random numbers used as exponents in a DH exchange|
|C1, C2|Random challenge values|
|Ca1, Ca2|Augmented challenge values|
|S1, S2|32-bit sequence numbers|
|R1, R2|Reply values|
|T_ID|Authentication transaction identifier|
|SC_C|Secure channel concatenation indication|
|H( )|One-way hash function (refer to Figure 741)|
|HMAC(K, Str)|HMAC function (refer to RFC 2104) with key K on string Str using hash function H( )|
||||Concatenation operation|
|KS|Session key|



When used with a non-NULL DH exchange, the DH-HMAC-CHAP protocol is able to generate a session
key KS to be used to establish a TLS session between host and controller (refer to section 8.3.4.5.9).


645


NVM Express [®] Base Specification, Revision 2.2


For an NVM subsystem, the controller is the entity running the protocol, using the identity and credentials
of the NVM subsystem. The DH-HMAC-CHAP protocol proceeds in the following order:


1) The authentication transaction shall begin with the host sending the common AUTH_Negotiate

message to negotiate the authentication protocol to use and its associated parameters (refer to
section 8.3.4.4.1). The AUTH_Negotiate message carries the transaction identifier (T_ID) for the
entire authentication transaction and the list of authentication protocol descriptors for the
authentication protocols that may be used in this authentication transaction. For DH-HMAC-CHAP,
the authentication protocol descriptor includes the list of hash functions (HashIDList) and DiffieHellman group identifiers (DHgIDList) that may be used in this authentication protocol transaction.
2) If the parameters of the received DH-HMAC-CHAP protocol descriptor are compatible with the

controller’s policies, then the controller shall reply with a DH-HMAC-CHAP_Challenge message
(refer to section 8.3.4.5.3) carrying the same transaction identifier value (T_ID) received in the
AUTH_Negotiate message, the identifiers of the hash function (HashID) and the DH group (DHgID)
selected for use among the ones proposed by the host in the AUTH_Negotiate message, a
sequence number (S1), a random challenge value (C1), and the DH exponential (g [x] mod p). If the
controller selects a NULL DH group identifier, then the DH portion of the DH-HMAC-CHAP protocol
shall not be used, and the protocol reduces to a HMAC-CHAP transaction.
3) If the received DH-HMAC-CHAP_Challenge message is valid, then the host shall send a DH
HMAC-CHAP_Reply message (refer to section 8.3.4.5.11) carrying the same transaction identifier
value (T_ID), the response R1 to the challenge value C1, and its own DH exponential (g [y] mod p).
The DH Value Length shall be cleared to 0h if the controller has sent a NULL DH group identifier
in the DH-HMAC-CHAP_Challenge message. If bidirectional authentication is requested, then the
DH-HMAC-CHAP_Reply message shall carry also a sequence number S2 and a random challenge
value C2 that differs from the challenge value C1 received in the DH-HMAC-CHAP_Challenge
message.
4) If the authentication verification by the controller succeeds, then the controller shall reply with a

DH-HMAC-CHAP_Success1 message (refer to section 8.3.4.5.5) carrying the same transaction
identifier value (T_ID). If bidirectional authentication was requested, then the DH-HMACCHAP_Success1 message shall also carry the response R2 to the challenge value C2. If the
authentication verification fails, then the controller shall send an AUTH_Failure1 message and
disconnect the NVMe over Fabrics connection upon transmitting it.
5) The authentication transaction ends here, unless bidirectional authentication has been requested.

In this case, as shown by the dashed arrow in Figure 738, if the authentication verification by the
host succeeds, then the host shall send a DH-HMAC-CHAP_Success2 message (refer to section
8.3.4.5.6) carrying the same transaction identifier value (T_ID). If the authentication verification
fails, then the host shall send an AUTH_Failure2 message and disconnect the NVMe over Fabrics
connection upon transmitting it.


If the controller receives a message that is not the expected next message in the DH-HMAC-CHAP protocol
sequence, then the controller shall:


  - reply with an AUTH_Failure1 message having reason code ‘Authentication failure’ and reason code
explanation ‘Incorrect protocol message’; and

  - disconnect the NVMe over Fabrics connection upon transmitting the AUTH_Failure1 message.


If the host receives a message that is not the expected next message in the DH-HMAC-CHAP protocol
sequence, then the host shall:


  - reply with an AUTH_Failure2 message having reason code ‘Authentication failure’ and reason code
explanation ‘Incorrect protocol message’; and

  - disconnect the NVMe over Fabrics connection upon transmitting the AUTH_Failure2 message.


The payload format of a message shall be validated before performing any other security computation.


**8.3.4.5.2** **DH-HMAC-CHAP Authentication Protocol Descriptor**


The authentication protocol descriptor for DH-HMAC-CHAP (refer to section 8.3.4.4.1) is shown in Figure
740.


646


NVM Express [®] Base Specification, Revision 2.2


**Figure 740: Authentication protocol descriptor for DH-HMAC-CHAP**

|Bytes|Description|
|---|---|
|0|**Authentication Protocol Identifier (AuthID):**(01h for DH-HMAC-CHAP)|
|1|Reserved|
|2|**HashIDList Length (HALEN):**Number of hash function identifiers (1 to 30)|
|3|**DHgIDList Length (DHLEN):**Number of Diffie-Hellman group identifiers (1 to 30)|
|3+HALEN:4|**Hash Function Identifier List (HashIDList):** Array of hash function identifiers (one byte per<br>identifier)|
|33:4+HALEN|**Pad (PAD):**Padding bytes cleared to 0h, if present|
|33+DHLEN:34|**Diffie-Hellman Group Identifier List (DHgIDList):**Array of Diffie-Hellman Group identifiers (one<br>byte per identifier)|
|63:34+DHLEN|**Pad1 (PAD1):**Padding bytes cleared to 0h, if present|



The one-way hash functions used by DH-HMAC-CHAP are shown in Figure 741.


**Figure 741: DH-HMAC-CHAP hash function identifiers**

|Identifier|Hash Function|Hash Length (bytes)|1<br>Hash Block Size (bytes)|Reference|
|---|---|---|---|---|
|00h|Reserved|Reserved|Reserved|Reserved|
|01h|SHA-256|32|64|RFC 6234|
|02h|SHA-384|48|128|RFC 6234|
|03h|SHA-512|64|128|RFC 6234|
|04h-DFh|Reserved|Reserved|Reserved|Reserved|
|E0h-FEh|Vendor specific|Vendor specific|Vendor specific|Vendor specific|
|FFh|Reserved|Reserved|Reserved|Reserved|
|Notes:<br>1.<br>The hash block size is used by the HMAC calculation|Notes:<br>1.<br>The hash block size is used by the HMAC calculation|Notes:<br>1.<br>The hash block size is used by the HMAC calculation|Notes:<br>1.<br>The hash block size is used by the HMAC calculation|Notes:<br>1.<br>The hash block size is used by the HMAC calculation|



The SHA-256 hash function shall be supported. Use of the SHA-256 hash function may be prohibited by
the requirements of security policies that are not defined by NVM Express (e.g., CNSA 1.0 requires use of
SHA-384).


Upon receiving an AUTH_Negotiate message, if the HashIDList proposed by the host does not satisfy the
security requirements of the controller (e.g., the host proposed SHA-256, but the controller’s security policy
requires a SHA-384 hash), then the controller shall:

  - reply to the AUTH_Negotiate message with an AUTH_Failure1 message having reason code
‘Authentication failure’ and reason code explanation ‘Hash function not usable’; and

  - disconnect the NVMe over Fabrics connection upon transmitting the AUTH_Failure1 message.


The Diffie-Hellman (DH) groups used by DH-HMAC-CHAP are shown in Figure 742.


**Figure 742: DH-HMAC-CHAP Diffie-Hellman group identifiers**

|Identifier|DH group size|Generator (g)|Modulus (p) and Reference|
|---|---|---|---|
|00h|NULL|n/a|n/a|
|01h|2048-bit|2|refer to RFC 7919|
|02h|3072-bit|2|refer to RFC 7919|
|03h|4096-bit|2|refer to RFC 7919|
|04h|6144-bit|2|refer to RFC 7919|
|05h|8192-bit|2|refer to RFC 7919|
|06h-DFh|Reserved|Reserved|Reserved|
|E0h-FEh|Vendor specific|Vendor specific|Vendor specific|
|FFh|Reserved|Reserved|Reserved|



The 00h identifier indicates that no Diffie-Hellman exchange is performed, which reduces the DH-HMACCHAP protocol to the HMAC-CHAP protocol. The 00h identifier shall not be proposed in an


647


NVM Express [®] Base Specification, Revision 2.2


AUTH_Negotiate message that requests secure channel concatenation (i.e., with the SC_C field set to a
non-zero value).


The 2048-bit DH group and the 3072-bit DH group shall be supported. A mechanism shall be provided to
disable (i.e., prohibit) use of the 2048-bit DH group. Use of the 2048-bit DH group may be prohibited by the
requirements of security policies that are not defined by NVM Express (e.g., CNSA 1.0 requires use of a
3072-bit or larger DH group).


Upon receiving an AUTH_Negotiate message, if the DHgIDList proposed by the host:

  - does not satisfy the security requirements of the controller (e.g., the host proposed only the NULL
DH group, but the controller’s security policy requires a DH group whose size is 3072-bit or larger);
or

  - contains the NULL DH group (i.e., identifier 00h) and the AUTH_Negotiate message is requesting
secure channel concatenation (i.e., with the SC_C field set to a non-zero value),


then the controller shall:

  - reply to the AUTH_Negotiate message with an AUTH_Failure1 message having reason code
‘Authentication failure’ and reason code explanation ‘DH group not usable’; and

  - disconnect the NVMe over Fabrics connection upon transmitting the AUTH_Failure1 message.


**8.3.4.5.3** **DH-HMAC-CHAP_Challenge Message**


The DH-HMAC-CHAP_Challenge message is sent from the controller to the host. The format of the DHHMAC-CHAP_Challenge message is shown in Figure 743.


**Figure 743: DH-HMAC-CHAP_Challenge message format**

|Bytes|Description|
|---|---|
|0|**Authentication Type (AUTH_TYPE):**01h (i.e., DH-HMAC-CHAP)|
|1|**Authentication Identifier (AUTH_ID):**01h (i.e., DH-HMAC-CHAP_Challenge)|
|3:2|Reserved|
|5:4|**Transaction Identifier (T_ID):**16-bit transaction identifier|
|6|**Hash Length (HL):**Length in bytes of the selected hash function|
|7|Reserved|
|8|**Hash Identifier (HashID):** Identifier of selected hash function|
|9|**Diffie-Hellman Group Identifier (DHgID):** Identifier of selected Diffie-Hellman group|
|11:10|**DH Value Length (DHVLEN):** Length in bytes of DH value. If no DH value is included<br>in the message, then this field is cleared to 0h|
|15:12|**Sequence Number (SEQNUM):** Sequence number S1|
|15+HL:16|**Challenge Value (CVAL):** Challenge C1|
|15+HL+DHVLEN:16+HL|**DH Value (DHV):** DH exponential gx mod p. This field is not present (i.e., the CVAL field<br>is the last field in the message) if DHVLEN is cleared to 0h|



**Hash Length (HL):** Shall be set to the length in bytes of the selected hash function, as specified in Figure
741.


**HashID:** Shall be set to the hash function identifier (refer to Figure 741) selected for this authentication
transaction among those proposed in the DH-HMAC-CHAP protocol descriptor in the AUTH_Negotiate
message. The controller shall select a hash function in accord with its applicable policy.


**DHgID:** Shall be set to the DH group identifier (refer to Figure 743) selected for this authentication
transaction among those proposed in the DH-HMAC-CHAP protocol descriptor in the AUTH_Negotiate
message. The controller shall select a DH group identifier in accord with its applicable policy. If this field is
cleared to 0h, then the DH portion of the DH-HMAC-CHAP protocol shall not be performed in this
authentication transaction. The controller shall not clear this field to 00h if the AUTH_Negotiate message
(refer to section 8.3.4.4.1) for this instance of the DH-HMAC-CHAP protocol requested secure channel
concatenation (i.e., the SC_C field in that message was set to a non-zero value).


648


NVM Express [®] Base Specification, Revision 2.2


**DH Value Length (DHVLEN):** Diffie-Hellman exponential length. This length shall be a multiple of 4. If the
DH group identifier is cleared to 0h (i.e., NULL DH exchange), this field shall be cleared to 0h. Otherwise,
it shall be set to the length in bytes of the DH Value.


**Sequence Number (SEQNUM):** 32-bit sequence number S1. A random non-zero value shall be used as
the initial value. The sequence number is incremented modulo 2 [32] after each use, except that the value 0h
is skipped (i.e., incrementing the value FFFFFFFFh results in the value 00000001h).


**Challenge Value (CVAL):** Shall be set to a random challenge value C1 (refer to section 8.3.4.5.7). Each
challenge value should be unique and unpredictable, since repetition of a challenge value in conjunction
with the same key may reveal information about the key or the correct response to this challenge. The
algorithm for generating the challenge value is outside the scope of this specification. Randomness of the
challenge value is crucial to the security of the protocol (refer to section 8.3.4.5.7). The CVAL length is the
same as the length of the selected hash function (i.e., HL).


**DH Value (DHV):** Diffie-Hellman exponential. If the DH Value Length is cleared to 0h, this field is not
present. The DH value shall be set to the value of g [x] mod p, where x is a random number selected by the
controller that shall be at least 256 bits long (refer to section 8.3.4.5.7) and p and g shall have the values
indicated in Figure 742, based on the selected DH group identifier.


Upon receiving a DH-HMAC-CHAP_Challenge message, if:

  - the Hash Length (HL) does not match the value specified in Figure 741 for the selected hash
function;

  - the Sequence Number (SEQNUM) is cleared to 0h;

  - DHgID is cleared to 0h and the AUTH_Negotiate message (refer to section 8.3.4.4.1) that the host
sent for this instance of the DH-HMAC-CHAP protocol requested secure channel concatenation
(i.e., the SC_C field in that message is set to a non-zero value);

  - DHgID is non-zero and the DH Value Length (DHVLEN) is cleared to 0h; or

  - DHgID is non-zero and the DH Value (DHV) is 0, 1, or p-1;


then the host shall:

  - reply with an AUTH_Failure2 message having reason code ‘Authentication failure’ and reason code
explanation ‘Incorrect payload’; and

  - disconnect the NVMe over Fabrics connection.


**8.3.4.5.4** **DH-HMAC-CHAP_Reply Message**


The DH-HMAC-CHAP_Reply message is sent from the host to the controller. The host may request
authentication of the controller to enable bidirectional authentication, by including a DH-HMAC-CHAP
challenge value C2 in this message. The challenge value C2 shall be different from the challenge value C1
received in the DH-HMAC-CHAP_Challenge message.


The format of the DH-HMAC-CHAP_Reply message is shown in Figure 744.


**Figure 744: DH-HMAC-CHAP_Reply message format**





|Bytes|Description|
|---|---|
|0|**Authentication Type (AUTH_TYPE):**01h (i.e., DH-HMAC-CHAP)|
|1|**Authentication Identifier (AUTH_ID):**02h (i.e., DH-HMAC-CHAP_Reply)|
|3:2|Reserved|
|5:4|**Transaction Identifier (T_ID):**16-bit transaction identifier|
|6|**Hash Length (HL):**Length in bytes of the selected hash function|
|7|Reserved|
|8|**Challenge Valid (CVALID):**<br>**Value**<br>**Definition**<br>00h<br>The Challenge Value is not valid<br>01h<br>The Challenge Value is valid<br>All other values<br>Reserved|


|Value|Definition|
|---|---|
|00h|The Challenge Value is not valid|
|01h|The Challenge Value is valid|
|All other values|Reserved|


649


NVM Express [®] Base Specification, Revision 2.2


**Figure 744: DH-HMAC-CHAP_Reply message format**

|Bytes|Description|
|---|---|
|9|Reserved|
|11:10|**DH Value Length (DHVLEN):** Length in bytes of DH value. If no DH value is<br>included in the message, then this field is cleared to 0h.|
|15:12|**Sequence Number (SEQNUM):** Sequence number S2.|
|15+HL:16|**Response Value (RVAL):** Response R1.|
|15+2*HL:16+HL|**Challenge Value (CVAL):** Challenge C2, if valid (i.e., if the CVALID field is set to<br>01h), cleared to 0h otherwise.|
|15+2*HL+DHVLEN:6+2*HL|**DH Value (DHV):** DH exponential gy mod p. This field is not present (i.e., the<br>CVAL field is the last field in the message) if DHVLEN is cleared to 0h.|



**Hash Length (HL):** Shall be set to the length in bytes of the selected hash function, as specified in Figure
741.


**Challenge Valid:** If the host does not require bidirectional authentication or no establishment of a secure
channel after unidirectional authentication is sought (refer to section 8.3.4.5.9), this field shall be cleared to
0h. Otherwise, this field shall be set to 01h.


**DH Value Length (DHVLEN):** Diffie-Hellman exponential length. This length shall be a multiple of 4. If the
DH group identifier is cleared to 0h (i.e., NULL DH exchange), this field shall be cleared to 0h. Otherwise,
it shall be set to the length in bytes of the DH Value.


**Sequence Number (SEQNUM):** 32-bit sequence number S2. A random non-zero value shall be used as
the initial value. The sequence number is incremented modulo 2 [32] after each use, except that the value 0h
is skipped (i.e., incrementing the value FFFFFFFFh results in the value 00000001h). The value 0h is used
to indicate that bidirectional authentication is not performed, but a challenge value C2 is carried in order to
generate a pre-shared key (PSK) for subsequent establishment of a secure channel (refer to section
8.3.4.5.9).


**Response Value (RVAL):** DH-HMAC-CHAP response value R1. The value of R1 is computed using the
hash function H( ) selected by the HashID parameter in the DH-HMAC-CHAP_Challenge message, and
the augmented challenge Ca1. If the NULL DH group has been selected, the augmented challenge Ca1 is
equal to the challenge C1 received from the controller (i.e., Ca1 = C1). If a non-NULL DH group has been
selected, the augmented challenge is computed applying the HMAC function using the hash function H( )
selected by the HashID parameter in the DH-HMAC-CHAP_Challenge message with the hash of the
ephemeral DH key resulting from the combination of the random value y selected by the host with the DH
exponential (i.e., g [x] mod p) received from the controller as HMAC key (refer to RFC 2104) to the challenge
C1 (i.e., Ca1 = HMAC(H((g [x] mod p) [y] mod p), C1) = HMAC(H(g [xy] mod p), C1)). The value of R1 shall be
computed applying the HMAC function using the hash function H( ) selected by the HashID parameter in
the DH-HMAC-CHAP_Challenge message with key Kh as HMAC key to the concatenation of the
augmented challenge Ca1, the sequence number S1, the transaction identifier T_ID, the secure channel
concatenation indication SC_C sent in the AUTH_Negotiate message, the eight ASCII characters
”HostHost” to indicate the host is computing the reply, the host NQN not including the null terminator, a 00h
byte, and the NVM subsystem NQN not including the null terminator (i.e., R1 = HMAC(Kh, Ca1 || S1 || T_ID
|| SC_C || ”HostHost” || NQNh || 00h || NQNc)). Using C language notation:


Ca1 = (DHgID == 00h) ? C1 : HMAC(H((g [x] mod p) [y] mod p)), C1)
R1 = HMAC(Kh, Ca1 || S1 || T_ID || SC_C || ”HostHost” || NQNh || 00h || NQNc)


**Challenge Value (CVAL):** Shall be set to a random challenge value C2 (refer to section 8.3.4.5.7). Each
challenge value should be unique and unpredictable, since repetition of a challenge value in conjunction
with the same key may reveal information about the key or the correct response to this challenge. The
algorithm for generating the challenge value is outside the scope of this specification. Randomness of the
challenge value is crucial to the security of the protocol (refer to section 8.3.4.5.7). The CVAL length is the
same as the length of the selected hash function (i.e., HL).


650


NVM Express [®] Base Specification, Revision 2.2


**DH Value (DHV):** Diffie-Hellman exponential. If the DH Value Length is cleared to 0h, this field is not
present. The DH Value shall be set to the value of g [y] mod p, where y is a random number selected by the
host that shall be at least 256 bits long (refer to section 8.3.4.5.7) and p and g shall have the values indicated
in Figure 742, based on the selected DH group identifier.


Upon receiving a DH-HMAC-CHAP_Reply message, if:

  - the Hash Length (HL) does not match the value specified in Figure 741 for the selected hash
function;

  - DHgID is non-zero and the DH Value Length (DHVLEN) is cleared to 0h; or

  - DHgID is non-zero and the DH Value (DHV) is 0, 1, or p-1;


then the controller shall:

  - reply with an AUTH_Failure1 message having reason code ‘Authentication failure’ and reason code
explanation ‘Incorrect payload’; and

  - disconnect the NVMe over Fabrics connection.


In addition, the controller shall:

  - check the challenge value C2, if the Challenge Valid field is set to 01h, to verify it is different from
the challenge value C1 the controller previously sent. If C2 is equal to C1, the controller shall:


`o` reply with an AUTH_Failure1 message having reason code ‘Authentication failure’ and
reason code explanation ‘Authentication failed’; and

`o` disconnect the NVMe over Fabrics connection; and

  - verify the response value R1 using the negotiated hash function. If verification of the response value
R1 does not succeed, the controller shall:


`o` reply with an AUTH_Failure1 message having reason code ‘Authentication failure’ and
reason code explanation ‘Authentication failed’; and

`o` disconnect the NVMe over Fabrics connection.


If verification of the response value R1 succeeds, the host has been authenticated and the controller
shall continue with a DH-HMAC-CHAP_Success1 message.


**8.3.4.5.5** **DH-HMAC-CHAP_Success1 Message**


The DH-HMAC-CHAP_Success1 message is sent from the controller to the host and indicates that the
controller has successfully authenticated the host. The format of the DH-HMAC-CHAP_Success1 message
is shown in Figure 745.


**Figure 745: DH-HMAC-CHAP_Success1 message format**

|Bytes|Description|
|---|---|
|0|**Authentication Type (AUTH_TYPE):**01h (i.e., DH-HMAC-CHAP)|
|1|**Authentication Identifier (AUTH_ID):**03h (i.e., DH-HMAC-CHAP_Success1)|
|3:2|Reserved|
|5:4|**Transaction Identifier (T_ID):**16-bit transaction identifier|
|6|**Hash Length (HL):**Length in bytes of the selected hash function|
|7|Reserved|
|8|**Response Valid (RVALID):**<br>**Value**<br>**Definition**<br>00h<br>The Response Value is not valid<br>01h<br>The Response Value is valid<br>All other values<br>Reserved|
|15:9|Reserved|
|15+HL:16|**Response Value (RVAL):** Response R2, if valid (i.e., if the RVALID field is set to 01h), cleared to<br>0h otherwise|


|Value|Definition|
|---|---|
|00h|The Response Value is not valid|
|01h|The Response Value is valid|
|All other values|Reserved|



651


NVM Express [®] Base Specification, Revision 2.2


**Hash Length (HL):** Shall be set to the length in bytes of the selected hash function, as specified in Figure
741.


**Response Valid:** If the host did not request authentication of the controller (i.e., bidirectional authentication)
this field shall be cleared to 0h to indicate that no response is conveyed (i.e., the Response Value field is
not valid). If the host did request authentication of the controller, this field shall be set to 01h.


**Response Value (RVAL):** DH-HMAC-CHAP response value R2. The value of R2 is computed using the
hash function H( ) selected by the HashID parameter of the DH-HMAC-CHAP_Challenge message, and
the augmented challenge Ca2. If the NULL DH group has been selected, the augmented challenge Ca2 is
equal to the challenge C2 received from the host (i.e., Ca2 = C2). If a non-NULL DH group has been selected,
the augmented challenge is computed applying the HMAC function using the hash function H( ) selected
by the HashID parameter in the DH-HMAC-CHAP_Challenge message with the hash of the ephemeral DH
key resulting from the combination of the random value x selected by the controller with the DH exponential
(i.e., g [y] mod p) received from the host as HMAC key (refer to RFC 2104) to the challenge C2 (i.e., Ca2 =
HMAC(H((g [y] mod p) [x] mod p), C2) = HMAC(H(g [xy] mod p)), C2). The value of R2 shall be computed applying
the HMAC function using the hash function H( ) selected by the HashID parameter in the DH-HMACCHAP_Challenge message with key Kc as HMAC key to the concatenation of the augmented challenge
Ca2, the sequence number S2, the transaction identifier T_ID, the secure channel concatenation indication
SC_C received in the AUTH_Negotiate message, the ten ASCII characters ”Controller” to indicate the
controller is computing the reply, the NVM Subsystem NQN not including the null terminator, a 00h byte,
and the host NQN not including the null terminator (i.e., R2 = HMAC(Kc, Ca2 || S2 || T_ID || SC_C ||
”Controller” || NQNc || 00h || NQNh)). Using C language notation:


Ca2 = (DHgID == 00h) ? C2 : HMAC(H((g [y] mod p) [x] mod p)), C2)
R2 = HMAC(Kc, Ca2 || S2 || T_ID || SC_C || ”Controller” || NQNc || 00h || NQNh)


Upon receiving a DH-HMAC-CHAP_Success1 message:

  - if the Hash Length (HL) does not match the value specified in Figure 741 for the selected hash
function, the host shall:


`o` reply with an AUTH_Failure2 message having reason code ‘Authentication failure’ and
reason code explanation ‘Incorrect payload’; and

`o` disconnect the NVMe over Fabrics connection; and


  - if the Response Valid field is set to 01h, the host shall verify the response value R2 using the
negotiated hash function and DH group. If verification of the response value R2 does not succeed,
the host shall:


`o` reply with an AUTH_Failure2 message having reason code ‘Authentication failure’ and
reason code explanation ‘Authentication failed’; and

`o` disconnect the NVMe over Fabrics connection.


If verification of the response value R2 succeeds, the controller has been authenticated and the host
shall continue with a DH-HMAC-CHAP_Success2 message.


**8.3.4.5.6** **DH-HMAC-CHAP_Success2 Message**


The DH-HMAC-CHAP_Success2 message is sent from the host to the controller and indicates that the host
has successfully authenticated the controller. The format of the DH-HMAC-CHAP_Success2 message is
shown in Figure 746.


**Figure 746: DH-HMAC-CHAP_Success2 message format**

|Bytes|Description|
|---|---|
|0|**Authentication Type (AUTH_TYPE):**01h (i.e., DH-HMAC-CHAP)|
|1|**Authentication Identifier (AUTH_ID):**04h (i.e., DH-HMAC-CHAP_Success2)|
|3:2|Reserved|
|5:4|**Transaction Identifier (T_ID):**16-bit transaction identifier|
|15:6|Reserved|



652


NVM Express [®] Base Specification, Revision 2.2


**8.3.4.5.7** **DH-HMAC-CHAP Security Requirements**


In order to authenticate with the DH-HMAC-CHAP protocol, each host or controller uses a DH-HMACCHAP key that is associated with the entity’s NQN. A DH-HMAC-CHAP key is unidirectional (i.e., used only
for one direction of an authentication transaction). A DH-HMAC-CHAP key should not be associated with
more than one NQN as this opens security vulnerabilities. All DH-HMAC-CHAP implementations should
check for use of the same key with more than one NQN and should generate an administrative warning if
this situation occurs (e.g., as a result of configuring a DH-HMAC-CHAP key to verify authentication of
another entity).


The DH-HMAC-CHAP key is derived from an administratively configured secret (refer to section 8.3.4.5.8).
Each host and NVM subsystem shall support:

  - transforming the provided secret into a key applying the HMAC function using the hash function
specified in the secret representation (refer to section 8.3.4.5.8) with the secret as HMAC key to
the concatenation of its own NQN not including the null terminator and the seventeen ASCII
characters “NVMe-over-Fabrics” (i.e., key = HMAC(secret, NQN || ”NVMe-over-Fabrics”)). This
transformation ensures the resulting key is uniquely associated with the entity identified by the
NQN; and

  - using the provided secret as a key. This is intended for use with key management solutions able to
ensure that key is uniquely associated with the entity identified by the NQN.


NVM subsystems should support the ability to use a different NVM subsystem key with each host. Hosts
should support the ability to use a different host key with each NVM subsystem. NVM subsystems should
support the ability to use a different NVM subsystem secret with each host. Hosts should support the ability
to use a different host secret with each NVM subsystem.


If an implementation of NVMe over Fabrics is capable of functioning as both a host and an NVM subsystem,
then that implementation shall use either:

  - one NQN for the host functionality and a different NQN for the NVM subsystem functionality; or

  - one NQN for both host functionality and NVM subsystem functionality.


DH-HMAC-CHAP implementations may reuse a DH exponential (e.g., g [x] mod p or g [y] mod p). The primary
risk in allowing reuse of a DH exponential is replay of a prior authentication sequence based on the attacker
reusing the other exponential. For DH-HMAC-CHAP, replay is prevented with extremely high probability by
the requirement that all challenges be randomly generated. See section 2.12 of RFC 7296 for guidance on
DH exponential reuse.


The security of the DH-HMAC-CHAP protocol requires secrets, challenges, and DH exponents (i.e., x and
y) to be generated from actual randomness. For a discussion of randomness and sources of randomness,
refer to RFC 4086.


Implementations shall use a cryptographic random number generator that should be seeded with at least
256 bits of entropy to generate random numbers for this protocol. The secret provisioning mechanism for
each host and controller is outside of scope of this specification. For instance, secrets could be provisioned
via an encrypted HTTPS-based connection.


**8.3.4.5.8** **Secret Representation**


In order to facilitate provisioning, management, and interchange (e.g., copy & paste in an administrative
configuration tool) of secrets, all NVMe over Fabrics entities shall support the following ASCII representation
of secrets:


DHHC-1:xx:<Base64 encoded string>:


Where:

  - ”DHHC-1” indicates this is a version 1 representation of a secret for the DH-HMAC-CHAP protocol;

  - ‘:’ is used both as a separator and a terminator;

  - xx indicates the hash function to be used to transform the secret in key (refer to section 8.3.4.5.7),
encoded as the ASCII representation of the hexadecimal value specified in Figure 741 (e.g., the


653


NVM Express [®] Base Specification, Revision 2.2


two ASCII characters “01” indicate SHA-256). The two ASCII characters “00” indicate no transform
(i.e., use the secret as a key); and

  - The Base64 (refer to RFC 4648) string encodes the secret (32, 48, or 64 bytes binary) followed by
the CRC-32 (refer to RFC 1952) of the secret (4 bytes binary).


As an example, the 32-byte secret:


89AEB31A 874EAF84 841B4673 6B0DFDF2 BA58D30A A2A545A3 E235A352 1E07594Ch


has the CRC-32 A70D69FAh, that is represented in little endian format (i.e., FA690DA7h) for concatenation
to the secret, resulting in the following:


“DHHC-1:00:ia6zGodOr4SEG0Zzaw398rpY0wqipUWj4jWjUh4HWUz6aQ2n:”


when intended to be used as a key without transform.


When provided with a secret in this format, NVMe over Fabrics entities shall verify the validity of the
provided secret by computing the CRC-32 value of the secret and checking the computed value with the
provided value. If they do not match, then the secret shall not be used.


**8.3.4.5.9** **Generated PSK for TLS**


When used with a non-NULL DH exchange, the DH-HMAC-CHAP protocol is able to generate a session
key KS used to generate a pre-shared key (PSK) to establish a secure channel session with the TLS protocol
between host and controller for NVMe/TCP. A TLS session is concatenated to an authentication transaction
when the SC_C indication is set to NEWTLSPSK in the AUTH_Negotiate message (refer to section 8.3.4.1).
A TLS session shall not be concatenated to an authentication transaction if the involved host and controller
are administratively configured with a PSK for use with each other. In this case, host and controller shall
only establish a TLS session based on the retained PSK derived from that configured PSK.


The session key KS shall be computed from the ephemeral DH key (i.e., g [xy] mod p) generated during the
DH-HMAC-CHAP transaction by applying the hash function H( ) selected by the HashID parameter in the
DH-HMAC-CHAP_Challenge message (i.e., KS = H(g [xy] mod p)). The size of the session key KS is
determined by the selected hash function, as shown in Figure 741. Specifically:

  - The host computes KS as the hash of the ephemeral DH key resulting from the combination of the
random value y selected by the host with the DH exponential (i.e., g [x] mod p) received from the
controller (i.e., KS = H((g [x] mod p) [y] mod p) = H(g [xy] mod p)).

  - The controller computes KS as the hash of the ephemeral DH key resulting from the combination
of the random value x selected by the controller with the DH exponential (i.e., g [y] mod p) received
from the host (i.e., KS = H((g [y] mod p) [x] mod p) = H(g [xy] mod p)).


The generated PSK for TLS shall be computed applying the HMAC function using the hash function H( )
selected by the HashID parameter in the DH-HMAC-CHAP_Challenge message with the session key KS
as key to the concatenation of the two challenges C1 and C2 (i.e., generated PSK = HMAC(KS, C1 || C2)).
This generated PSK should be replaced periodically (e.g., every hour) or on demand by performing a
reauthentication on the Admin queue of the association with the appropriate SC_C value (refer to section
8.3.4.1).


The host may request secure channel concatenation with the TLS protocol by setting the SC_C field in the
AUTH_Negotiate message to NEWTLSPSK while performing only unidirectional authentication. In this case
the host shall still send a challenge value C2 to the controller and clear the sequence number S2 to 0h to
indicate that controller authentication is not requested.


**8.3.4.5.10 Mapping of DH-HMAC-CHAP Messages to Authentication Commands**


The DH-HMAC-CHAP_Reply message and the DH-HMAC-CHAP_Success2 message are sent from the
host to the controller, therefore they are mapped to the Authentication Send command. The DH-HMACCHAP_Challenge message and the DH-HMAC-CHAP_Success1 message are sent from the controller to
the host, therefore they are mapped to the Authentication Receive command.


654


NVM Express [®] Base Specification, Revision 2.2


**8.3.4.5.11 DH-HMAC-CHAP Configuration**


DH-HMAC-CHAP implementations that do not use an AVE (refer to section 8.3.4.6 for AVE information)
shall be able to be provisioned with their own DH-HMAC-CHAP secret and with a verification secret per
each remote entity that is able to be authenticated. DH-HMAC-CHAP implementations that use an AVE
shall be able to be provisioned with their own DH-HMAC-CHAP secret and the parameters for accessing
the AVE (refer to section 8.3.4.6.2).


This section uses the term configuration to indicate an NVMe internal state that controls the use of DHHMAC-CHAP. That internal state may or may not be externally configurable for a host or NVM subsystem.
For an NVMe/TCP implementation that supports DH-HMAC-CHAP, a DH-HMAC-CHAP configuration may
apply to:

  - a single connection;

  - a group of connections; or

  - all connections.


DH-HMAC-CHAP implementations that do not support secure channel concatenation with the TLS protocol
shall support configuring use of DH-HMAC-CHAP using one or more of the configurations shown in Figure
747.


**Figure 747: DH-HMAC-CHAP Configurations**

|Configuration|Description|
|---|---|
|Authentication Disabled|Authentication of a remote entity not allowed|
|Authentication Permitted|Authentication of a remote entity allowed|
|Authentication Required|Authentication of a remote entity required|



NVM subsystems that do not support secure channel concatenation with the TLS protocol shall set the ATR
and ASCR bits in the AUTHREQ field in the response of a successful Connect command (refer to Figure
549) as defined in Figure 748.


**Figure 748: NVM Subsystem AUTHREQ Settings for DH-HMAC-CHAP**

|Configuration|ASCR|ATR|
|---|---|---|
|Authentication Disabled|0|0|
|Authentication Permitted|0|0|
|Authentication Required|0|1|



Hosts that do not support secure channel concatenation with the TLS protocol shall behave as defined in
Figure 749, according to the ATR and ASCR bits in the AUTHREQ field received in the response of a
successful Connect command (refer to Figure 549).


**Figure 749: DH-HMAC-CHAP Host Behavior**











|Host Configuration|ASCR|ATR|Action|
|---|---|---|---|
|Authentication Disabled|0|0|Do not begin an authentication transaction|
|Authentication Disabled|0|1|Disconnect from the NVM subsystem|
|Authentication Disabled|1|any|any|
|Authentication Permitted|0|0|If the TASC field in the Discovery Log Page Entry for the<br>remote entity is set to 01b or set to 10b, then begin an<br>authentication transaction with the SC_C field set to NOSC.<br>If the TASC field in the Discovery Log Page Entry for the<br>remote entity is cleared to 00b or set to 11b or if no Discovery<br>Log Page Entry for the remote entity has been retrieved, then<br>do not begin an authentication transaction.|
|Authentication Permitted|0|1|Begin an authentication transaction with the SC_C field set to<br>NOSC|
|Authentication Permitted|1|any|Disconnect from the NVM subsystem|


655


NVM Express [®] Base Specification, Revision 2.2


**Figure 749: DH-HMAC-CHAP Host Behavior**

|Host Configuration|ASCR|ATR|Action|
|---|---|---|---|
|Authentication Required|0|any|Begin an authentication transaction with the SC_C field set to<br>NOSC|
|Authentication Required|1|any|Disconnect from the NVM subsystem|



NVM subsystems that do not support secure channel concatenation with the TLS protocol shall behave as
defined in Figure 750, according to the SC_C field in a received AUTH_Negotiate message (refer to section
8.3.4.4.1).


**Figure 750: DH-HMAC-CHAP NVM Subsystem Behavior**






|Subsystem Configuration|SC_C Value|Action|
|---|---|---|
|Authentication Disabled|Any|Disconnect from the host|
|Authentication Permitted|NOSC|Participate in the authentication transaction|
|Authentication Permitted|NEWTLSPSK or<br>REPLACETLSPSK|Disconnect from the host|
|Authentication Required|NOSC|Participate in the authentication transaction|
|Authentication Required|NEWTLSPSK or<br>REPLACETLSPSK|Disconnect from the host|



For example, consider a host that supports DH-HMAC-CHAP without secure channel concatenation with
the TLS protocol configured with Authentication Permitted and an NVM subsystem that supports DHHMAC-CHAP without secure channel concatenation with the TLS protocol configured with Authentication
Required. As defined in Figure 748, the NVM subsystem clears the ASCR bit to ‘0’ and sets the ATR bit to
‘1’ in the Connect response. As defined in Figure 749, upon receiving the Connect response the host begins
an authentication transaction with the SC_C field set to NOSC. As defined in Figure 750, the NVM
subsystem participates in the authentication transaction.


DH-HMAC-CHAP implementations that support secure channel concatenation with the TLS protocol shall
support configuring use of DH-HMAC-CHAP with secure channel concatenation with the TLS protocol using
one or more of the configurations shown in Figure 751.


**Figure 751: DH-HMAC-CHAP with TLS Concatenation Configurations**






|Configuration|Col2|Description|
|---|---|---|
|Authentication Disabled|TLS Disabled|Authentication and set up of a secure channel with a remote entity<br>not allowed|
|Authentication Permitted|TLS Disabled|Authentication of a remote entity allowed, set up of a secure<br>channel not allowed|
|Authentication Permitted|TLS Permitted|Authentication and set up of a secure channel with a remote entity<br>allowed|
|Authentication Required|TLS Disabled|Authentication of a remote entity required, set up of a secure<br>channel not allowed|
|Authentication Required|TLS Permitted|Authentication of a remote entity required, set up of a secure<br>channel allowed|
|Authentication Required|TLS Required|Authentication and set up of a secure channel with a remote entity<br>required|



NVM subsystems that support secure channel concatenation with the TLS protocol shall set the ATR and
ASCR bits in the AUTHREQ field in the response of a successful Connect command on an Admin Queue
over a TCP channel without TLS (refer to Figure 549) as defined in Figure 752.


**Figure 752: NVM Subsystem AUTHREQ Settings for DH-HMAC-CHAP with TLS Concatenation**

|Configuration|Col2|ASCR|ATR|
|---|---|---|---|
|Authentication Disabled|TLS Disabled|0|0|



656


NVM Express [®] Base Specification, Revision 2.2


**Figure 752: NVM Subsystem AUTHREQ Settings for DH-HMAC-CHAP with TLS Concatenation**






|Configuration|Col2|ASCR|ATR|
|---|---|---|---|
|Authentication Permitted|TLS Disabled|0|0|
|Authentication Permitted|TLS Permitted|0|0|
|Authentication Required|TLS Disabled|0|1|
|Authentication Required|TLS Permitted|0|1|
|Authentication Required|TLS Required|1|0|



Hosts that support secure channel concatenation with the TLS protocol shall behave as defined Figure 753,
according to the ATR and ASCR bits in the AUTHREQ field received in the response of a successful
Connect command on an Admin Queue over a TCP channel without TLS (refer to Figure 549).


**Figure 753: DH-HMAC-CHAP with TLS Concatenation Host Behavior**

























|Host Configuration|Col2|ASCR|ATR|Action|
|---|---|---|---|---|
|Authentication<br>Disabled|TLS Disabled|0|0|Do not begin an authentication transaction|
|Authentication<br>Disabled|TLS Disabled|0|1|Disconnect from the NVM subsystem|
|Authentication<br>Disabled|TLS Disabled|1|any|any|
|Authentication<br>Permitted|TLS Disabled|0|0|If the TASC field in the Discovery Log Page Entry for<br>the remote entity is set to 01b or set to 10b, then begin<br>an authentication transaction with the SC_C field set to<br>NOSC.<br>If the TASC field in the Discovery Log Page Entry for<br>the remote entity is cleared to 00b or set to 11b or if no<br>Discovery Log Page Entry for the remote entity has<br>been retrieved, then do not begin an authentication<br>transaction.|
|Authentication<br>Permitted|TLS Disabled|0|1|Begin an authentication transaction with the SC_C field<br>set to NOSC|
|Authentication<br>Permitted|TLS Disabled|1|any|Disconnect from the NVM subsystem|
|Authentication<br>Permitted|TLS Permitted|0|0|If the TASC field in the Discovery Log Page Entry for<br>the remote entity is set to 01b, then begin an<br>authentication transaction with the SC_C field set to<br>NOSC.<br>If the TASC field in the Discovery Log Page Entry for<br>the remote entity is set to 10b, then begin an<br>authentication transaction with the SC_C field set to<br>NEWTLSPSK.<br>If the TASC field in the Discovery Log Page Entry for<br>the remote entity is cleared to 00b or set to 11b or if no<br>Discovery Log Page Entry has been retrieved for the<br>remote entity, then do not begin an authentication<br>transaction.|
|Authentication<br>Permitted|TLS Permitted|0|1|Begin an authentication transaction with the SC_C field<br>set to NOSC|
|Authentication<br>Permitted|TLS Permitted|1|any|Begin an authentication transaction with the SC_C field<br>set to NEWTLSPSK|
|Authentication<br>Required|TLS Disabled|0|any|Begin an authentication transaction with the SC_C field<br>set to NOSC|
|Authentication<br>Required|TLS Disabled|1|any|Disconnect from the NVM subsystem|
|Authentication<br>Required|TLS Permitted|0|any|Begin an authentication transaction with the SC_C field<br>set to NOSC|
|Authentication<br>Required|TLS Permitted|1|any|Begin an authentication transaction with the SC_C field<br>set to NEWTLSPSK|
|Authentication<br>Required|TLS Required|any|any|Begin an authentication transaction with the SC_C field<br>set to NEWTLSPSK|


657


NVM Express [®] Base Specification, Revision 2.2


NVM subsystems that support secure channel concatenation with the TLS protocol shall behave as defined
in Figure 754, according to the SC_C field in a received AUTH_Negotiate message on an Admin Queue
over a TCP channel without TLS (refer to section 8.3.4.4.1).


**Figure 754: DH-HMAC-CHAP with TLS Concatenation NVM Subsystem Behavior**












|Subsystem Configuration|Col2|SC_C Value|Action|
|---|---|---|---|
|Authentication<br>Disabled|TLS Disabled|any|Disconnect from the host|
|Authentication<br>Permitted|TLS Disabled|NOSC|Participate in the authentication transaction|
|Authentication<br>Permitted|TLS Disabled|NEWTLSPSK or<br>REPLACETLSPSK|Disconnect from the host|
|Authentication<br>Permitted|TLS Permitted|NOSC|Participate in the authentication transaction|
|Authentication<br>Permitted|TLS Permitted|NEWTLSPSK|Participate in the authentication transaction and<br>establish a TLS channel as described in section<br>8.3.4.3|
|Authentication<br>Permitted|TLS Permitted|REPLACETLSPSK|Disconnect from the host|
|Authentication<br>Required|TLS Disabled|NOSC|Participate in the authentication transaction|
|Authentication<br>Required|TLS Disabled|NEWTLSPSK or<br>REPLACETLSPSK|Disconnect from the host|
|Authentication<br>Required|TLS Permitted|NOSC|Participate in the authentication transaction|
|Authentication<br>Required|TLS Permitted|NEWTLSPSK|Participate in the authentication transaction and<br>establish a TLS channel as described in section<br>8.3.4.3|
|Authentication<br>Required|TLS Permitted|REPLACETLSPSK|Disconnect from the host|
|Authentication<br>Required|TLS Required|NOSC or<br>REPLACETLSPSK|Disconnect from the host|
|Authentication<br>Required|TLS Required|NEWTLSPSK|Participate in the authentication transaction and<br>establish a TLS channel as described in section<br>8.3.4.3|



As an example, consider a host that supports DH-HMAC-CHAP with secure channel concatenation with
the TLS protocol configured with Authentication Permitted, TLS Permitted and an NVM subsystem that
supports DH-HMAC-CHAP with secure channel concatenation with the TLS protocol configured with
Authentication Required, TLS Required. As defined in Figure 752, the NVM subsystem sets the ASCR bit
to ‘1’ and clears the ATR bit to ‘0’ in the Connect response. As defined in Figure 753, upon receiving the
Connect response the host begins an authentication transaction with the SC_C field set to NEWTLSPSK.
As defined in Figure 754, the NVM subsystem participates in the authentication transaction and establishes
a TLS channel.


**DH-HMAC-CHAP Authentication Verification Entity**


**8.3.4.6.1** **Overview**


A DH-HMAC-CHAP Authentication Verification Entity (AVE) is a service that performs the DH-HMAC-CHAP
authentication verification function on behalf of an NVMe entity (i.e., a host or a controller). An example of
a DH-HMAC-CHAP authentication transaction with AVE is shown in Figure 755, using the notation shown
in Figure 739.


658


NVM Express [®] Base Specification, Revision 2.2


**Figure 755: Example of DH-HMAC-CHAP authentication transaction with AVE**


**Host** **Controller** **AVE**









As shown in Figure 755, a controller using the AVE service delegates to the AVE the verification of the
response R1 received from the host by passing the relevant DH-HMAC-CHAP authentication transaction
parameters to the AVE through a DH-HMAC-CHAP_Access-Request message. A host using the AVE
service delegates to the AVE the verification of the response R2 received from the controller by passing the
relevant DH-HMAC-CHAP authentication transaction parameters to the AVE through a DH-HMACCHAP_Access-Request message. In both cases, the AVE replies with a DH-HMAC-CHAP_Access-Result
message containing the result of the authentication verification (refer to section 8.3.4.6.3).


Use of the AVE service by an NVMe entity is optional and is determined by configuration of the NVMe
entity. If an NVMe entity uses the AVE, then provisioning of DH-HMAC-CHAP information on that entity is
reduced to only that entity’s DH-HMAC-CHAP secret (refer to section 8.3.4.5.8) and the parameters (refer
to section 8.3.4.6.2) for accessing the AVE (i.e., no DH-HMAC-CHAP keys are required to be provisioned
for verification of responses received from other NVMe entities).


An AVE is required to maintain the following information for each NVMe entity:

  - The NQN of that entity (i.e., NQNe),

  - the DH-HMAC-CHAP key associated with that entity (i.e., Ke), and

  - the PSK shared between that entity and the AVE (i.e., PSKea).


Ke is used to perform the authentication verification function (refer to section 8.3.4.6.3) and PSKea is used
to establish a secure connection with the AVE (refer to section 8.3.4.6.2). An AVE shall support all hash
functions defined for DH-HMAC-CHAP (refer to section 8.3.4.5.2).


To facilitate dynamic discovery of the transport addresses of an AVE through a Discovery Controller (refer
to section 8.3.4.6.4) and to simplify establishing a secure connection to an AVE (refer to section 8.3.4.6.2),
an AVE is identified at by an NQN (NQNAVE).


659


NVM Express [®] Base Specification, Revision 2.2


**8.3.4.6.2** **AVE Connections**


An NVMe entity (i.e., a host or a controller) connection with a DH-HMAC-CHAP AVE shall use TLS version
1.3 (refer to RFC 8446) with pre-shared key (PSK) authentication, as specified for NVMe/TCP (refer to the
NVM Express TCP Transport Specification).


In order to establish a TLS connection with an AVE, an NVMe entity requires a PSK shared between that
entity and the AVE (i.e., PSKea) for authentication of the TLS connection. PSKea shall be either derived from
the DH-HMAC-CHAP secret, if the DH-HMAC-CHAP secret representation specifies a hash function (refer
to section 8.3.4.5.8), or provisioned on the NVMe entity through a configured PSK, as specified for
NVMe/TCP.


Derivation of PSKea from a DH-HMAC-CHAP secret shall use the HKDF-Extract and HKDF-Expand-Label
operations (refer to RFC 5869 and RFC 8446) in the following order:


1. PRK = HKDF-Extract(0, DH-HMAC-CHAP secret); and
2. PSKea = HKDF-Expand-Label(PRK, “A-V-Entity” || NQNAVE, NQNe, Length(DH-HMAC-CHAP
secret)),


where NQNAVE is the NQN of the AVE and NQNe is the NQN of the NVMe entity. The hash function used
with HKDF shall be the one specified in the DH-HMAC-CHAP secret representation (refer to section
8.3.4.5.8). This transform requires that the NVMe entity knows NQNAVE.


Derivation of PSKea from a DH-HMAC-CHAP secret is not possible if the DH-HMAC-CHAP secret
representation does not specify a hash function. In this case PSKea shall be provisioned on the NVMe entity
through a configured PSK, as specified for NVMe/TCP, and that configured PSK should be different than
the DH-HMAC-CHAP secret for that entity.


Derivation of PSKea from a configured PSK shall use the HKDF-Extract and HKDF-Expand-Label operations
in the following order:


1. PRK = HKDF-Extract(0, Configured PSK); and
2. PSKea = HKDF-Expand-Label(PRK, “A-V-Entity” || NQNAVE, NQNe, Length(Configured PSK)),


where NQNAVE is the NQN of the AVE and NQNe is the NQN of the NVMe entity. The hash function used
with HKDF shall be the one specified in the PSK interchange format (refer to the NVM Express TCP
Transport Specification). If no hash function is specified in the PSK interchange format, then the configured
PSK shall be used as PSKea. This transform requires that the NVMe entity knows NQNAVE.


The TLS connection with the AVE shall be performed as specified in the TLS PSK and PSK Identity
Derivation section of the NVM Express TCP Transport Specification, with PSKea used as the Retained PSK,
NQNe used as the host NQN, and NQNAVE used as the controller NQN. Mandatory and recommended
cipher suites for this TLS connection are specified in the Mandatory and Recommended Cipher Suites
section of the NVM Express TCP Transport Specification. This TLS connection may be used for multiple
authentication verifications. An NVMe entity may terminate this TLS connection and re-establish it as
required. An AVE may terminate this TLS connection after some period of inactivity (e.g., 10 minutes). An
NVMe entity may avoid termination of this TLS connection by using the TLS heartbeat extension (refer to
RFC 6520).


**8.3.4.6.3** **AVE Access Protocol**


Communication with a DH-HMAC-CHAP AVE uses two PDUs, DH-HMAC-CHAP_Access-Request and
DH-HMAC-CHAP_Access-Result, that are sent directly over the TLS connection with the AVE (refer to
section 8.3.4.6.2). The format of the DH-HMAC-CHAP_Access-Request PDU is shown in Figure 756.


**Figure 756: DH-HMAC-CHAP_Access-Request PDU format**

|Bytes|Description|
|---|---|
|00|**PDU Type (PDU-Type):** AEh for DH-HMAC-CHAP_Access-Request|
|01|**Flags (FLAGS):** Reserved|
|02|**Header Length (HLEN):**Fixed length of 8 bytes (08h)|



660


NVM Express [®] Base Specification, Revision 2.2


**Figure 756: DH-HMAC-CHAP_Access-Request PDU format**

|Bytes|Description|
|---|---|
|03|**PDU Data Offset (PDO):**Reserved|
|07:04|**PDU Length (PLEN):**total length of the PDU in bytes|
|15:08|**Identifier (ID):**64-bit identifier used to match Access-Request and Access-Result<br>PDUs|
|16|**Hash Length (HL):**Length in bytes of the selected hash function|
|17|**Hash Identifier (HashID):** Identifier of selected hash function|
|19:18|**Transaction Identifier (T_ID):**16-bit authentication transaction identifier|
|20|**Secure Channel Concatenation (SC_C):**Secure Channel concatenation<br>indication|
|21|**Responder’s Role (RESPR):** ‘H’ if host, ‘C’ if controller|
|22|**NQN Responder Length (NQNRlen):** Length of the responder’s NQN|
|23|Reserved|
|27:24|**Sequence Number (SEQN):** Sequence number S|
|27+HL:28|**Augmented Challenge Value (ACV):**Challenge Ca|
|27+2*HL:28+HL|**Response Value (RESPV):** Response R|
|NQNRlen+27+2*HL:28+2*HL|**NQN of Responder (NQNR):**Responder’s NQN|



The DH-HMAC-CHAP_Access-Request PDU contains the parameters exchanged by the host and the
controller during a DH-HMAC-CHAP authentication transaction. The responder is the entity that replied to
a DH-HMAC-CHAP challenge sent by an authenticator.


Referring to Figure 755, when the controller transmits the DH-HMAC-CHAP_Access-Request PDU, the
parameters are instantiated as follows:

  - Responder’s Role: ‘H’

  - Sequence Number: S1

  - Augmented Challenge Value: Ca1

  - Response Value: R1

  - NQNR: NQNh

  - HashID, T_ID, SC_C: the correspondent DH-HMAC-CHAP parameters


When the host transmits the DH-HMAC-CHAP_Access-Request PDU, the parameters are instantiated as
follows:

  - Responder’s Role: ‘C’

  - Sequence Number: S2

  - Augmented Challenge Value: Ca2

  - Response Value: R2

  - NQNR: NQNc

  - HashID, T_ID, SC_C: the correspondent DH-HMAC-CHAP parameters


Upon receiving a DH-HMAC-CHAP_Access-Request PDU, the AVE shall perform the following steps in
order:


1. Lookup the DH-HMAC-CHAP key of the responder (i.e., Kr) from NQNR;
2. If the Responder’s Role is ‘H’, compute the expected response R’ as:
R’ = HMAC(Kr, Ca || S || T_ID || SC_C || ”HostHost” || NQNr || 00h || NQNa)
where NQNa is the NQN of the authenticator;
3. If the Responder’s Role is ‘C’, compute the expected response R’ as:
R’ = HMAC(Kr, Ca || S || T_ID || SC_C || ”Controller” || NQNr || 00h || NQNa)
where NQNa is the NQN of the authenticator; and
4. Compare the expected response R’ with the response value R received in the DH-HMACCHAP_Access-Request PDU. If R’ = R then the authentication is successful; if R’ ≠ R then the
authentication has failed.


661


NVM Express [®] Base Specification, Revision 2.2


The NQN of the authenticator (i.e., NQNa) is retrieved from the TLS identity associated to the TLS
connection with the AVE (refer to section 8.3.4.6.2).


The result of an authentication verification is returned to the NVMe entity in a DH-HMAC-CHAP_AccessResult PDU. The format of the DH-HMAC-CHAP_Access-Result PDU is shown in Figure 757.


**Figure 757: DH-HMAC-CHAP_Access-Result PDU format**






|Value|Definition|
|---|---|
|01h|Authentication Verification Successful|
|02h|Authentication Verification Failed|
|All other values|Reserved|



|Bytes|Description|
|---|---|
|00|**PDU Type (PDU-Type):** AFh for DH-HMAC-CHAP_Access-Result|
|01|**Flags (FLAGS):** Reserved|
|02|**Header Length (HLEN):**Fixed length of 8 bytes (08h)|
|03|**PDU Data Offset (PDO):**Reserved|
|07:04|**PDU Length (PLEN):**Fixed length of 20 bytes (14h)|
|15:08|**Identifier (ID):**64-bit identifier used to match Access-Request and Access-Result PDUs|
|16|**Authentication Verification Result (AuthRes):**<br>**Value**<br>**Definition**<br>01h<br>Authentication Verification Successful<br>02h<br>Authentication Verification Failed<br>All other values<br>Reserved|
|17|**Reason Code (RCODE):**Additional explanation when authentication verification failed <br>**Value**<br>**Definition**<br>00h<br>No additional explanation<br>01h<br>Authentication failure<br>02h<br>Selected hash function unusable<br>All other values<br>Reserved|
|19:18|Reserved|


**8.3.4.6.4** **AVE Discovery**

|Value|Definition|
|---|---|
|00h|No additional explanation|
|01h|Authentication failure|
|02h|Selected hash function unusable|
|All other values|Reserved|



The AVE transport addresses may be configured on an NVMe entity or may be discovered by interacting
with a Discovery Controller (e.g., a CDC). An NVMe entity should randomly select any of the discovered
AVE transport addresses to connect to the AVE. The AVE Discovery log page is defined to facilitate this
discovery (refer to section 5.1.12.3.3).


662


