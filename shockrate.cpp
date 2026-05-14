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

int main() {
    double tenderRate = 150.0;
    double mainRate = 350.0;
    double crossover = 2.5;
    double preload = 0.75;
    double maxShockTravel = 8.0;

    double keq = eqRate(tenderRate, mainRate);
    double preloadForceShock = keq * preload;

    cout << fixed << setprecision(2);

    cout << "DOUBLE COILOVER CALCULATOR\n";
    cout << "---------------------------------------------\n";
    cout << "Tender rate:                  " << tenderRate << " lb/in\n";
    cout << "Main rate:                    " << mainRate << " lb/in\n";
    cout << "Equivalent rate:              " << keq << " lb/in\n";
    cout << "Preload force at shock:       " << preloadForceShock << " lb\n";
    cout << "Crossover shock travel:       " << crossover << " in\n\n";
    return 0;
}