from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User

import utils

from voting.models import Vote
from tagging.models import Tag

class RecommenderManager(models.Manager):

    MIN_RECOMMENDATION_VALUE = 0
    MIN_SIMILARITY_VALUE = 0.25
    MIN_CONTENT_BASED_RECOMMENDATION_VALUE = 0.25
    
    def get_best_items_for_user(self, user, user_list, item_list, min_value=MIN_RECOMMENDATION_VALUE):
        user_item_matrix = self.create_matrix(user_list, item_list)

        recs = utils.get_usb_recommendations(user.id, user_item_matrix)
        recs.sort(reverse=True)
        
        ctype = ContentType.objects.get_for_model(item_list[0])
        items = [(value,ctype.get_object_for_this_type(id = rec)) for value,rec in recs if value>min_value]
        return items
        
    def get_similar_users(self, user, user_list, item_list, min_value=MIN_SIMILARITY_VALUE):
        user_item_matrix = self.create_matrix(user_list, item_list)
        sim_list = []
        for other in user_list:
            if user==other:continue
            sim=utils.distance_matrix_p1_p2(user_item_matrix[user.id],user_item_matrix[other.id]) #returns a 0..1 value
            if sim>min_value:
                sim_list.append((sim,other))
            
        sim_list.sort(reverse=True)
        return sim_list

    def get_best_users_for_item(self, item, user_list, item_list, min_value=MIN_RECOMMENDATION_VALUE):
        user_item_matrix = self.create_matrix(user_list, item_list)
        item_user_matrix = self.rotate_matrix(user_item_matrix)

        recs = utils.get_usb_recommendations(item.id, item_user_matrix)
        recs.sort(reverse=True)

        users = [(value,User.objects.get(id = rec)) for value,rec in recs if value>min_value]
        
        return users
    
    def get_similar_items(self, item, user_list, item_list, min_value=MIN_SIMILARITY_VALUE):
        user_item_matrix = self.create_matrix(user_list, item_list)
        item_user_matrix = self.rotate_matrix(user_item_matrix)
        sim_list = []
        for other in item_list:
            if item==other:continue
            sim=utils.distance_matrix_p1_p2(item_user_matrix[item.id],item_user_matrix[other.id]) #returns a 0..1 value
            if sim>min_value:
                sim_list.append((sim,other))
            
        sim_list.sort(reverse=True)
        return sim_list
        
    def create_matrix(self, users, items):
        user_item_matrix = {}
        for user in users:
            votes_for_user = Vote.objects.get_for_user_in_bulk(items, user)
            user_item_matrix[user.id] = votes_for_user
        
        return user_item_matrix
    
    def rotate_matrix(self, matrix):
        rotated_matrix = {}
        for user in matrix:
            for item in matrix[user]:
                rotated_matrix.setdefault(item,{})
                rotated_matrix[item][user]=matrix[user][item]
        return rotated_matrix
        
# Content Based Recommendations
    def get_content_based_recs(self, user, tagged_items, min_value=MIN_CONTENT_BASED_RECOMMENDATION_VALUE):
        ''' For a given user tags and a dicc of item tags, returns the distances between the user and the items
            >>> eng=RecommenderManager()
            >>> user_tags=['a','b','c','d']
            >>> tag_matrix={}
            >>> tag_matrix['it1']=['z','a','c']
            >>> tag_matrix['it2']=['b','c']
            >>> tag_matrix['it3']=['a','r','t','v']
            >>> eng.get_content_based_recs(user_tags,tag_matrix)
            [(7.5, 'it1'), (10.0, 'it2'), (5.0, 'it3')]
        '''

        item_tag_matrix = {}
        for item in tagged_items:
            item_tag_matrix[item] = Tag.objects.get_for_object(item)
        
        user_tags = Tag.objects.get_for_object(user)
        
        recs = []
        for item,item_tags in item_tag_matrix.items():
            sim = utils.tanamoto2(item_tags, user_tags)
            if sim>=min_value:
                recs.append((sim, item))
                
        return recs

# Clustering methods
    def cluster_users(self, users, items, cluster_count=2):
        user_item_matrix = self.create_matrix(users, items)
        return utils.kcluster(user_item_matrix, items, cluster_count)

    def cluster_items(self, users, items, cluster_count=2):
        user_item_matrix = self.create_matrix(users, items)
        item_user_matrix = self.rotate_matrix(user_item_matrix)
        return utils.kcluster(item_user_matrix, users, cluster_count)
