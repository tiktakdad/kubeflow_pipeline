import kfp
import kfp.components as comp
from kubernetes.client.models import V1SecurityContext
from kfp import dsl
@dsl.pipeline(
    name='tiktakdad-iris',
    description='tiktakdad iris test'
)

def soojin_pipeline():
    user = 1000
    add_p = dsl.ContainerOp(
        name="load iris data pipeline",
        image="tiktakdad/iris-preprocessing@sha256:9afcd31ddd4f9068f09201669915911ca9e4504f6f993f514d26418b6627959a",
        arguments=[
            '--data_path', './Iris.csv'
        ],
        file_outputs={'iris' : '/iris.csv'}
    )
    add_p.set_security_context(V1SecurityContext(run_as_user=user, run_as_group=0))

    ml = dsl.ContainerOp(
        name="training pipeline",
        image="tiktakdad/iris-training@sha256:5a316f66ad586d9494bc9b2b70225948337cbb1d1341e92fb8e83d70ff3f92d9",
        arguments=[
            '--data', add_p.outputs['iris']
        ]
    )
    ml.set_security_context(V1SecurityContext(run_as_user=user, run_as_group=0))

    ml.after(add_p)
    
if __name__ == "__main__":
    import kfp.compiler as compiler
    compiler.Compiler().compile(test_pipeline, __file__ + ".tar.gz")
