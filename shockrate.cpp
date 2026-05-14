#include <iostream>
#include <iomanip>
using namespace std;

double eqRate(double tenderRate, double mainRate) {
    return (tenderRate * mainRate) / (tenderRate + mainRate);
}

double shockForce(
    double tenderRate,
    double mainRate,
    double crossover,
    double preload,
    double shockTravel
) {
    double keq = eqRate(tenderRate, mainRate);

    if (shockTravel <= crossover) {
        return keq * (preload + shockTravel);
    } else {
        return keq * (preload + crossover) + mainRate * (shockTravel - crossover);
    }
}

double activeShockRate(
    double tenderRate,
    double mainRate,
    double crossover,
    double shockTravel
) {
    double keq = eqRate(tenderRate, mainRate);

    if (shockTravel <= crossover) {
        return keq;
    } else {
        return mainRate;
    }
}

double wheelTravel(double shockTravel, double motionRatio) {
    return shockTravel / motionRatio;
}

double wheelForce(double shockForceValue, double motionRatio) {
    return shockForceValue * motionRatio;
}

double wheelRate(double shockRateValue, double motionRatio) {
    return shockRateValue * motionRatio * motionRatio;
}

int main() {
    double tenderRate = 150.0;
    double mainRate = 350.0;
    double motionRatio = 0.85;
    double crossover = 2.5;
    double preload = 0.75;
    double maxShockTravel = 8.0;

    double keq = eqRate(tenderRate, mainRate);
    double preloadForceShock = keq * preload;
    double preloadForceWheel = wheelForce(preloadForceShock, motionRatio);

    cout << fixed << setprecision(2);

    cout << "DOUBLE COILOVER CALCULATOR\n";
    cout << "---------------------------------------------\n";
    cout << "Tender rate:                 " << tenderRate << " lb/in\n";
    cout << "Main rate:                   " << mainRate << " lb/in\n";
    cout << "Equivalent rate:             " << keq << " lb/in\n";
    cout << "Wheel rate before crossover: " << wheelRate(keq, motionRatio) << " lb/in\n";
    cout << "Wheel rate after crossover:  " << wheelRate(mainRate, motionRatio) << " lb/in\n";
    cout << "Preload force at wheel:      " << preloadForceWheel << " lb\n\n";
    return 0;
}