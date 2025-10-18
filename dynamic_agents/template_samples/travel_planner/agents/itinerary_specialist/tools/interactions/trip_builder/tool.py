"""Agent-scoped tool that composes the final itinerary for the traveler."""

from __future__ import annotations

from typing import Any, Dict, Optional


class Tool:
    def __init__(self, metadata: Dict[str, Any]):
        self.metadata = metadata

    def compile_itinerary(
        self,
        traveler_name: Optional[str] = None,
        preferences: Optional[Dict[str, Any]] = None,
        state: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        preferences = preferences or {}
        state = state or {}
        def _safe_get(container: Optional[Dict[str, Any]], key: str) -> Optional[str]:
            if isinstance(container, dict):
                value = container.get(key)
                if isinstance(value, str) and value.strip():
                    return value
            return None

        traveler_name = (
            traveler_name
            or _safe_get(state.get("profile"), "name")
            or _safe_get(state.get("user"), "name")
            or _safe_get(state.get("travel"), "traveler_name")
            or _safe_get(state.get("travel"), "primary_contact")
            or "Viajante"
        )
        hotel_results = state.get("web_travel_search:search_hotels", {}).get("options", [])
        flight_results = state.get("web_travel_search:search_flights", {}).get("itineraries", [])
        experience_results = state.get("web_travel_search:search_experiences", {}).get("activities", [])

        best_hotel = hotel_results[0] if hotel_results else None
        best_flight = flight_results[0] if flight_results else None
        best_experience = experience_results[0] if experience_results else None

        summary_parts = [f"Proposta personalizada para {traveler_name}"]
        if best_flight:
            summary_parts.append(
                f"Voo sugerido: {best_flight.get('title', 'opcao disponivel')}"
            )
        if best_hotel:
            summary_parts.append(
                f"Hotel recomendado: {best_hotel.get('title', 'hotel disponivel')}"
            )
        if best_experience:
            summary_parts.append(
                f"Experiencia destacada: {best_experience.get('title', 'atividade disponivel')}"
            )
        if preferences:
            summary_parts.append("Preferencias consideradas: " + ", ".join(preferences.keys()))

        recommended_plan = {
            "flights": flight_results[:3],
            "hotels": hotel_results[:3],
            "experiences": experience_results[:5],
            "preferences": preferences,
        }

        return {
            "summary": " | ".join(summary_parts),
            "recommended_plan": recommended_plan,
        }
