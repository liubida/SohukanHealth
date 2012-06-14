# -*- coding: utf-8 -*-
'''
Created on Jun 14, 2012

@author: liubida
'''

from boto.s3.connection import Location
import boto
#from django.conf import settings

s3 = None
bucket_pool = dict()

def build_connect_s3():
    global s3
    if s3 is None:
        s3 = boto.connect_s3('AKIAIXEPRIJSQA4A2KOA', 'rfUdPSAC2hXhHMGG0wXiHcxeuEpqybEGxn8xPYMy', is_secure=False)

    return s3


def get_or_create_bucket(bucket_name, policy='public-read', location=Location.DEFAULT):
    s3 = build_connect_s3()
    global bucket_pool
    if bucket_name in bucket_pool:
        bucket = bucket_pool[bucket_name]
    else:
        bucket = s3.lookup(bucket_name, validate=False)
        if not bucket:
            try:
                bucket = s3.create_bucket(bucket_name, policy=policy, location=location)
                bucket.set_canned_acl('public-read')
            except s3.provider.storage_create_error:
                print 'Bucket (%s) is owned by another user' % bucket_name
        bucket_pool[bucket_name] = bucket

    return bucket


def get_data_to_string(bucket_name, key_name):
    #get_contents_to_filename,get_file
    bucket = get_or_create_bucket(bucket_name)
    key = bucket.lookup(key_name)
    if not key:
        return None

    return key.get_contents_as_string()


def get_data_to_filename(bucket_name, key_name, filename):
    #get_contents_to_filename,get_file
    bucket = get_or_create_bucket(bucket_name)
    key = bucket.lookup(key_name)
    if not key:
        return None

    return key.get_contents_to_filename(filename)


def store_data_from_filename(bucket_name, key_name, path_source_file, metadata=None, headers=None, policy='public-read'):
    bucket = get_or_create_bucket(bucket_name, policy)
    key = bucket.new_key(key_name)
    key.set_contents_from_filename(path_source_file, headers=headers, policy=policy)
    if metadata:
        key.metadata.update(metadata)

    return key


def store_data_from_stream(bucket_name, key_name, stream, metadata=None, headers=None, policy='public-read'):
    bucket = get_or_create_bucket(bucket_name, policy)
    key = bucket.new_key(key_name)
    key.set_contents_from_stream(stream, headers=headers, policy=policy)
    if metadata:
        key.metadata.update(metadata)

    return key


def store_data_from_string(bucket_name, key_name, need_store_string, metadata=None, headers=None, policy='public-read'):
    bucket = get_or_create_bucket(bucket_name, policy)
    key = bucket.new_key(key_name)
    key.set_contents_from_string(need_store_string, headers=headers, policy=policy)
    if metadata:
        key.metadata.update(metadata)

    return key


def modify_metadata(bucket_name, key_name, metadata):
    bucket = get_or_create_bucket(bucket_name)
    key = bucket.lookup(key_name)
    if key:
        key.copy(bucket.name, key.name, metadata, preserve_acl=True)

    return key


def enable_logging(bucket_name, log_bucket_name, log_prefix=None):
    s3 = build_connect_s3()
    bucket = get_or_create_bucket(bucket_name)
    log_bucket = s3.lookup(log_bucket_name)
    log_bucket.set_as_logging_target()
    bucket.enable_logging(log_bucket, target_prefix=log_prefix)

    return None


def disable_logging(bucket_name):
    bucket = get_or_create_bucket(bucket_name)
    bucket.disable_logging()

    return None


def bucket_du(bucket_name):
    bucket = get_or_create_bucket(bucket_name)
    total_bytes = 0
    if bucket:
        for key in bucket:
            total_bytes += key.size

    return total_bytes


def get_expire_data_url(bucket_name, key_name, expires_seconds):#该URL地址有过期时间
    s3 = build_connect_s3()
    url = s3.generate_url(expires_seconds, 'GET', bucket_name, key_name)
    if False:
        url = url.replace('s3.sce.sohu.com', 's3.itc.cn')
    
    return url


def get_data_url(bucket_name, key_name):
    if False:
        domain = 's3.amazonaws.com'
    else:
        domain = 's3.itc.cn'
    url = 'http://%s.%s/%s' % (bucket_name, domain, key_name)

    return url


def set_bucket_acl(bucket_name, policy):
    '''
    POLICY: 'private', 'public-read','public-read-write', 
    'authenticated-read', 'bucket-owner-read', 'bucket-owner-full-control'
    '''
    bucket = get_or_create_bucket(bucket_name, policy)
    bucket.set_acl(policy)
    
    return None


def get_bucket_acl(bucket_name):
    bucket = get_or_create_bucket(bucket_name)

    return bucket.get_acl()


if __name__ == '__main__':
    bucket_name = 'sohukan'
    key_name = 'bookmark-30'
    expires_seconds = 86400
    print get_expire_data_url(bucket_name, key_name, expires_seconds)
