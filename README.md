# Dahua VTO Integration

#### Configuration
Configuration support single Dahua VTO unit through Configuration -> Integrations

\* Custom component doesn't support YAML configuration!, in case you have used it via configuration.yaml, please remove it <br/>
\* In case labels in Configuration -> Integrations -> Add new are note being displayed, please delete the custom component and re-download it   


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