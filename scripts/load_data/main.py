import pandas as pd

if __name__ == "__main__":
    path = "data/recipes.csv"
    
    print("Downloading dataset to: ", path)    

    df = pd.read_csv("hf://datasets/datahiveai/recipes-with-nutrition/recipes-with-nutrition.csv")
    df.to_csv(path, index=False)

    print("Finished dataset")    
