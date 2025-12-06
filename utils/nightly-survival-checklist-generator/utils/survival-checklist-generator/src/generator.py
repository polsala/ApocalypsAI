'''python
"""
survival_checklist_generator

Provides a simple function to generate a survival checklist based on a scenario.
"""

from __future__ import annotations
from typing import List, Dict

# Mockable data source: mapping scenario -> list of items
_DEFAULT_CHECKLISTS: Dict[str, List[str]] = {
    "zombie": [
        "Secure a fortified shelter",
        "Gather melee weapons",
        "Stockpile non‑perishable food",
        "Maintain a reliable water source",
        "Establish a communication plan",
    ],
    "nuclear": [
        "Find a lead‑lined shelter",
        "Acquire potassium iodide tablets",
        "Store canned food and water",
        "Prepare a radiation detector",
        "Plan for decontamination procedures",
    ],
    "meteor": [
        "Identify underground safe zones",
        "Gather emergency blankets",
        "Secure long‑term food supplies",
        "Maintain a solar charger",
        "Set up a community watch",
    ],
}


def generate_checklist(scenario: str) -> List[str]:
    """Return a checklist of survival steps for the given scenario.

    Parameters
    ----------
    scenario: str
        The post‑apocalyptic scenario (e.g., "zombie", "nuclear", "meteor").

    Returns
    -------
    List[str]
        Ordered list of recommended actions. If the scenario is unknown,
        a generic checklist is returned.

    The function looks up a predefined mapping but can be overridden by
    providing a custom ``_DEFAULT_CHECKLISTS`` dictionary at runtime.
    """
    key = scenario.lower().strip()
    return _DEFAULT_CHECKLISTS.get(key, [
        "Assess the situation",
        "Secure shelter",
        "Gather water and food",
        "Establish communication",
        "Plan for long‑term survival",
    ])
'''
