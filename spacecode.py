# %%
#Quinn Boerger
#Project 4
#6/15/2025



# %%
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

def load_and_clean_train():
    df = pd.read_csv("train.csv")

    df = df[['PassengerId', 'HomePlanet', 'CryoSleep', 'Destination', 'Age', 'VIP',
             'RoomService', 'FoodCourt', 'ShoppingMall', 'Spa', 'VRDeck', 'Transported']]

    df.dropna(inplace=True)

    df['CryoSleep'] = df['CryoSleep'].astype(int)
    df['VIP'] = df['VIP'].astype(int)
    df['Transported'] = df['Transported'].astype(int)

    df = pd.get_dummies(df, columns=['HomePlanet', 'Destination'])

    return df

def load_and_clean_test(required_columns):
    test = pd.read_csv("test.csv")
    passenger_ids = test['PassengerId']

    test = test[['HomePlanet', 'CryoSleep', 'Destination', 'Age', 'VIP',
                 'RoomService', 'FoodCourt', 'ShoppingMall', 'Spa', 'VRDeck']]

    test.fillna(method='ffill', inplace=True)
    test['CryoSleep'] = test['CryoSleep'].astype(int)
    test['VIP'] = test['VIP'].astype(int)
    test = pd.get_dummies(test)

    for col in required_columns:
        if col not in test.columns:
            test[col] = 0
    test = test[required_columns]

    return test, passenger_ids

def main():
    df = load_and_clean_train()
    X = df.drop(['PassengerId', 'Transported'], axis=1)
    y = df['Transported']

    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestClassifier(random_state=42)
    model.fit(X_train, y_train)
    val_preds = model.predict(X_val)
    acc = accuracy_score(y_val, val_preds)
    print(f"Validation Accuracy: {acc:.4f}")

    X_test, ids = load_and_clean_test(X.columns)
    preds = model.predict(X_test)

    submission = pd.DataFrame({
        "PassengerId": ids,
        "Transported": preds.astype(bool)
    })

    submission.to_csv("submission.csv", index=False)
    print("Created submission.csv with", submission.shape[0], "rows.")

if __name__ == "__main__":
    main()



# %%




