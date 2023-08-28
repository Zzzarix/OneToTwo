# %% Import Dependencies
from typing import Optional

from onetotwo.manager import FireBaseManager
from onetotwo.oneway.model import OneWay, Redirect, TargetUrl, WayLifetime


# %% Managers
class RedirectManager(FireBaseManager[Redirect]):
    """Redirect firebase manager"""

    def __init__(self, app_name: str, model_name: str) -> None:
        super().__init__(app_name, model_name)

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

    def __init__(self, app_name: str, model_name: str, redirect_manager: RedirectManager) -> None:
        super().__init__(app_name, model_name)
        self._redirect = redirect_manager

    def create(
        self, name: str, target: TargetUrl, is_temporary: bool, lifetime: WayLifetime, user_uid: Optional[str] = None
    ) -> OneWay:
        """Create OneWay model"""
        return self._create(name=name, target=target, is_temporary=is_temporary, lifetime=lifetime, user_uid=user_uid)

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
