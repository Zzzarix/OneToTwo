# %% Import Dependencies
from typing import List, Optional, Type
from urllib.parse import urlparse

from onetotwo.applogger import AppLogger
from onetotwo.manager import MongoManager
from onetotwo.oneway.model import OneWay, Redirect, TargetUrl, WayLifetime
from onetotwo.utils import make_alias


# %% Managers
class RedirectManager(MongoManager[Redirect]):
    """Redirect firebase manager"""

    @classmethod
    def init(cls, logger: AppLogger, model: Type[Redirect]) -> None:
        super().init(logger, model)

    @classmethod
    def create(cls, ip: str, oneway_uid: str) -> Redirect:
        """Create Redirect model"""
        return cls._create(ip=ip, oneway_uid=oneway_uid)

    @classmethod
    def get(cls, uid: str) -> Optional[Redirect]:
        """Get Redirect model"""
        return cls._get_one({"_id": uid})

    @classmethod
    def get_redirects(cls, oneway_uid: str) -> List[Redirect]:
        """Get Redirect models associated with OneWay"""
        return cls._get_many({"oneway_uid": oneway_uid})

    @classmethod
    def delete_redirects(cls, oneway_uid: str) -> None:
        """Delete the Redirects model associated with OneWay"""
        return cls._delete({"oneway_uid": oneway_uid})


class OneWayManager(MongoManager[OneWay]):
    """OneWay firebase manager"""

    _redirect = RedirectManager

    @classmethod
    def init(cls, logger: AppLogger, model: Type[OneWay]) -> None:
        super().init(logger, model)

    @classmethod
    def _make_target_url(cls, target: str) -> TargetUrl:
        url = urlparse(target)

        query = dict([q.split("=") for q in url.query.split("&")])

        return TargetUrl(is_secured=True, domain=url.netloc, path=url.path, params=query)

    @classmethod
    def create(
        cls,
        name: str,
        target: str,
        is_temporary: bool,
        lifetime: WayLifetime,
        user_uid: Optional[str] = None,
        only_numbers: bool = False,
    ) -> OneWay:
        """Create OneWay model"""
        target_url = cls._make_target_url(target)
        alias = make_alias(length=5, only_numbers=only_numbers)
        while cls.get_by_alias(alias):
            alias = make_alias(length=5, only_numbers=only_numbers)
        return cls._create(
            name=name, alias=alias, target=target_url, is_temporary=is_temporary, lifetime=lifetime, user_uid=user_uid
        )

    @classmethod
    def get(cls, uid: str) -> Optional[OneWay]:
        """Get OneWay model"""
        return cls._get_one({"_id": uid})

    @classmethod
    def get_by_alias(cls, alias: str) -> Optional[OneWay]:
        """Get OneWay model by unique alias"""
        return cls._get_one({"alias": alias})

    @classmethod
    def delete(cls, uid: str) -> None:
        """Delete OneWay model"""
        cls._delete({"_id": uid})

        cls._redirect.delete_redirects(uid)

    @classmethod
    def redirect(cls, alias: str, ip: str) -> Optional[str]:
        """Returns a link for redirection"""
        way = cls.get_by_alias(alias)

        if not way:
            return None

        cls._redirect.create(ip=ip, oneway_uid=way.uid)

        return way.target.to_str()
