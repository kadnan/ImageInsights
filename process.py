import cv2
import pymysql

rgb2hex = lambda r, g, b: '#%02x%02x%02x' % (r, g, b)


def get_links():
    ids = []
    records = []

    try:
        if connection is not None:
            with connection.cursor() as cursor:
                sql = 'SELECT * FROM images where status = 0 LIMIT {}'.format(LIMIT)
                cursor.execute(sql)
                records = cursor.fetchall()

                for record in records:
                    ids.append(record['id'])
                # Update the status
                sql = 'UPDATE images set status = 1 where id IN (%s)' % ','.join('%s' for i in ids)
                cursor.execute(sql, ids)
                connection.commit()
    except Exception as ex:
        print('Error while fetching jobs')
        print(ex)
    finally:
        return records


def process_image(image_name):
    color_count = {}
    print('Processing the image {}'.format(image_name))
    path = 'website/static/uploaded_images/' + image_name

    image = cv2.imread(path)

    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            (b, g, r) = image[i, j]
            h_value = rgb2hex(r, g, b)

            if h_value in color_count:
                color_count[h_value] += 1
            else:
                color_count[h_value] = 1
    return color_count


def store_image_details(img_name, image_id, c_count):
    print('Storing the image  Details of {}'.format(img_name))

    if connection is not None:
        with connection.cursor() as cursor:
            # insert colors
            if len(c_count) > 0:
                for c in c_count:
                    sql = 'INSERT INTO image_colors(image_id,color_code,code_frequency) VALUES (%s,%s,%s)'
                    cursor.execute(sql, (image_id, c, c_count[c]))
        connection.commit()
    return image_id


def get_connection():
    connection = None
    try:
        connection = pymysql.connect(host='localhost',
                                     user='root',
                                     password='root',
                                     db='imginsights',
                                     cursorclass=pymysql.cursors.DictCursor)
        print('Connected')
    except Exception as ex:
        print(str(ex))
    finally:
        return connection


if __name__ == '__main__':
    LIMIT = 2
    processed_ids = []

    connection = get_connection()
    images = get_links()

    for image in images:
        image_pixel_data = process_image(image['name'])
        processed_ids.append(store_image_details(image['name'], image['id'], image_pixel_data))

    if len(processed_ids) > 0:
        ids = ','.join(map(str, processed_ids))

        if connection is not None:
            with connection.cursor() as cursor:
                sql = "UPDATE images SET status = 3 where id IN ({})".format(ids)
                print(sql)
                cursor.execute(sql)
                connection.commit()
