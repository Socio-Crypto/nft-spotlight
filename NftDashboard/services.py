import json
from datetime import datetime
from flipside import Flipside

def convert_records_to_dict(sdk_records):
   
    data = {}
    if sdk_records is not None:
        data = sdk_records[0]
    return data

def get_result_from_query(sql_query):
    
    flipside = Flipside("693499b7-8af2-4914-a193-5d13085ee9be", "https://api-v2.flipsidecrypto.xyz")
    result = flipside.query(sql_query)

    activity_data = {}
    if result.records is not None:
        activity_data = result.records
    return activity_data


def get_ethereum_sales_data_dynamic_token_and_address(project_name, token_id):
   

    sql_query = f""" 
       SELECT a.*, b.price as last_sale, b.price_usd as last_price_usd
        FROM
        (SELECT tokenid,
        count(DISTINCT tx_hash) as num_sales,
        avg(price_usd) as avg_price_usd,
        avg(price) as average_price
        FROM ethereum.core.ez_nft_sales
        WHERE project_name = '{project_name}' and tokenid = '{token_id}'
        GROUP by
        tokenid) a
        LEFT JOIN (
        SELECT tokenid,
        price,price_usd, rank
        FROM(
        SELECT *,
        rank()over(partition by tokenid ORDER BY block_timestamp DESC) as rank
        FROM ethereum.core.ez_nft_sales
        WHERE project_name = '{project_name}' and tokenid = '{token_id}'
        )
        WHERE rank = 1
        ) b
        ON a.tokenid = b.tokenid
    """
    result = get_result_from_query(sql_query)
    data = {}
    if result is not None:
        data = result[0]
    return data


def get_nft_sales_eth(project_name, token_id):
    """ NFT sales history"""

    sql_query = f"""
    SELECT block_number, date_trunc('day',block_timestamp) as date, buyer_address, seller_address, currency_symbol, price, tokenid, project_name AS project_name, platform_name
    FROM ethereum.core.ez_nft_sales
    WHERE project_name = '{project_name}' and tokenid = '{token_id}'
    ORDER BY date
    """

    result = get_result_from_query(sql_query)

    sales_price= []
    index = 0
    # if result.records is not None:
    for record in result:

        sales_price.append({})
        py_date = datetime.strptime(record['date'][:19], '%Y-%m-%dT%H:%M:%S')
        formatted_date = py_date.strftime('%m/%d/%Y')

        sales_price[index]['DATE'] = formatted_date
        sales_price[index]['PRICE'] = record['price']
        
        index += 1
    return [json.dumps(sales_price), convert_records_to_dict(get_result_from_query(sql_query))]


def get_nft_sales_algorand(nft_asset_id):
    """ NFT sales history"""

    sql_query = f"""
        SELECT date_trunc('day', a.block_timestamp) as date, a.tx_group_id, a.nft_marketplace AS marketplace, 
                    a.purchaser AS buyer, a.nft_asset_id AS token, b.collection_name AS collection, total_sales_amount AS price
        FROM flipside_prod_db.algorand.nft_sales a
        LEFT JOIN flipside_prod_db.algorand.nft_asset b
        ON a.nft_asset_id = b.nft_asset_id
        WHERE a.nft_asset_id = '{nft_asset_id}' 
    """

    result = get_result_from_query(sql_query)

    sales_price= []
    index = 0

    for record in result:

        sales_price.append({})
        py_date = datetime.strptime(record['date'][:19], '%Y-%m-%d %H:%M:%S')
        formatted_date = py_date.strftime('%m/%d/%Y')

        sales_price[index]['DATE'] = formatted_date
        sales_price[index]['PRICE'] = record['price']
        
        index += 1
    return [json.dumps(sales_price), convert_records_to_dict(get_result_from_query(sql_query))]


def get_nft_ethereum_meta_data(project_name, nft_asset_id):
    """ """

    sql_query = f"""
        SELECT *
        FROM ethereum.nft.dim_nft_metadata
        where  project_name = '{project_name}' and token_id = '{nft_asset_id}'
    """

    result = get_result_from_query(sql_query)

    return convert_records_to_dict(result)



def get_nft_image_url(project_name, nft_asset_id):
    """ """

    sql_query = f"""

        Select 
            image_url 
        from ethereum.nft.dim_nft_metadata
        where project_name = '{project_name}' and token_id = '{nft_asset_id}'
    """

    result = get_result_from_query(sql_query)
    data = ''
    nft_is_exist = False
    # if result.records:
    for a in result:
        data = a['image_url'][7:]
     
    return data


def get_nft_ethereum_meta_data_with_dynamic_address(project_name):
    """ """

    sql_query = f"""
        SELECT *
        FROM ethereum.core.dim_nft_metadata
        where project_name = '{project_name}' 
    """

    result = get_result_from_query(sql_query)

    return result


def get_activity_for_ethereum(project_name, token_id):
    """
    """
    sql_query = f"""
        SELECT 'sale' as label,
        block_number, date_trunc('day',block_timestamp) as date, buyer_address, seller_address, currency_symbol, price, tokenid, project_name, platform_name, tx_hash
            FROM ethereum.core.ez_nft_sales
        WHERE project_name = '{project_name}' and tokenid = '{token_id}'
        UNION
        SELECT 'mint' as label,
        block_number, date_trunc('day',block_timestamp) as date, nft_to_address as buyer_address, '' as seller_address, 'ETH' as currency_symbol, mint_price_eth as price, tokenid, project_name, '' as platform_name,tx_hash
        FROM ethereum.core.ez_nft_mints    
        WHERE project_name = '{project_name}' and tokenid = '{token_id}'
        UNION
        SELECT 'transfer' as label,
        block_number, date_trunc('day',block_timestamp) as date, nft_to_address as buyer_address, nft_from_address as seller_address, '' as currency_symbol, '0' as price, tokenid, project_name, '' as platform_name,tx_hash
        FROM ethereum.core.ez_nft_transfers    
        WHERE nft_from_address != '0x0000000000000000000000000000000000000000'
        AND project_name = '{project_name}' and tokenid = '{token_id}'
        

        ORDER BY block_number desc
    """

    result = get_result_from_query(sql_query)

    return result


def get_activity_for_algorand(nft_asset_id):
    """
    """
    sql_query = f"""
        SELECT 'sale' as label,
            block_id, date_trunc('day',block_timestamp) as date, purchaser as buyer_address, 'ALGO' as currency_symbol, total_sales_amount/number_of_nfts as price, x.nft_asset_id, y.collection_name, nft_marketplace as platform_name, tx_group_id
        FROM flipside_prod_db.algorand.nft_sales x
        LEFT JOIN flipside_prod_db.algorand.nft_asset y
        ON x.nft_asset_id = y.nft_asset_id
        WHERE x.nft_asset_id = {nft_asset_id} 
    """

    result = get_result_from_query(sql_query)

    return result

def get_box_plot_data_for_a_collection_algorand(collection_name):


    sql_query = f"""
        WITH sales_data AS (
        SELECT
            BLOCK_NUMBER,
            date_trunc('week', block_timestamp) as date,
            CURRENCY_SYMBOL,
            PRICE as price
        FROM
            ethereum.nft.ez_nft_sales
        WHERE
            project_name = '{collection_name}'
        )
        SELECT
        a.date,
        MIN(s.price) AS minimum,
        AVG(q1) AS q1,
        AVG(median) AS median,
        AVG(q3) AS q3,
        MAX(s.price) AS maximum
        FROM
        (
            SELECT
            date,
            PERCENTILE_CONT(0.25) WITHIN GROUP (
                ORDER BY
                price
            ) OVER (PARTITION BY date) AS q1,
            MEDIAN(price) OVER (PARTITION BY date) AS median,
            PERCENTILE_CONT(0.75) WITHIN GROUP (
                ORDER BY
                price
            ) OVER (PARTITION BY date) AS q3
            FROM
            sales_data
        ) a
        LEFT JOIN sales_data s ON s.date = a.date
        GROUP BY
        1
        ORDER BY
        date
    """

    result = get_result_from_query(sql_query)

    return result



def get_weekly_collection_average_eth(collection_name):

    sql_query = f"""
        WITH sales_data AS (
        SELECT
            BLOCK_NUMBER,
            date_trunc('week', block_timestamp) as date,
            CURRENCY_SYMBOL,
            PRICE as price
        FROM
            ethereum.nft.ez_nft_sales
        WHERE
            project_name = '{collection_name}'
        )
        SELECT
        a.date,
        AVG(average) AS average
        FROM
        (
            SELECT
            date,
            AVG(price) OVER (PARTITION BY date) AS average
            FROM
            sales_data
        ) a
        LEFT JOIN sales_data s ON s.date = a.date
        GROUP BY
        1
        ORDER BY
        date
    """

    result = get_result_from_query(sql_query)

    return result


def check_nft_in_flipside(collection_name, token_id):

    sql_query = f"""
        SELECT
        *
        FROM
        ethereum.nft.ez_nft_sales
        WHERE
        project_name = '{collection_name}' and tokenid = '{token_id}'
    """

    result = get_result_from_query(sql_query)

    if len(result)== 0:
        return False
    else: 
        return True
