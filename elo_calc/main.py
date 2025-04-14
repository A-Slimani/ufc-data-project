import pandas as pd

def get_fighters():
    pass

def elo_calculation(winner, loser, df_elo):
    # get elo from id
    w_data = df_elo.loc[df_elo['id'] == winner]
    l_data = df_elo.loc[df_elo['id'] == loser]
    w_elo = w_data['elo'].item()
    l_elo = l_data['elo'].item()

    # find higher / lower elo
    a = max(w_elo, l_elo)
    b = min(w_elo, l_elo)

    # TODO: caculate the k_factor based of the number of fights
    w_fight_count = w_data['fight_count'].item()
    l_fight_count = w_data['fight_count'].item()
    w_kfactor = 80
    l_kfactor = 80

    if w_fight_count > 5:
        w_kfactor = 50
    elif w_fight_count > 15:
        w_kfactor = 30
    elif w_fight_count > 25:
        w_kfactor = 20
   
    if l_fight_count > 5:
        l_kfactor = 50
    elif l_fight_count > 15:
        l_kfactor = 30
    elif l_fight_count > 25:
        l_kfactor = 20

    # caculate elo diff
    elo_result = (1 / (1 + 10 ** ((a - b) / 400)))

    # calculate new elo
    new_w_elo = round(w_elo + w_kfactor * (1 - elo_result))
    new_l_elo = round(l_elo + l_kfactor * (0 - elo_result))

    print(f"{w_data['full_name'].item()}:+{new_w_elo} -- {l_data['full_name'].item()}:-{new_l_elo}")

    return new_w_elo, new_l_elo 


def main():
    df_elo = pd.read_csv("./stg_fighters.csv")
    df_fights = pd.read_csv("./fact_fights.csv")

    df_elo = df_elo[['id', 'full_name', 'weight_class_description']]
    df_elo['elo'] = 1000
    df_elo['fight_count'] = 1 

    # just calculate by win / lose
    df_fights = df_fights[['event_id', 'r_fighter_id', 'r_fighter_status', 'b_fighter_id', 'b_fighter_status']]
    df_fights = df_fights.sort_values(by=['event_id'])

    for fight in df_fights.iterrows():
        r_fighter = fight[1]['r_fighter_id']
        r_status = fight[1]['r_fighter_status']
        b_fighter = fight[1]['b_fighter_id']
        b_status = fight[1]['b_fighter_status']

        if r_status == 'Win':
            n = elo_calculation(r_fighter, b_fighter, df_elo)
            df_elo.loc[df_elo['id'] == r_fighter, 'elo'] = n[0]
            df_elo.loc[df_elo['id'] == b_fighter, 'elo'] = n[1]
        elif b_status == 'Win':
            n = elo_calculation(b_fighter, r_fighter, df_elo)
            df_elo.loc[df_elo['id'] == r_fighter, 'elo'] = n[1]
            df_elo.loc[df_elo['id'] == b_fighter, 'elo'] = n[0]

        df_elo.loc[df_elo['id'] == r_fighter, 'fight_count'] += 1
        df_elo.loc[df_elo['id'] == b_fighter, 'fight_count'] += 1


    df_elo.to_csv("./elo_scores.csv", index=False)


if __name__ == "__main__":
    main()



