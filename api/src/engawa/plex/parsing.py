from xml.etree import ElementTree


class Location:
    def __init__(self, id_: int, path: str) -> None:
        self.id_: int = id_
        self.path: str = path

    def __str__(self) -> str:
        return f"Location(id={self.id_}, path={self.path})"

    def __repr__(self) -> str:
        return f"Location(id={self.id_}, path={self.path})"

    @classmethod
    def from_xml(cls, xml_data: ElementTree.Element) -> "Location":
        id_: int = int(xml_data.attrib.get("id", 0))
        path: str = xml_data.attrib.get("path", "")

        return cls(id_, path)


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
        location: list[Location],
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
        self.location: list[Location] = location

    def __str__(self) -> str:
        return f"Directory(title={self.title})"

    def __repr__(self) -> str:
        return f"Directory(title={self.title})"

    @classmethod
    def from_xml(cls, xml_data: ElementTree.Element) -> "Directory":
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
        location: list[Location] = [
            Location.from_xml(location_data) for location_data in xml_data.findall(Location.__name__)
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
    def from_xml(cls, xml_data: ElementTree.Element) -> "Device":
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
        name: str | None,
        default_audio_language: str,
        auto_select_audio: int,
        default_subtitle_language: str,
        subtitle_mode: int,
        thumb: str | None,
    ) -> None:
        self.id_: int = id_
        self.key: str = key
        self.name: str | None = name
        self.default_audio_language: str = default_audio_language
        self.auto_select_audio: int = auto_select_audio
        self.default_subtitle_language: str = default_subtitle_language
        self.subtitle_mode: int = subtitle_mode
        self.thumb: str | None = thumb

    @classmethod
    def from_xml(cls, xml_data: ElementTree.Element) -> "Account":
        id_: int = int(xml_data.attrib.get("id", 0))
        key: str = xml_data.attrib.get("key", "")
        name: str | None = xml_data.attrib.get("name")
        default_audio_language: str = xml_data.attrib.get("defaultAudioLanguage", "")
        auto_select_audio: int = int(xml_data.attrib.get("autoSelectAudio", 0))
        default_subtitle_language: str = xml_data.attrib.get("defaultSubtitleLanguage", "")
        subtitle_mode: int = int(xml_data.attrib.get("subtitleMode", 0))
        thumb: str | None = xml_data.attrib.get("thumb")

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


class MediaContainer:
    def __init__(
        self,
        name: str,
        size: int = 0,
        allow_sync: int | None = None,
        plugins: str | None = None,
        directories: list[Directory] | None = None,
        devices: list[Device] | None = None,
        account: list[Account] | None = None,
        claimed: int | None = None,
        machine_identifier: str | None = None,
        version: str | None = None,
        content: str | None = None,
        identifier: str | None = None,
    ) -> None:
        self.name: str = name
        self.size: int = size
        self.allow_sync: int | None = allow_sync
        self.plugins: str | None = plugins
        self.directories: list[Directory] = directories or []
        self.devices: list[Device] = devices or []
        self.account: list[Account] = account or []
        self.claimed: int | None = claimed
        self.machine_identifier: str | None = machine_identifier
        self.version: str | None = version
        self.content: str | None = content
        self.identifier: str | None = identifier

    def __str__(self) -> str:
        _: list[str] = [self.name]
        if self.directories:
            _.append(f"Directories: {', '.join(str(directory) for directory in self.directories)}")
        if self.devices:
            _.append(f"Devices: {', '.join(str(device) for device in self.devices)}")
        if self.account:
            _.append(f"Accounts: {', '.join(str(account) for account in self.account)}")
        return ", ".join(_)

    def __repr__(self) -> str:
        _: list[str] = [self.name]
        if self.directories:
            _.append(f"Directories: {', '.join(repr(directory) for directory in self.directories)}")
        if self.devices:
            _.append(f"Devices: {', '.join(repr(device) for device in self.devices)}")
        if self.account:
            _.append(f"Accounts: {', '.join(repr(account) for account in self.account)}")
        return ", ".join(_)

    @classmethod
    def from_xml(cls, xml_data: ElementTree.Element) -> "MediaContainer":
        name: str = xml_data.attrib["title1"]
        size: int = int(xml_data.attrib.get("size", 0))
        allow_sync: int | None = int(xml_data.attrib.get("allowSync", 0))
        plugins: str | None = xml_data.attrib.get("plugins")
        claimed: int | None = int(xml_data.attrib.get("claimed", 0))
        machine_identifier: str | None = xml_data.attrib.get("machineIdentifier")
        version: str | None = xml_data.attrib.get("version")
        content: str | None = xml_data.attrib.get("content")
        identifier: str | None = xml_data.attrib.get("identifier")
        directories: list[Directory] = [
            Directory.from_xml(directory_data) for directory_data in xml_data.findall("Directory")
        ]
        devices: list["Device"] = [Device.from_xml(device_data) for device_data in xml_data.findall("Device")]
        account: list["Account"] = [Account.from_xml(account_data) for account_data in xml_data.findall("Account")]

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


def parse_directories(directory_xml: ElementTree.Element) -> list[Directory]:
    directories: list[Directory] = []
    for directory_data in directory_xml.findall("Directory"):
        directory = Directory.from_xml(directory_data)
        directories.append(directory)
    return directories


def parse_accounts(account_xml: ElementTree.Element) -> list[Account]:
    accounts: list[Account] = []
    for account_data in account_xml.findall("Account"):
        account = Account.from_xml(account_data)
        accounts.append(account)
    return accounts


def parse_devices(device_xml: ElementTree.Element) -> list[Device]:
    devices: list[Device] = []
    for device_data in device_xml.findall("Device"):
        device = Device.from_xml(device_data)
        devices.append(device)
    return devices


def parse_media_container(xml_data: ElementTree.Element) -> MediaContainer:
    return MediaContainer.from_xml(xml_data)
