
<form method="POST" action="/login/" class="form-horizontal">
    {{ form.hidden_tag() }}
    {% for field in form if field.type != 'CSRFTokenField' %}
    <div class="control-group">
        <label class="control-label" for="{{ field.id }}">{{ field.label }}</label>
        <div class="controls">{{ field }}</div>
        {% if field.errors %}
        <ul>
            {% for error in field.errors %}
            <li>{{ error }}</li>
            {% endfor %}
        </ul>
        {% endif %}
    </div>
    {% endfor %}
    <div class="control-group">
        <div class="controls">
            <input type="checkbox" name="remember_me" value='yes' id="remember_me" />
            <label for="remember_me">Remember me</label>
            <br />
            <input type="submit" class="btn" value="Sign in" />
        </div>
    </div>
</form>
