from wtforms import (
    PasswordField,  # Importing the field class for password inputs
    EmailField,  # Importing the field class for email inputs
    Form,  # Importing the base class for forms
    FileField,  # Importing the field class for file uploads
    validators,  # Importing validators for form fields
    SelectField,  # Importing the field class for dropdown/select inputs
    StringField,  # Importing the field class for string/text inputs
    TextAreaField,  # Importing the field class for multi-line text inputs
)


class CommentForm(Form):
    comment = TextAreaField(
        "Comment",
        [validators.Length(min=1, max=500), validators.InputRequired()]
    )


class ChangeProfilePictureForm(Form):
    newProfilePictureSeed = StringField(
        "ProfilePictureSeed",
        [validators.InputRequired()]
    )


class CreatePostForm(Form):
    postTitle = StringField(
        "Post Title",
        [validators.Length(min=4, max=75), validators.InputRequired()]
    )
    postTags = StringField(
        "Post Tags",
        [validators.Length(min=4, max=75), validators.InputRequired()]
    )
    postContent = TextAreaField(
        "Post Content",
        [validators.Length(min=20), validators.InputRequired()]
    )
    postBanner = FileField(
        "Post Banner",
        [validators.InputRequired()]
    )
    postCategory = StringField(
        "Post Category",
        [validators.Length(min=2), validators.InputRequired()]
    )


class VerifyUserForm(Form):
    code = StringField(
        "code",
        [validators.Length(min=4, max=4), validators.InputRequired()]
    )


class ChangeUserNameForm(Form):
    newUserName = StringField(
        "Username",
        [validators.Length(min=1, max=25), validators.InputRequired()]
    )


class SignUpForm(Form):
    userName = StringField(
        "Username",
        [validators.Length(min=1, max=25), validators.InputRequired()]
    )
    email = EmailField(
        "Email",
        [validators.Length(min=6, max=50), validators.InputRequired()]
    )
    password = PasswordField(
        "Password",
        [
            validators.Length(min=1),
            validators.InputRequired(),
        ]
    )
    passwordConfirm = PasswordField(
        "passwordConfirm",
        [
            validators.Length(min=1),
            validators.InputRequired()
        ]
    )


class LoginForm(Form):
    email = EmailField(
        "Email",
        [validators.Length(min=6, max=50), validators.InputRequired()]
    )
    password = PasswordField(
        "Password",
        [validators.Length(min=1), validators.InputRequired()]
    )


class ForgetForm(Form):
    email = EmailField(
        "Email",
        [validators.Length(min=6, max=50), validators.InputRequired()]
    )


class PasswordResetForm(Form):
    code = StringField(
        "code",
        [validators.Length(min=4, max=4), validators.InputRequired()]
    )
    password = PasswordField(
        "Password",
        [
            validators.Length(min=1),
            validators.InputRequired()
        ]
    )
    passwordConfirm = PasswordField(
        "passwordConfirm",
        [
            validators.Length(min=1),
            validators.InputRequired()
        ]
    )
