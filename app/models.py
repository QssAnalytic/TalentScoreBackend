import environ, os, ast
from cryptography.fernet import Fernet
from django.db import models
from django.utils.text import slugify



class Answer(models.Model):
    questionIdd = models.ForeignKey(
        "app.Question", on_delete=models.CASCADE, related_name='answers')
    answer_title = models.CharField(max_length=100, null=True, blank=True)
    sub_answer_question = models.CharField(max_length=150, blank=True, null=True)
    answer_weight = models.CharField(max_length=150,  null=True, blank=True)
    answer_weight_for_hashing = models.CharField(max_length=150, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    answer_dependens_on = models.ForeignKey('self', on_delete=models.PROTECT,
                                             null=True,
                                               blank=True)
    stage_fit = models.OneToOneField('app.Stage', on_delete=models.PROTECT, null=True,blank=True)
    answer_weight_store = models.JSONField(blank=True, null=True)
    class Meta:
        verbose_name = 'Answer'
        verbose_name_plural = 'Answers'


    def save(self, *args, **kwargs):
        env = environ.Env()
        environ.Env.read_env()
        hash_key = ast.literal_eval(env("hash_key"))
        cipher = Fernet(hash_key)
        if self.answer_weight_for_hashing!=None:

            self.answer_weight = cipher.encrypt(self.answer_weight_for_hashing.encode())
        return super().save(*args, **kwargs)

    def get_stage_slug(self):
        if self.stage_fit is not None:
            return self.stage_fit.slug
        return None
    

    def __str__(self):
        if self.questionIdd_id:
            return "answer={}; question={}".format(self.answer_title, self.questionIdd.question_title)
        else:
            return "answer={}; question=None".format(self.answer_title)


class SubAnswer(models.Model):
    answer = models.ForeignKey('app.Answer', on_delete = models.CASCADE, related_name='subanswers')
    answer_title = models.CharField(max_length=150)
    sub_answer_weight = models.CharField(max_length=150,  null=True, blank=True)
    answer_weight= models.CharField(max_length=150, blank=True, null=True)

    def save(self, *args, **kwargs):
        env = environ.Env()
        environ.Env.read_env()
        hash_key = ast.literal_eval(env("hash_key"))
        cipher = Fernet(hash_key)
        if self.answer_weight==None:
            self.answer_weight = cipher.encrypt(self.sub_answer_weight.encode())
        return super().save(*args, **kwargs)
    

class Question(models.Model):

    question_title = models.CharField(verbose_name='question', max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    stage=models.ForeignKey('app.Stage', related_name = 'questions', on_delete=models.CASCADE)
    question_dependens_on_answer = models.ForeignKey('app.Answer', related_name = 'questions', blank=True,null=True, on_delete=models.CASCADE)
    question_type = models.CharField(max_length=50, blank=True, null=True)
    question_dependens_on_question = models.ForeignKey('self', blank=True, null=True, related_name='question_depend', on_delete=models.CASCADE)
    question_index = models.IntegerField(blank=True, null=True)
    class Meta:
        verbose_name = 'Question'
        verbose_name_plural = 'Questions'
    
        ordering = ['stage__stage_name', 'question_index']

    def __str__(self):
        
        return self.question_title
    
class Stage(models.Model):
    stage_name = models.CharField(max_length = 150)
    parent=models.ForeignKey('self', blank=True, null=True, related_name='stage_children', on_delete=models.CASCADE)
    slug = models.SlugField(max_length=100, blank=True)
    stage_index = models.IntegerField(blank=True, null=True)
    #stage_dependens_on = models.ForeignKey('app.Answer', on_delete=models.CASCADE, null=True, blank=True)
    def __str__(self):
        return self.stage_name
    
    class Meta:
        ordering = ['stage_index']
    

    def save(self, *args, **kwargs):
        if self.stage_name:
            self.slug=slugify(self.stage_name.replace('ı','i').replace('ə','e').replace('ö','o').replace('ü','u').replace('ç','c')\
                              .replace("I", "I").replace('Ə','E').replace('Ö','O').replace('Ü','U').replace('Ç','C'))
            
        return super().save(*args, **kwargs)


