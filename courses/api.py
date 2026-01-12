from ninja import Router
from typing import List
from courses.schemas import CourseOut, CourseIn, CourseUpdate, CourseVideoOut, EnrollmentIn
from services.course_service import CourseService
from ninja_jwt.authentication import JWTAuth
from django.shortcuts import get_object_or_404
from courses.models import Enrollment, Course

router = Router(tags=["Plataforma de Cursos Gratuitos - SME-SP"])

#Lista os cursos disponiveis
@router.get("/",
            response=List[CourseOut],
            auth=None,
            summary="Lista todos os cursos disponíveis",
            description=
            """
            Lista todos os cursos disponíveis"

                Parâmetros:

                    - Nenhum

                Retorna:

                    200 - Uma Lista com todos os cursos disponíveis.
            """,)
def list_courses(request):
    return CourseService.list()

#Retorna um curso de acordo com o id
@router.get("/{course_id}", 
            response=CourseOut,
            auth=None,
            summary="Retorna um curso com base no ID",
            description=
            """
            Retorna os dados de um curso com base no ID"

                Parâmetros:

                    - course_id: ID do curso

                Retorna:

                    200 - Os dados de um curso.

                Erro: 
                    Not Found: No Course matches the given query.

            """,)
def get_course(request, course_id: int):
    return CourseService.get(course_id)

#Cria um curso
@router.post("/",
            response=CourseOut,
            auth=JWTAuth(),
            summary="Cria um novo curso",
            description=
            """
            Cria um novo curso

                Parâmetros:

                    - title: Título do curso
                    - description: Descrição do curso
                    - workload: Tempo de duração do curso
                    - published: Curso publicado ou não
                    - image_url": Imagem para o card do curso

                Retorna:

                    200 - Os dados de um curso.

                Erro: 
                    Unauthorized.

            """,)
def create_course(request, payload: CourseIn,):
    if not request.user.is_staff:
        return 403, {"detail": "Apenas admins"}
    return CourseService.create(payload.dict())

@router.put("/{course_id}",
            response=CourseOut,
            auth=JWTAuth(),
            summary="Atualiza os dados de um curso",
            description=
            """
            Atualiza os dados de um curso

                Parâmetros:
                    
                    - id: ID do curso
                    - title: Título do curso
                    - description: Descrição do curso
                    - workload: Tempo de duração do curso
                    - published: Curso publicado ou não
                    - image_url": Imagem para o card do curso

                Retorna:

                    200 - Os novos dados de um curso.

                Erro: 
                    Unauthorized.

            """,)
def update_course(request, course_id: int, payload: CourseUpdate):
    if not request.user.is_staff:
        return 403, {"detail": "Apenas admins"}

    return CourseService.update(
        course_id,
        payload.dict(exclude_unset=True)
        )

#Deleta um curso
@router.delete("/{course_id}",
            summary="Deleta um curso",
            description=
            """
            Deleta um curso"

                Parâmetros:
                    
                    - id: ID do curso

                Retorna:

                    200 - OK.

                Erro: 
                    Unauthorized.

            """,)
def delete_course(request, course_id: int):
    CourseService.delete(course_id)
    return {"success": True}

@router.get("/{course_id}/video", response=CourseVideoOut, auth=JWTAuth())
def get_course_video(request, course_id: int):
    course = get_object_or_404(Course, id=course_id)

    if not Enrollment.objects.filter(
        user=request.user,
        course=course
    ).exists():
        return 403, {"detail": "Você não está inscrito neste curso"}

    return {
        "id": course.id,
        "title": course.title,
        "video_url": course.video_url,
    }


@router.get("/my/", response=List[CourseOut], auth=JWTAuth())
def my_courses(request):
    enrollments = Enrollment.objects.filter(user=request.user).select_related("course")
    return [e.course for e in enrollments]

@router.post("/enroll/",summary="Matricula em um curso", auth=JWTAuth())
def enroll_course(request, payload: EnrollmentIn):
    course = get_object_or_404(Course, id=payload.course_id)

    enrollment, created = Enrollment.objects.get_or_create(
        user=request.user,
        course=course
    )

    if not created:
        return 200, {"detail": "Usuário já matriculado"}

    return {"success": True}