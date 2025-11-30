class XTable extends HTMLElement {
  constructor() {
    super();

    this._fields = {};
  }

  connectedCallback() {
    var observer = new MutationObserver(() => {
      observer.disconnect();

      var query = document.createElement('div');
      query.className = 'query';

      var result = document.createElement('code');

      var fields = document.createElement('div');
      fields.className = 'fields';

      for (var child of [...this.children]) {
        this.removeChild(child);

        var field = document.createElement('div');

        field.appendChild(child);

        if (child.tagName == 'INPUT') {
          child.placeholder = child.name.replaceAll('_', ' ');
          if (child.type == 'checkbox') {
            var label = document.createElement('label');
            label.for = child.id = Math.random();
            label.innerText = child.placeholder;

            field.classList.add('checkbox');

            field.insertBefore(label, child);
          }
        }

        var constraints = document.createElement('div');
        constraints.className = 'constraints';

        if (child.hasAttribute('x-key'))
          constraints.innerHTML += '<span class="key">key</span>';
        if (child.hasAttribute('x-nocreate'))
          constraints.innerHTML += '<span class="serial">serial</span>';
        if (child.hasAttribute('x-noupdate'))
          constraints.innerHTML += '<span class="constant">constant</span>';
        if (child.hasAttribute('x-opt'))
          constraints.innerHTML += '<span class="optional">optional</span>';

        if (constraints.innerHTML)
          field.appendChild(constraints);

        fields.appendChild(field);
      };

      query.appendChild(fields);
      query.appendChild(result);

      var h2 = document.createElement('h2');
      h2.innerHTML = this.getAttribute('x-table').replaceAll('_', ' ');
      this.appendChild(h2);

      this.appendChild(query);

      var control = document.createElement('div');
      control.className = 'control';
      control.innerHTML = `
        <button>list all items</button>
        <div class="mode">
          <span>MODE</span>
          <div>
            <button>get</button>
            <button disabled>create</button>
            <button disabled>update</button>
          </div>
          <button>send</button>
        </div>
      `;

      this.appendChild(control);
    });

    observer.observe(this, { childList: true, subtree: true });
  }
}

customElements.define('x-table', XTable);
