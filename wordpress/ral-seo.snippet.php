/**
 * RAL SEO — completamenti SEO per roccoandrealigorio.it
 *
 * Snippet PHP di WPCode (id 213), "Esegui ovunque". Lavora insieme allo snippet
 * "Blog – stile, intestazione e SEO articoli" (id 151), che stampa già:
 *  - articoli e pagina Blog: meta description, Open Graph, Twitter card, JSON-LD;
 *  - categorie: meta description, canonical, Open Graph, twitter:card.
 * Qui si aggiunge SOLO quello che manca, senza ripetere tag già presenti:
 *  - campi ral_seo_title / ral_seo_description / ral_seo_keyword (API REST, blog-automatico)
 *    e ral_seo_title come <title> dell'articolo;
 *  - pagina Blog: <link rel="canonical"> (anche sulle pagine successive /page/N/);
 *  - categorie: twitter:title, twitter:description, twitter:image;
 *  - tag: titolo, canonical, meta description, Open Graph e Twitter card completi;
 *  - archivi autore e data: canonical.
 */

add_action( 'init', function () {
	foreach ( array( 'ral_seo_title', 'ral_seo_description', 'ral_seo_keyword' ) as $chiave ) {
		register_post_meta( 'post', $chiave, array(
			'type'              => 'string',
			'single'            => true,
			'show_in_rest'      => true,
			'sanitize_callback' => 'sanitize_text_field',
			'auth_callback'     => function () {
				return current_user_can( 'edit_posts' );
			},
		) );
	}
} );

// URL definitivo di un archivio, compresa l'eventuale pagina /page/N/
function ral_seo_url_archivio( $base ) {
	$pagina = max( 1, (int) get_query_var( 'paged' ) );
	return $pagina > 1 ? get_pagenum_link( $pagina ) : $base;
}

// Stessa descrizione che lo snippet 151 usa per le categorie
function ral_seo_desc_termine( $termine ) {
	$desc = trim( wp_strip_all_tags( term_description( $termine ) ) );
	if ( ! $desc ) {
		$desc = 'Articoli su ' . $termine->name . ' dal blog di Rocco Andrea Ligorio, Software Engineer: guide pratiche su gestionali, Progressive Web App, automazioni e sicurezza.';
	}
	return $desc;
}

function ral_seo_meta( $chiave, $valore ) {
	if ( '' === (string) $valore ) {
		return '';
	}
	$attr = 0 === strpos( $chiave, 'twitter:' ) ? 'name' : 'property';
	return '<meta ' . $attr . '="' . esc_attr( $chiave ) . '" content="' . esc_attr( $valore ) . '" />' . "\n";
}

// Titoli: articolo (campo SEO) e tag (dopo lo snippet 151, priorità 30)
add_filter( 'pre_get_document_title', function ( $titolo ) {
	if ( is_singular( 'post' ) ) {
		$t = get_post_meta( get_queried_object_id(), 'ral_seo_title', true );
		return $t ? $t : $titolo;
	}
	if ( is_tag() ) {
		return single_tag_title( '', false ) . ': articoli | Rocco Andrea Ligorio';
	}
	return $titolo;
}, 40 );

add_action( 'wp_head', function () {
	$img = wp_get_attachment_image_url( 145, 'full' ); // immagine social predefinita del sito
	$out = '';

	if ( is_home() ) {
		// Pagina Blog: lo snippet 151 stampa già Open Graph e Twitter, manca il canonical
		$out .= '<link rel="canonical" href="' . esc_url( ral_seo_url_archivio( get_permalink( (int) get_option( 'page_for_posts' ) ) ) ) . '" />' . "\n";

	} elseif ( is_category() ) {
		// Categorie: lo snippet 151 stampa canonical, Open Graph e twitter:card
		$cat  = get_queried_object();
		$out .= ral_seo_meta( 'twitter:title', wp_get_document_title() );
		$out .= ral_seo_meta( 'twitter:description', ral_seo_desc_termine( $cat ) );
		$out .= ral_seo_meta( 'twitter:image', $img );

	} elseif ( is_tag() ) {
		// Tag: nessun altro snippet se ne occupa
		$tag    = get_queried_object();
		$url    = ral_seo_url_archivio( get_tag_link( $tag ) );
		$titolo = wp_get_document_title();
		$desc   = ral_seo_desc_termine( $tag );
		$out   .= '<meta name="description" content="' . esc_attr( $desc ) . '" />' . "\n";
		$out   .= '<link rel="canonical" href="' . esc_url( $url ) . '" />' . "\n";
		foreach ( array(
			'og:type'             => 'website',
			'og:locale'           => 'it_IT',
			'og:site_name'        => 'Rocco Andrea Ligorio',
			'og:url'              => $url,
			'og:title'            => $titolo,
			'og:description'      => $desc,
			'og:image'            => $img,
			'twitter:card'        => 'summary_large_image',
			'twitter:title'       => $titolo,
			'twitter:description' => $desc,
			'twitter:image'       => $img,
		) as $k => $v ) {
			$out .= ral_seo_meta( $k, $v );
		}

	} elseif ( is_author() ) {
		$out .= '<link rel="canonical" href="' . esc_url( ral_seo_url_archivio( get_author_posts_url( get_queried_object_id() ) ) ) . '" />' . "\n";

	} elseif ( is_date() ) {
		$base = is_day() ? get_day_link( get_query_var( 'year' ), get_query_var( 'monthnum' ), get_query_var( 'day' ) )
			: ( is_month() ? get_month_link( get_query_var( 'year' ), get_query_var( 'monthnum' ) ) : get_year_link( get_query_var( 'year' ) ) );
		$out .= '<link rel="canonical" href="' . esc_url( ral_seo_url_archivio( $base ) ) . '" />' . "\n";
	}

	if ( $out ) {
		echo "<!-- RAL SEO -->\n" . $out . "<!-- /RAL SEO -->\n";
	}
}, 3 );
