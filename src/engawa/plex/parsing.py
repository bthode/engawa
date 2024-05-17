from typing import List, Optional
from xml.etree import ElementTree as ET


class Location:
    def __init__(self, id_: int, path: str) -> None:
        self.id_: int = id_
        self.path: str = path

    def __str__(self) -> str:
        return f"Location(id={self.id_}, path={self.path})"

    def __repr__(self) -> str:
        return f"Location(id={self.id_}, path={self.path})"

    @classmethod
    def from_xml(cls, xml_data: ET.Element) -> "Location":
        id_: int = int(xml_data.attrib.get("id", 0))
        path: str = xml_data.attrib.get("path", "")

        return cls(id_, path)


class MediaContainer:
    def __init__(
        self,
        name: str,
        size: int = 0,
        allow_sync: Optional[int] = None,
        plugins: Optional[str] = None,
        directories: Optional[List["Directory"]] = None,
        devices: Optional[List["Device"]] = None,
        account: Optional[List["Account"]] = None,
        claimed: Optional[int] = None,
        machine_identifier: Optional[str] = None,
        version: Optional[str] = None,
        content: Optional[str] = None,
        identifier: Optional[str] = None,
    ) -> None:
        self.name: str = name
        self.size: int = size
        self.allow_sync: Optional[int] = allow_sync
        self.plugins: Optional[str] = plugins
        self.directories: List["Directory"] = directories or []
        self.devices: List["Device"] = devices or []
        self.account: List["Account"] = account or []
        self.claimed: Optional[int] = claimed
        self.machine_identifier: Optional[str] = machine_identifier
        self.version: Optional[str] = version
        self.content: Optional[str] = content
        self.identifier: Optional[str] = identifier

    def __str__(self) -> str:
        _: List[str] = [self.name]
        if self.directories:
            _.append(f"Directories: {', '.join(str(directory) for directory in self.directories)}")
        if self.devices:
            _.append(f"Devices: {', '.join(str(device) for device in self.devices)}")
        if self.account:
            _.append(f"Accounts: {', '.join(str(account) for account in self.account)}")
        return ", ".join(_)

    def __repr__(self) -> str:
        _: List[str] = [self.name]
        if self.directories:
            _.append(f"Directories: {', '.join(repr(directory) for directory in self.directories)}")
        if self.devices:
            _.append(f"Devices: {', '.join(repr(device) for device in self.devices)}")
        if self.account:
            _.append(f"Accounts: {', '.join(repr(account) for account in self.account)}")
        return ", ".join(_)

    @classmethod
    def from_xml(cls, xml_data: ET.Element) -> "MediaContainer":
        name: str = xml_data.attrib["title1"]
        size: int = int(xml_data.attrib.get("size", 0))
        allow_sync: Optional[int] = int(xml_data.attrib.get("allowSync", 0))
        plugins: Optional[str] = xml_data.attrib.get("plugins")
        claimed: Optional[int] = int(xml_data.attrib.get("claimed", 0))
        machine_identifier: Optional[str] = xml_data.attrib.get("machineIdentifier")
        version: Optional[str] = xml_data.attrib.get("version")
        content: Optional[str] = xml_data.attrib.get("content")
        identifier: Optional[str] = xml_data.attrib.get("identifier")
        directories: List["Directory"] = [
            Directory.from_xml(directory_data) for directory_data in xml_data.findall("Directory")
        ]
        devices: List["Device"] = [Device.from_xml(device_data) for device_data in xml_data.findall("Device")]
        account: List["Account"] = [Account.from_xml(account_data) for account_data in xml_data.findall("Account")]

        return cls(
            name=name,
            size=size,
            allow_sync=allow_sync,
            plugins=plugins,
            directories=directories,
            devices=devices,
            account=account,
            claimed=claimed,
            machine_identifier=machine_identifier,
            version=version,
            content=content,
            identifier=identifier,
        )


class Directory:
    def __init__(
        self,
        allow_sync: int,
        art: str,
        composite: str,
        filters: int,
        refreshing: int,
        thumb: str,
        key: int,
        type_: str,
        title: str,
        agent: str,
        scanner: str,
        language: str,
        uuid: str,
        updated_at: str,
        created_at: str,
        scanned_at: str,
        content: int,
        directory: int,
        content_changed_at: str,
        hidden: int,
        location: List["Location"],
    ) -> None:
        self.allow_sync: int = allow_sync
        self.art: str = art
        self.composite: str = composite
        self.filters: int = filters
        self.refreshing: int = refreshing
        self.thumb: str = thumb
        self.key: int = key
        self.type_: str = type_
        self.title: str = title
        self.agent: str = agent
        self.scanner: str = scanner
        self.language: str = language
        self.uuid: str = uuid
        self.updated_at: str = updated_at
        self.created_at: str = created_at
        self.scanned_at: str = scanned_at
        self.content: int = content
        self.directory: int = directory
        self.content_changed_at: str = content_changed_at
        self.hidden: int = hidden
        self.location: List["Location"] = location

    def __str__(self) -> str:
        return f"Directory(title={self.title})"

    def __repr__(self) -> str:
        return f"Directory(title={self.title})"

    @classmethod
    def from_xml(cls, xml_data: ET.Element) -> "Directory":
        allow_sync: int = int(xml_data.attrib.get("allowSync", 0))
        art: str = xml_data.attrib.get("art", "")
        composite: str = xml_data.attrib.get("composite", "")
        filters: int = int(xml_data.attrib.get("filters", 0))
        refreshing: int = int(xml_data.attrib.get("refreshing", 0))
        thumb: str = xml_data.attrib.get("thumb", "")
        key: int = int(xml_data.attrib.get("key", 0))
        type_: str = xml_data.attrib.get("type", "")
        title: str = xml_data.attrib.get("title", "")
        agent: str = xml_data.attrib.get("agent", "")
        scanner: str = xml_data.attrib.get("scanner", "")
        language: str = xml_data.attrib.get("language", "")
        uuid: str = xml_data.attrib.get("uuid", "")
        updated_at: str = xml_data.attrib.get("updatedAt", "")
        created_at: str = xml_data.attrib.get("createdAt", "")
        scanned_at: str = xml_data.attrib.get("scannedAt", "")
        content: int = int(xml_data.attrib.get("content", 0))
        directory: int = int(xml_data.attrib.get("directory", 0))
        content_changed_at: str = xml_data.attrib.get("contentChangedAt", "")
        hidden: int = int(xml_data.attrib.get("hidden", 0))
        location: List["Location"] = [
            Location.from_xml(location_data) for location_data in xml_data.findall("Location")
        ]

        return cls(
            allow_sync,
            art,
            composite,
            filters,
            refreshing,
            thumb,
            key,
            type_,
            title,
            agent,
            scanner,
            language,
            uuid,
            updated_at,
            created_at,
            scanned_at,
            content,
            directory,
            content_changed_at,
            hidden,
            location,
        )


class Device:
    def __init__(
        self,
        id_: int,
        name: str,
        platform: str,
        client_identifier: str,
        created_at: str,
    ) -> None:
        self.id_: int = id_
        self.name: str = name
        self.platform: str = platform
        self.client_identifier: str = client_identifier
        self.created_at: str = created_at

    def __str__(self) -> str:
        return f"Device(name={self.name})"

    @classmethod
    def from_xml(cls, xml_data: ET.Element) -> "Device":
        id_: int = int(xml_data.attrib.get("id", 0))
        name: str = xml_data.attrib.get("name", "")
        platform: str = xml_data.attrib.get("platform", "")
        client_identifier: str = xml_data.attrib.get("clientIdentifier", "")
        created_at: str = xml_data.attrib.get("createdAt", "")

        return cls(id_, name, platform, client_identifier, created_at)


class Account:
    def __init__(
        self,
        id_: int,
        key: str,
        name: Optional[str],
        default_audio_language: str,
        auto_select_audio: int,
        default_subtitle_language: str,
        subtitle_mode: int,
        thumb: Optional[str],
    ) -> None:
        self.id_: int = id_
        self.key: str = key
        self.name: Optional[str] = name
        self.default_audio_language: str = default_audio_language
        self.auto_select_audio: int = auto_select_audio
        self.default_subtitle_language: str = default_subtitle_language
        self.subtitle_mode: int = subtitle_mode
        self.thumb: Optional[str] = thumb

    @classmethod
    def from_xml(cls, xml_data: ET.Element) -> "Account":
        id_: int = int(xml_data.attrib.get("id", 0))
        key: str = xml_data.attrib.get("key", "")
        name: Optional[str] = xml_data.attrib.get("name")
        default_audio_language: str = xml_data.attrib.get("defaultAudioLanguage", "")
        auto_select_audio: int = int(xml_data.attrib.get("autoSelectAudio", 0))
        default_subtitle_language: str = xml_data.attrib.get("defaultSubtitleLanguage", "")
        subtitle_mode: int = int(xml_data.attrib.get("subtitleMode", 0))
        thumb: Optional[str] = xml_data.attrib.get("thumb")

        return cls(
            id_,
            key,
            name,
            default_audio_language,
            auto_select_audio,
            default_subtitle_language,
            subtitle_mode,
            thumb,
        )


def parse_directories(directory_xml: ET.Element) -> List[Directory]:
    directories: List[Directory] = []
    for directory_data in directory_xml.findall("Directory"):
        directory = Directory.from_xml(directory_data)
        directories.append(directory)
    return directories


def parse_accounts(account_xml: ET.Element) -> List[Account]:
    accounts: List[Account] = []
    for account_data in account_xml.findall("Account"):
        account = Account.from_xml(account_data)
        accounts.append(account)
    return accounts


def parse_devices(device_xml: ET.Element) -> List[Device]:
    devices: List[Device] = []
    for device_data in device_xml.findall("Device"):
        device = Device.from_xml(device_data)
        devices.append(device)
    return devices


def parse_media_container(xml_data: ET.Element) -> MediaContainer:
    return MediaContainer.from_xml(xml_data)
