"""
Kodreferens

- - - INTE en del av lösningen - - - 

Extrakt ur ett tidigare eget projekt (separat .ipynb)
Detta är INTE verifierat att köra fristående i detta projekts venv. Det förutsätter dataframes ("df_model", "train_c", "val_c" osv.) som byggdes upp i tidigare celler i originalnotebooken, vilka inte reproduceras här för att undvika att gissa på kod jag inte kan verifiera

Syfte: visa faktisk modelleringsprocess som ligger bakom resonemanget i "report.md"; inte att vara körbar kod i detta repo
"""

# --- Datakälla - koppling till detta projekts data/ ---
# Detta är den faktiska inläsningen från originalkoden. Samma råformat (csv, ingen header) ligger i detta repos "data/nq-15m_bk.csv". Alltså samma källdata som valideras av "src/validator/" i detta projekt

import pandas as pd

df_raw = pd.read_csv(
    "data/nq-15m_bk.csv", sep=";", header=None,
    names=["date", "time", "open", "high", "low", "close", "volume"],
)
# Ur denna råa 15-minutersdata byggdes "sessions" som dagliga features ("Asia"/"London"/"RTH") som sedan matades in i XGBoost-modellerna nedan. Den aggregeringslogiken är utelämnad här. Jag ville bara visa att samma rådata som valideras här också var grunden för ML-projektet


# --- Cell 27: Träna XGBoost-regressor för RTH-range i ticks ---
from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_error, r2_score

reg = XGBRegressor(
    n_estimators=300, max_depth=3, learning_rate=0.03,
    subsample=0.7, colsample_bytree=0.7, random_state=42
)
reg.fit(X_tr_r, y_tr_r, eval_set=[(X_vl_r, y_vl_r)], verbose=False)

# --- Cell 28: Fix - läckande feature (range_vs_atr) borttagen ---
feature_cols_reg = [f for f in feature_cols_v2 if f != "range_vs_atr"]

# --- Cell 34: Ta bort korta dagar (tidig stängning) och FOMC-dagar ---
rth_bar_counts = df_raw[df_raw["session"] == "RTH"].groupby("trade_date").size()
short_days = rth_bar_counts[rth_bar_counts < 15].index

fomc_bars = df_raw[df_raw.index.hour == 14].copy()
fomc_bars = fomc_bars[fomc_bars.index.minute.isin([0, 15])]
fomc_bars["vol_median_20"] = fomc_bars.groupby(fomc_bars.index.minute)["volume"].transform(
    lambda x: x.rolling(20, min_periods=5).median()
)
fomc_bars["fomc_flag"] = fomc_bars["volume"] > 3 * fomc_bars["vol_median_20"]

days_to_remove = set(short_days) | set(fomc_days)
df_model_clean = df_model[~df_model.index.isin(days_to_remove)].copy()
# Resultat: 145 korta dagar + 135 FOMC-dagar = 280 borttagna av 4446

# --- Cell 39: Sharpe, Sortino och equity curve (valideringdata) ---
import numpy as np

sharpe = (daily_pnl.mean() / daily_pnl.std()) * np.sqrt(252)
sortino = (daily_pnl.mean() / daily_pnl[daily_pnl < 0].std()) * np.sqrt(252)
# Resultat: Sharpe 1.34, Sortino 1.94 (valideringsperiod 2021-2023)

# --- Cell 43: FINAL OOS-TEST (2024-2026) - körs endast en gång ---
X_test = test_df[feature_cols]
test_df["proba"] = model.predict_proba(X_test)[:, 1]
test_df["signal"] = np.where(test_df["proba"] > 0.55, 1,
                     np.where(test_df["proba"] < 0.45, -1, 0))

sharpe_oos = (oos["pnl_usd"].mean() / oos["pnl_usd"].std()) * np.sqrt(252)


# FAKTISKT RESULTAT: Sharpe -0.21, Total P&L -$29 000
# Slutsats: modellen överanpassades till valideringsperiodens marknadsregim