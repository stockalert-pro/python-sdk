"""Base alerts resource with shared logic."""
from typing import Any, Dict

from ..exceptions import ValidationError


class AlertsResourceBase:
    """Base class with shared validation logic."""

    def _validate_create_request(self, data: Dict[str, Any]) -> None:
        """Validate create alert request."""
        # Basic validation
        if not data.get("symbol"):
            raise ValidationError("Symbol is required")

        if not data.get("condition"):
            raise ValidationError("Condition is required")

        # Validate symbol format (allow A-Z, 0-9, dot, hyphen; up to 10 chars)
        symbol = str(data["symbol"]).strip().upper()
        import re
        if not symbol or not re.fullmatch(r"[A-Z0-9.-]{1,10}", symbol):
            raise ValidationError("Symbol must be 1-10 chars: A-Z, 0-9, dot or hyphen")

        # Normalize symbol
        data["symbol"] = symbol

        # Validate notification channel
        if "notification" in data:
            valid_channels = ["email", "sms"]
            if data["notification"] not in valid_channels:
                raise ValidationError(f"Notification must be one of: {', '.join(valid_channels)}")

        # Validate condition-specific requirements
        self._validate_condition_requirements(data)

    def _validate_condition_requirements(self, data: Dict[str, Any]) -> None:
        """Validate condition-specific requirements."""
        condition = data["condition"]
        threshold = data.get("threshold")
        params = data.get("parameters", {}) or {}

        # Conditions that require threshold
        requires_threshold = [
            "price_above", "price_below", "price_change_up", "price_change_down",
            "reminder", "ma_touch_above", "ma_touch_below", "rsi_limit", "volume_change",
            "pe_ratio_below", "pe_ratio_above",
            "forward_pe_below", "forward_pe_above",
            "earnings_announcement", "dividend_ex_date", "insider_transactions"
        ]

        # Conditions that don't use threshold
        no_threshold = [
            "new_high", "new_low", "ma_crossover_golden", "ma_crossover_death",
            "daily_reminder", "dividend_payment"
        ]

        if condition in requires_threshold and threshold is None:
            raise ValidationError(f"{condition} requires a threshold value")

        if condition in no_threshold and threshold is not None:
            raise ValidationError(f"{condition} does not use a threshold value")

        # Specific validations
        if condition in ["ma_touch_above", "ma_touch_below"]:
            if not isinstance(threshold, int) or threshold <= 0:
                raise ValidationError(
                    f"{condition} requires a positive moving average period as threshold"
                )

        if condition == "rsi_limit" and threshold is not None:
            if not 0 <= threshold <= 100:
                raise ValidationError("RSI threshold must be between 0 and 100")

        if condition == "reminder":
            if not params.get("reminder_date") or not params.get("reminder_time"):
                raise ValidationError("Reminder alerts require reminder_date and reminder_time")

        if condition == "daily_reminder":
            delivery_time = params.get("deliveryTime")
            if delivery_time is not None and delivery_time not in ["market_open", "after_market_close"]:
                raise ValidationError(
                    'Daily reminder deliveryTime must be "market_open" or "after_market_close"'
                )

        if condition == "dividend_payment":
            shares = params.get("shares")
            if not isinstance(shares, (int, float)) or shares <= 0:
                raise ValidationError("Dividend payment alerts require a positive shares parameter")

        if condition == "insider_transactions":
            if threshold is not None and threshold <= 0:
                raise ValidationError("insider_transactions threshold must be greater than 0")

            direction = params.get("direction")
            if direction is not None and direction not in ["buy", "sell", "both"]:
                raise ValidationError("insider_transactions direction must be buy, sell or both")

            min_executives = params.get("minExecutives")
            if min_executives is not None and (
                not isinstance(min_executives, int) or min_executives < 1
            ):
                raise ValidationError(
                    "insider_transactions minExecutives must be a positive integer"
                )

            window_days = params.get("windowDays")
            if window_days is not None and (
                not isinstance(window_days, int) or window_days < 1
            ):
                raise ValidationError(
                    "insider_transactions windowDays must be a positive integer"
                )

            open_market_only = params.get("openMarketOnly")
            if open_market_only is not None and not isinstance(open_market_only, bool):
                raise ValidationError(
                    "insider_transactions openMarketOnly must be a boolean"
                )
