import json
from shroomdk import ShroomDK
from datetime import datetime


def convert_records_to_dict(sdk_records):
   
    data = {}
    if sdk_records is not None:
        data = sdk_records[0]
    return data



def get_ethereum_sales_data_dynamic_token_and_address(collection_name, nft_asset_id):
   

    sdk = ShroomDK("0aa823ca-fc7c-485a-9412-4d96b04e54be")
    sql_query = f""" 
       SELECT a.*, b.price as last_sale
        FROM (
        SELECT x.nft_asset_id,
        COUNT (DISTINCT tx_group_id) as num_sales,
        avg(total_sales_amount/number_of_nfts) as average_price
        FROM flipside_prod_db.algorand.nft_sales x
        LEFT JOIN flipside_prod_db.algorand.nft_asset y
        ON x.nft_asset_id = y.nft_asset_id
        WHERE collection_name = ('{collection_name}')
        GROUP BY x.nft_asset_id) a
        LEFT JOIN (
        SELECT nft_asset_id, total_sales_amount/number_of_nfts as price, rank
        FROM (
            SELECT x.*,y.collection_name, rank()over(partition by x.nft_asset_id ORDER BY block_timestamp DESC) as rank
            FROM flipside_prod_db.algorand.nft_sales x
            LEFT JOIN flipside_prod_db.algorand.nft_asset y
            ON x.nft_asset_id = y.nft_asset_id
            WHERE collection_name = ('{collection_name}')
                )
        WHERE rank = 1
                ) b
        ON a.nft_Asset_id = b.nft_asset_id
        where a.nft_Asset_id = {nft_asset_id}
    """

    result = sdk.query(sql_query).records
    data = {}
    if result is not None:
        data = result[0]
    return data



def get_nft_sales_eth(address, token_id):
    """ NFT sales history"""

    sdk = ShroomDK("0aa823ca-fc7c-485a-9412-4d96b04e54be")
    sql_query = f"""
    SELECT block_number, date_trunc('day',block_timestamp) as date, buyer_address, seller_address, currency_symbol, price, tokenid, project_name AS project_name, platform_name
    FROM ethereum.core.ez_nft_sales
    WHERE nft_address = lower('{address}') and tokenid = {token_id}
    ORDER BY date
    """

    result = sdk.query(sql_query)

    sales_price= []
    index = 0
    if result.records is not None:
        for record in result.records:

            sales_price.append({})
            py_date = datetime.strptime(record['date'][:19], '%Y-%m-%d %H:%M:%S')
            formatted_date = py_date.strftime('%m/%d/%Y')

            sales_price[index]['DATE'] = formatted_date
            sales_price[index]['PRICE'] = record['price']
            
            index += 1
    return [json.dumps(sales_price), convert_records_to_dict(sdk.query(sql_query).records)]


def get_nft_sales_algorand(nft_asset_id):
    """ NFT sales history"""

    sdk = ShroomDK("0aa823ca-fc7c-485a-9412-4d96b04e54be")
    sql_query = f"""
        SELECT date_trunc('day', a.block_timestamp) as date, a.tx_group_id, a.nft_marketplace AS marketplace, 
                    a.purchaser AS buyer, a.nft_asset_id AS token, b.collection_name AS collection, total_sales_amount AS price
        FROM flipside_prod_db.algorand.nft_sales a
        LEFT JOIN flipside_prod_db.algorand.nft_asset b
        ON a.nft_asset_id = b.nft_asset_id
        WHERE a.nft_asset_id = '{nft_asset_id}' 
    """

    result = sdk.query(sql_query)

    sales_price= []
    index = 0
    if result.records is not None:
        for record in result.records:

            sales_price.append({})
            py_date = datetime.strptime(record['date'][:19], '%Y-%m-%d %H:%M:%S')
            formatted_date = py_date.strftime('%m/%d/%Y')

            sales_price[index]['DATE'] = formatted_date
            sales_price[index]['PRICE'] = record['price']
            
            index += 1
    return [json.dumps(sales_price), convert_records_to_dict(sdk.query(sql_query).records)]


def get_nft_ethereum_meta_data(address, token_id):
    """ """

    sdk = ShroomDK("0aa823ca-fc7c-485a-9412-4d96b04e54be")
    sql_query = f"""
        SELECT *
        FROM ethereum.core.dim_nft_metadata
        where contract_address = lower('{address}')
        AND token_id = {token_id}
    """

    result = sdk.query(sql_query)

    return convert_records_to_dict(result.records)



def get_nft_image_url(nft_asset_id):
    """ """

    sdk = ShroomDK("0aa823ca-fc7c-485a-9412-4d96b04e54be")
    sql_query = f"""
       SELECT nft_url, nft_asset_id
        FROM algorand.nft.ez_nft_asset
        WHERE nft_asset_id = '{nft_asset_id}'
    """

    result = sdk.query(sql_query)
    data = ''
    nft_is_exist = False
    if result.records:
        for a in result.records:
            data = a['nft_url'][7:]
     
    return data


def get_nft_ethereum_meta_data_with_dynamic_address(address):
    """ """

    sdk = ShroomDK("0aa823ca-fc7c-485a-9412-4d96b04e54be")
    sql_query = f"""
        SELECT *
        FROM ethereum.core.dim_nft_metadata
        where contract_address = lower('{address}')
    """

    result = sdk.query(sql_query)

    return result.records

def get_activity_for_ethereum(address, token_id):
    """
    """
    sdk = ShroomDK("0aa823ca-fc7c-485a-9412-4d96b04e54be")
    sql_query = f"""
        SELECT 'sale' as label,
        block_number, date_trunc('day',block_timestamp) as date, buyer_address, seller_address, currency_symbol, price, tokenid, project_name, platform_name, tx_hash
            FROM ethereum.core.ez_nft_sales
        WHERE nft_address = lower('{address}') and tokenid = {token_id}
        UNION
        SELECT 'mint' as label,
        block_number, date_trunc('day',block_timestamp) as date, nft_to_address as buyer_address, '' as seller_address, 'ETH' as currency_symbol, mint_price_eth as price, tokenid, project_name, '' as platform_name,tx_hash
        FROM ethereum.core.ez_nft_mints    
        WHERE nft_address = lower('{address}') and tokenid = {token_id}
        UNION
        SELECT 'transfer' as label,
        block_number, date_trunc('day',block_timestamp) as date, nft_to_address as buyer_address, nft_from_address as seller_address, '' as currency_symbol, '0' as price, tokenid, project_name, '' as platform_name,tx_hash
        FROM ethereum.core.ez_nft_transfers    
        WHERE nft_from_address != '0x0000000000000000000000000000000000000000'
        AND nft_address = lower('{address}') and tokenid = {token_id}
        

        ORDER BY block_number desc
    """

    result = sdk.query(sql_query)

    return result.records


def get_activity_for_algorand(nft_asset_id):
    """
    """
    sdk = ShroomDK("0aa823ca-fc7c-485a-9412-4d96b04e54be")
    sql_query = f"""
        SELECT 'sale' as label,
            block_id, date_trunc('day',block_timestamp) as date, purchaser as buyer_address, 'ALGO' as currency_symbol, total_sales_amount/number_of_nfts as price, x.nft_asset_id, y.collection_name, nft_marketplace as platform_name, tx_group_id
        FROM flipside_prod_db.algorand.nft_sales x
        LEFT JOIN flipside_prod_db.algorand.nft_asset y
        ON x.nft_asset_id = y.nft_asset_id
        WHERE x.nft_asset_id = {nft_asset_id} 
    """

    result = sdk.query(sql_query)

    return result.records

def get_box_plot_data_for_a_collection_algorand(collection_name):

    sdk = ShroomDK("0aa823ca-fc7c-485a-9412-4d96b04e54be")
    sql_query = f"""
       WITH nfts as (
        SELECT nft_asset_id
        FROM flipside_prod_db.algorand.nft_asset
                WHERE collection_name = '{collection_name}'
        ),
        sales_data AS (
                SELECT 
                block_id, date_trunc('week',block_timestamp) as date, 'algo' as currency_symbol, total_sales_amount/number_of_nfts as price 
                FROM flipside_prod_db.algorand.nft_sales
                WHERE nft_asset_id IN (SELECT nft_asset_id FROM nfts)
                )

                SELECT a.date,
                    MIN(s.price) AS minimum,
                    AVG(q1) AS q1,
                    AVG(median) AS median,
                    AVG(q3) AS q3,
                    MAX(s.price) AS maximum
                FROM (
                SELECT date,
                    PERCENTILE_CONT(0.25) WITHIN GROUP 
                        (ORDER BY price) OVER (PARTITION BY date) AS q1,
                    MEDIAN(price) OVER (PARTITION BY date) AS median,
                    PERCENTILE_CONT(0.75) WITHIN GROUP 
                        (ORDER BY price) OVER (PARTITION BY date) AS q3
                FROM sales_data
                )a
                LEFT JOIN sales_data s
                ON s.date = a.date
                GROUP BY 1
                ORDER BY date
    """

    result = sdk.query(sql_query)

    return result.records