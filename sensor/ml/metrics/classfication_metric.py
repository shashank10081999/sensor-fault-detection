from sensor.entity.artifact_entity import ClassficationMetricArtifact
from sklearn.metrics import f1_score , precision_score , recall_score


def get_classification_metrics(y_true,y_predicted) -> ClassficationMetricArtifact:
    try:
        model_f1_score = f1_score(y_true  , y_predicted)
        model_precision_score = precision_score(y_true  , y_predicted)
        model_recall_score = recall_score(y_true , y_predicted)

        classfication_metrics =  ClassficationMetricArtifact(f1_score= model_f1_score , precision_score= model_precision_score , recall_score= model_recall_score)

        return classfication_metrics
    except Exception as e:
        raise e


