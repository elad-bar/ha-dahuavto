# Dahua VTO Integration

#### Integration configuration of the VTO unit
```
name: custom name
host: hostname or ip
port: port of the VTO unit
username: Username to the web portal
password: Password to the web portal
```

#### Components:
###### binary_sensor.dahua_vto_available
```
State: represents whether the unit is online or not
Attributes:
    appAutoStart
    deviceType
    hardwareVersion
    processor
    serialNumber
    updateSerial
    updateSerialCloudUpgrade
    Last Ring
    Last Update
    CallType
    CreateTime
    EndState
    LocalNumber
    MessageTime
    PeerNumber
    PeerType
    RecNo
    TalkTime
    CreateDateTime
    CreatedDate
    device_class
```


###### binary_sensor.dahua_vto_ring
```
State: represents whether over the last 5 seconds there was a call
Attributes:
    appAutoStart
    deviceType
    hardwareVersion
    processor
    serialNumber
    updateSerial
    updateSerialCloudUpgrade
    Last Ring
    Last Update
    CallType
    CreateTime
    EndState
    LocalNumber
    MessageTime
    PeerNumber
    PeerType
    RecNo
    TalkTime
    CreateDateTime
    CreatedDate
    device_class
```