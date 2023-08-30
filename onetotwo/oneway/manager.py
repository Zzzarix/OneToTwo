# %% Import Dependencies
from typing import Optional, Type
from urllib.parse import urlparse
from onetotwo.applogger import AppLogger

from onetotwo.manager import FireBaseManager
from onetotwo.oneway.model import OneWay, Redirect, TargetUrl, WayLifetime
from onetotwo.utils import make_uuid


# %% Managers
class RedirectManager(FireBaseManager[Redirect]):
    """Redirect firebase manager"""

    def __init__(self, app_name: str, logger: AppLogger, model: Type[Redirect]) -> None:
        super().__init__(app_name, logger, model)

    def create(self, ip: str, oneway_uid: str) -> Redirect:
        """Create Redirect model"""
        return self._create(ip=ip, oneway_uid=oneway_uid)

    def get(self, uid: str) -> Redirect:
        """Get Redirect model"""
        return self._get(uid)

    def delete_redirects(self, oneway_uid: str) -> None:
        """Delete the Redirects model associated with OneWay"""
        for redirect in self._ref.order_by_child("oneway_uid").get():
            self._delete(redirect["uid"])


class OneWayManager(FireBaseManager[OneWay]):
    """OneWay firebase manager"""

    def __init__(self, app_name: str, logger: AppLogger, model: Type[OneWay], redirect_manager: RedirectManager) -> None:
        super().__init__(app_name, logger, model)
        self._redirect = redirect_manager

    def _make_target_url(self, target: str) -> TargetUrl:
        url = urlparse(target)

        query = dict([q.split("=") for q in url.query.split("&")])

        return TargetUrl(uid=make_uuid(), is_secured=True, domain=url.netloc, path=url.path, params=query)

    def create(
        self,
        name: str,
        alias: str,
        target: str,
        is_temporary: bool,
        lifetime: WayLifetime,
        user_uid: Optional[str] = None,
    ) -> OneWay:
        """Create OneWay model"""
        target_url = self._make_target_url(target)
        return self._create(
            name=name, alias=alias, target=target_url, is_temporary=is_temporary, lifetime=lifetime, user_uid=user_uid
        )

    def get(self, uid: str) -> OneWay:
        """Get OneWay model"""
        return self._get(uid)

    def delete(self, uid: str) -> None:
        """Delete OneWay model"""
        self._delete(uid)

        self._redirect.delete_redirects(uid)

    def redirect(self, alias: str, ip: str) -> str:
        """Returns a link for redirection"""
        res = self._ref.order_by_child("alias").equal_to({"alias": alias}).get()
        way = OneWay(**res)

        self._redirect.create(ip=ip, oneway_uid=way.uid)

        return way.target.format()
