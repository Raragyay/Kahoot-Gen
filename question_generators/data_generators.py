from functools import reduce


async def syn_ant_set(df):
    return reduce(set.union, df['French'], reduce(set.union, df['Antonym']))

async def english_set(df):
    return set(df['English'])
