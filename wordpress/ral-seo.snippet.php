/**
 * RAL SEO — metadati per l'indicizzazione degli articoli di roccoandrealigorio.it
 *
 * Da installare come snippet PHP in WPCode (Snippet di codice → Aggiungi snippet →
 * Codice personalizzato → tipo "PHP Snippet", posizione "Esegui ovunque"), poi Attiva.
 *
 * Cosa fa:
 *  - registra i campi ral_seo_title / ral_seo_description / ral_seo_keyword,
 *    scrivibili via API REST da blog-automatico;
 *  - negli articoli stampa: title ottimizzato, meta description, Open Graph,
 *    Twitter card e dati strutturati JSON-LD (BlogPosting);
 *  - in home page stampa meta description e Open Graph di base.
 * Se in futuro attivi un plugin SEO (All in One SEO, Yoast, Rank Math) lo snippet
 * si disattiva da solo per evitare tag doppi.
 */

if ( ! function_exists( 'ral_seo_plugin_attivo' ) ) {

	function ral_seo_plugin_attivo() {
		return defined( 'AIOSEO_VERSION' ) || defined( 'WPSEO_VERSION' ) || class_exists( 'RankMath' );
	}

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

	function ral_seo_descrizione( $post ) {
		$d = get_post_meta( $post->ID, 'ral_seo_description', true );
		if ( ! $d ) {
			$d = has_excerpt( $post ) ? get_the_excerpt( $post ) : wp_trim_words( wp_strip_all_tags( $post->post_content ), 30, '…' );
		}
		return trim( wp_strip_all_tags( $d ) );
	}

	// <title> personalizzato
	add_filter( 'pre_get_document_title', function ( $titolo ) {
		if ( ral_seo_plugin_attivo() || ! is_singular( 'post' ) ) {
			return $titolo;
		}
		$t = get_post_meta( get_queried_object_id(), 'ral_seo_title', true );
		return $t ? $t : $titolo;
	}, 20 );

	add_action( 'wp_head', function () {
		if ( ral_seo_plugin_attivo() ) {
			return;
		}
		$sito  = get_bloginfo( 'name' );
		$righe = array();

		if ( is_singular( 'post' ) ) {
			$post   = get_queried_object();
			$titolo = get_post_meta( $post->ID, 'ral_seo_title', true );
			$titolo = $titolo ? $titolo : get_the_title( $post );
			$desc   = ral_seo_descrizione( $post );
			$url    = get_permalink( $post );
			$img    = get_the_post_thumbnail_url( $post, 'full' );
			$kw     = get_post_meta( $post->ID, 'ral_seo_keyword', true );
			$tag    = wp_list_pluck( (array) get_the_tags( $post->ID ), 'name' );
			$parole = array_values( array_unique( array_filter( array_merge( array( $kw ), $tag ) ) ) );

			$righe[] = '<meta name="description" content="' . esc_attr( $desc ) . '">';
			$righe[] = '<meta property="og:locale" content="it_IT">';
			$righe[] = '<meta property="og:type" content="article">';
			$righe[] = '<meta property="og:title" content="' . esc_attr( $titolo ) . '">';
			$righe[] = '<meta property="og:description" content="' . esc_attr( $desc ) . '">';
			$righe[] = '<meta property="og:url" content="' . esc_url( $url ) . '">';
			$righe[] = '<meta property="og:site_name" content="' . esc_attr( $sito ) . '">';
			$righe[] = '<meta property="article:published_time" content="' . esc_attr( get_the_date( 'c', $post ) ) . '">';
			$righe[] = '<meta property="article:modified_time" content="' . esc_attr( get_the_modified_date( 'c', $post ) ) . '">';
			if ( $img ) {
				$righe[] = '<meta property="og:image" content="' . esc_url( $img ) . '">';
				$righe[] = '<meta property="og:image:width" content="1200">';
				$righe[] = '<meta property="og:image:height" content="630">';
			}
			$righe[] = '<meta name="twitter:card" content="' . ( $img ? 'summary_large_image' : 'summary' ) . '">';
			$righe[] = '<meta name="twitter:title" content="' . esc_attr( $titolo ) . '">';
			$righe[] = '<meta name="twitter:description" content="' . esc_attr( $desc ) . '">';

			$autore = array( '@type' => 'Person', 'name' => 'Rocco Andrea Ligorio', 'url' => home_url( '/' ) );
			$schema = array(
				'@context'         => 'https://schema.org',
				'@type'            => 'BlogPosting',
				'headline'         => wp_strip_all_tags( get_the_title( $post ) ),
				'description'      => $desc,
				'url'              => $url,
				'mainEntityOfPage' => array( '@type' => 'WebPage', '@id' => $url ),
				'datePublished'    => get_the_date( 'c', $post ),
				'dateModified'     => get_the_modified_date( 'c', $post ),
				'inLanguage'       => 'it-IT',
				'author'           => $autore,
				'publisher'        => $autore,
			);
			if ( $img ) {
				$schema['image'] = $img;
			}
			if ( $parole ) {
				$schema['keywords'] = implode( ', ', $parole );
			}
			$cat = get_the_category( $post->ID );
			if ( $cat ) {
				$schema['articleSection'] = $cat[0]->name;
			}
			$righe[] = '<script type="application/ld+json">' . wp_json_encode( $schema, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES ) . '</script>';

		} elseif ( is_front_page() ) {
			$desc = get_bloginfo( 'description' );
			if ( $desc ) {
				$righe[] = '<meta name="description" content="' . esc_attr( $desc ) . '">';
				$righe[] = '<meta property="og:description" content="' . esc_attr( $desc ) . '">';
			}
			$righe[] = '<meta property="og:type" content="website">';
			$righe[] = '<meta property="og:title" content="' . esc_attr( $sito ) . '">';
			$righe[] = '<meta property="og:url" content="' . esc_url( home_url( '/' ) ) . '">';
			$righe[] = '<meta property="og:site_name" content="' . esc_attr( $sito ) . '">';
		}

		if ( $righe ) {
			echo "\n<!-- RAL SEO -->\n" . implode( "\n", $righe ) . "\n<!-- /RAL SEO -->\n";
		}
	}, 5 );
}
