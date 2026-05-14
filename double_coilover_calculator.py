from dataclasses import dataclass
from typing import List, Dict


@dataclass
class CoiloverSetup:
    tender_rate: float
    main_rate: float
    motion_ratio: float
    crossover_shock_travel: float
    preload_threads_in: float
    max_shock_travel: float
    points: int = 121


def equivalent_rate_series(k1: float, k2: float) -> float:
    return (k1 * k2) / (k1 + k2)


def force_at_shock_travel(setup: CoiloverSetup, shock_travel: float) -> Dict[str, float]:
    keq = equivalent_rate_series(setup.tender_rate, setup.main_rate)
    x = max(0.0, shock_travel)
    crossover = max(0.0, min(setup.crossover_shock_travel, setup.max_shock_travel))
    preload = max(0.0, setup.preload_threads_in)

    if x <= crossover:
        shock_force = keq * (preload + x)
        shock_rate = keq
    else:
        shock_force = keq * (preload + crossover) + setup.main_rate * (x - crossover)
        shock_rate = setup.main_rate

    wheel_force = shock_force * setup.motion_ratio
    wheel_rate = shock_rate * setup.motion_ratio ** 2
    wheel_travel = x / setup.motion_ratio

    return {
        "shock_travel_in": x,
        "wheel_travel_in": wheel_travel,
        "shock_force_lb": shock_force,
        "wheel_force_lb": wheel_force,
        "shock_rate_lb_per_in": shock_rate,
        "wheel_rate_lb_per_in": wheel_rate,
    }


def build_curve(setup: CoiloverSetup) -> List[Dict[str, float]]:
    curve = []
    n = max(2, setup.points)
    for i in range(n):
        x = setup.max_shock_travel * i / (n - 1)
        curve.append(force_at_shock_travel(setup, x))
    return curve


def print_summary(setup: CoiloverSetup) -> None:
    keq = equivalent_rate_series(setup.tender_rate, setup.main_rate)
    preload_force_shock = keq * setup.preload_threads_in
    preload_force_wheel = preload_force_shock * setup.motion_ratio
    crossover = force_at_shock_travel(setup, setup.crossover_shock_travel)
    end_point = force_at_shock_travel(setup, setup.max_shock_travel)

    print("\nDOUBLE COILOVER SPRING CALCULATOR")
    print("-" * 40)
    print(f"Tender rate:                  {setup.tender_rate:.2f} lb/in")
    print(f"Main rate:                    {setup.main_rate:.2f} lb/in")
    print(f"Equivalent pre-crossover:     {keq:.2f} lb/in")
    print(f"Motion ratio:                 {setup.motion_ratio:.3f}")
    print(f"Wheel rate before crossover:  {keq * setup.motion_ratio**2:.2f} lb/in")
    print(f"Wheel rate after crossover:   {setup.main_rate * setup.motion_ratio**2:.2f} lb/in")
    print(f"Preload threads showing:      {setup.preload_threads_in:.3f} in")
    print(f"Preload force at wheel:       {preload_force_wheel:.2f} lb")
    print(f"Crossover shock travel:       {setup.crossover_shock_travel:.3f} in")
    print(f"Crossover wheel travel:       {crossover['wheel_travel_in']:.3f} in")
    print(f"Wheel force at crossover:     {crossover['wheel_force_lb']:.2f} lb")
    print(f"Wheel force at max travel:    {end_point['wheel_force_lb']:.2f} lb")


def prompt_float(label: str, default: float) -> float:
    raw = input(f"{label} [{default}]: ").strip()
    return default if raw == "" else float(raw)


def main() -> None:
    print("Enter values in inches and lb/in. Press Enter to accept defaults.\n")
    setup = CoiloverSetup(
        tender_rate=prompt_float("Tender spring rate", 150.0),
        main_rate=prompt_float("Main spring rate", 350.0),
        motion_ratio=prompt_float("Motion ratio", 0.85),
        crossover_shock_travel=prompt_float("Crossover point (shock travel)", 2.5),
        preload_threads_in=prompt_float("Threads showing / preload compression", 0.75),
        max_shock_travel=prompt_float("Max shock travel to evaluate", 8.0),
        points=int(prompt_float("Number of curve points", 21)),
    )

    print_summary(setup)

    curve = build_curve(setup)
    print("\nSample force curve points:")
    print("shock_travel(in) | wheel_travel(in) | shock_force(lb) | wheel_force(lb) | wheel_rate(lb/in)")
    print("-" * 95)
    for row in curve:
        print(
            f"{row['shock_travel_in']:15.3f} | "
            f"{row['wheel_travel_in']:16.3f} | "
            f"{row['shock_force_lb']:15.2f} | "
            f"{row['wheel_force_lb']:15.2f} | "
            f"{row['wheel_rate_lb_per_in']:17.2f}"
        )


if __name__ == "__main__":
    main()
